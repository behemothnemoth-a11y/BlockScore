from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import json
import math
from pathlib import Path
import re
import yaml

from .util import parse_fraction, round_fraction


@dataclass
class ContractResult:
    test_id: str
    path: str
    status: str
    checks: int
    failures: list[str]
    note: str = ""


def _yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _resolve(root: Path, rel: str) -> Path:
    return root / Path(rel)


def _pass(test_id, path, checks, note=""):
    return ContractResult(test_id, str(path), "PASS", checks, [], note)


def _fail(test_id, path, checks, failures):
    return ContractResult(test_id, str(path), "FAIL", checks, failures)


def _timing_contract(root: Path, path: Path, d: dict) -> ContractResult:
    qpm = int(d["benchmark_qpm"])
    hz = 20 if "COMMAND" in d["test_id"] else 10
    offsets = [parse_fraction(x) for x in d["ostinato_offsets_qn"]]
    expected_key = (
        "first_measure_expected_game_ticks"
        if hz == 20
        else "first_measure_expected_redstone_ticks"
    )
    expected = list(map(int, d[expected_key]))
    ticks = [round_fraction(x * Fraction(hz * 60, qpm)) for x in offsets]
    failures = []
    checks = 1
    if ticks != expected:
        failures.append(f"first measure ticks {ticks} != {expected}")

    checks += 1
    exact_per_qn = Fraction(hz * 60, qpm)
    if str(exact_per_qn) != str(d["derived"][f"{'game' if hz == 20 else 'redstone'}_ticks_per_qn"]):
        failures.append("derived ticks-per-QN mismatch")

    checks += len(d["absolute_bar_start_expectations"])
    for row in d["absolute_bar_start_expectations"]:
        got = round_fraction(parse_fraction(row["qn"]) * exact_per_qn)
        if got != int(row["tick"]):
            failures.append(f"measure {row['measure']} tick {got} != {row['tick']}")

    checks += 2
    if ticks != sorted(ticks):
        failures.append("event order reversed")
    if len(ticks) != len(set(ticks)):
        failures.append("sequence collapse in first-measure vector")

    return _fail(d["test_id"], path, checks, failures) if failures else _pass(
        d["test_id"], path, checks
    )


def _allocation_contract(root: Path, path: Path, d: dict) -> ContractResult:
    busy = int(d["settings"]["busy_window_game_ticks"])
    failures = []
    checks = 0
    for case in d.get("cases", []):
        attacks = case.get("attacks")
        if attacks is None:
            attacks = [{"tick": t} for t in case.get("first_measure_attack_ticks", [])]
        ticks = sorted(int(x["tick"]) for x in attacks)
        free: list[int] = []
        next_pool = 0
        for tick in ticks:
            free.sort()
            if free and free[0] <= tick:
                free.pop(0)
            else:
                next_pool += 1
            free.append(tick + busy)
        expected = case["expected"]
        if "required_pool_size" in expected:
            checks += 1
            if next_pool != int(expected["required_pool_size"]):
                failures.append(
                    f"{case['case_id']}: pool {next_pool} != {expected['required_pool_size']}"
                )
        if "minimum_tick_spacing" in expected and len(ticks) > 1:
            checks += 1
            spacing = min(b - a for a, b in zip(ticks, ticks[1:]))
            if spacing != int(expected["minimum_tick_spacing"]):
                failures.append(
                    f"{case['case_id']}: spacing {spacing} != {expected['minimum_tick_spacing']}"
                )
    return _fail(d["test_id"], path, checks, failures) if failures else _pass(
        d["test_id"], path, checks
    )


def _prototype_contract(root: Path, path: Path, d: dict) -> ContractResult:
    manifest_path = _resolve(root, d["prototype"])
    manifest = _yaml(manifest_path)
    pack_root = manifest_path.parent / "datapack" / "BlockScore_Mars_CR_01"
    place = (pack_root / "data/blockscore/function/build/place_bank.mcfunction").read_text()
    dispatch = (pack_root / "data/blockscore/function/song/dispatch.mcfunction").read_text()
    pack = json.loads((pack_root / "pack.mcmeta").read_text())
    expected = d["expected"]
    checks = 0
    failures = []

    comparisons = {
        "endpoint_count": int(manifest["endpoint_count"]),
        "song_event_count": int(manifest["song_event_count"]),
        "normal_attack_playsound_commands": len(
            re.findall(r"(?m)^(?!#).*\bplaysound\b", dispatch)
        ),
        "last_schedule_tick": max(
            int(x) for x in re.findall(r"matches\s+(\d+)", dispatch)
        ),
    }
    for key, got in comparisons.items():
        checks += 1
        if got != expected[key]:
            failures.append(f"{key}: {got} != {expected[key]}")

    note_blocks = len(re.findall(r"(?m)^setblock .*note_block", place))
    checks += 1
    if note_blocks != expected["endpoint_count"]:
        failures.append(f"placed note blocks {note_blocks} != {expected['endpoint_count']}")

    checks += 2
    if pack["pack"]["min_format"] != expected["pack_min_format"]:
        failures.append("pack min_format mismatch")
    if pack["pack"]["max_format"] != expected["pack_max_format"]:
        failures.append("pack max_format mismatch")

    return _fail(d["test_id"], path, checks, failures) if failures else _pass(
        d["test_id"], path, checks
    )


def _backend_neutrality(root: Path, path: Path, d: dict) -> ContractResult:
    fixture = _yaml(_resolve(root, d["fixture"]))
    failures = []
    checks = 0
    forbidden = list(d["forbidden_at_master_stage"])
    for event in fixture["events"]:
        backend = event.get("backend") or {}
        for field in forbidden:
            checks += 1
            if backend.get(field) is not None:
                failures.append(f"{event['id']}: backend.{field} is not null")
    return _fail(d["test_id"], path, checks, failures) if failures else _pass(
        d["test_id"], path, checks
    )


def _master_integrity(root: Path, path: Path, d: dict) -> ContractResult:
    fixture = _yaml(_resolve(root, d["fixture"]))
    events = fixture["events"]
    exp = d["expected"]
    failures = []
    checks = 1
    if len(events) != int(exp["master_event_count"]):
        failures.append(f"master event count {len(events)} != {exp['master_event_count']}")
    counts = Counter(x["master_voice_id"] for x in events)
    for voice, expected in exp["master_event_counts"].items():
        checks += 1
        if counts[voice] != int(expected):
            failures.append(f"{voice}: {counts[voice]} != {expected}")

    source_ids = []
    master_ids = []
    for event in events:
        master_ids.append(event["id"])
        source = event["source"]
        source_ids.extend(source.get("event_ids", []))
        if "event_id" in source:
            source_ids.append(source["event_id"])
    checks += 2
    if len(master_ids) != len(set(master_ids)):
        failures.append("duplicate master event IDs")
    if len(source_ids) != int(exp["source_event_count"]) or len(set(source_ids)) != len(source_ids):
        failures.append(
            f"source ID accounting total={len(source_ids)} unique={len(set(source_ids))} "
            f"expected={exp['source_event_count']}"
        )
    return _fail(d["test_id"], path, checks, failures) if failures else _pass(
        d["test_id"], path, checks
    )


def _compiled_command_rail(root: Path, path: Path, d: dict) -> ContractResult:
    plan = json.loads(_resolve(root, d["build_plan"]).read_text(encoding="utf-8"))
    endpoints = _yaml(_resolve(root, d["endpoint_fixture"]))
    schedule = _yaml(_resolve(root, d["schedule"]))
    exp = d["expected"]
    failures = []
    checks = 0
    metrics = plan["metrics"]
    mapping = {
        "master_events": metrics["master_events"],
        "endpoint_keys": metrics["endpoint_keys"],
        "endpoint_count": metrics["endpoint_count"],
        "largest_pool_size": metrics["largest_pool_size"],
        "activate_actions": metrics["activate_actions"],
        "reset_actions": metrics["reset_actions"],
        "max_activate_actions_one_tick": metrics["max_activate_actions_one_tick"],
    }
    for key, got in mapping.items():
        checks += 1
        if got != exp[key]:
            failures.append(f"{key}: {got} != {exp[key]}")

    endpoint_rows = endpoints.get("endpoints", endpoints)
    if isinstance(endpoint_rows, dict):
        endpoint_rows = list(endpoint_rows.values())
    checks += 1
    positions = []
    for row in endpoint_rows:
        pos = row.get("note") or row.get("note_position") or row.get("coordinates")
        if pos is not None:
            positions.append(tuple(pos) if isinstance(pos, list) else str(pos))
    if positions and len(set(positions)) != exp["unique_note_positions"]:
        failures.append("endpoint note positions are not unique")

    checks += 1
    if float(metrics["max_listener_distance_blocks"]) >= float(
        exp["max_listener_distance_lt_blocks"]
    ):
        failures.append("listener distance exceeds contract")

    return _fail(d["test_id"], path, checks, failures) if failures else _pass(
        d["test_id"], path, checks
    )


def _static_instrument_contract(root: Path, path: Path, d: dict) -> ContractResult:
    custom = json.loads(
        (root / "data/java-26.2/custom-instruments.json").read_text(encoding="utf-8")
    )
    by_block = {x["minecraft_block"]: x for x in custom["instruments"]}
    failures = []
    checks = 0
    blocks = []

    def collect(value):
        if isinstance(value, dict):
            for v in value.values():
                collect(v)
        elif isinstance(value, list):
            for v in value:
                collect(v)
        elif isinstance(value, str) and value.startswith("blockscore:") and value.endswith("_block"):
            blocks.append(value)

    collect(d.get("new_blocks", {}))
    if d["test_id"] == "INSTRUMENT-CUSTOM-001":
        blocks.append(d["registry"]["expected_block"])

    for block in blocks:
        checks += 1
        if block not in by_block:
            failures.append(f"registry missing {block}")

    if d["test_id"] == "INSTRUMENT-CUSTOM-001":
        item = by_block.get(d["registry"]["expected_block"])
        if item:
            checks += 5
            if item["provider_id"] != d["registry"]["expected_provider"]:
                failures.append("provider mismatch")
            if item["sound_event"] != d["registry"]["expected_sound_event"]:
                failures.append("sound event mismatch")
            if item["note_state_min"] != d["state_contract"]["note"]["minimum"]:
                failures.append("note min mismatch")
            if item["note_state_max"] != d["state_contract"]["note"]["maximum"]:
                failures.append("note max mismatch")
            if item["sample_strategy"]["root_note_states"] != d["samples"]["expected_root_note_states"]:
                failures.append("sample roots mismatch")

    return _fail(d["test_id"], path, checks, failures) if failures else _pass(
        d["test_id"], path, checks
    )


def _backend_comparison(root: Path, path: Path, d: dict) -> ContractResult:
    data = _yaml(_resolve(root, d["comparison"]))
    exp = d["expected"]
    backends = data["backends"]
    failures = []
    checks = 0
    values = {
        "command_rail_note_blocks": backends["COMMAND_RAIL_PHYSICAL"]["physical_note_blocks"],
        "redstone_note_blocks": backends["REDSTONE_PHYSICAL"]["physical_note_blocks"],
        "command_and_digital_rms_error_ms": backends["COMMAND_RAIL_PHYSICAL"]["timing"]["rms_error_ms"],
        "redstone_source_rms_error_ms": backends["REDSTONE_PHYSICAL"]["timing"]["rms_error_ms"],
    }
    reduction = 100.0 * (1.0 - values["command_rail_note_blocks"] / values["redstone_note_blocks"])
    values["physical_note_block_reduction_percent"] = reduction
    for key, expected in exp.items():
        checks += 1
        got = values[key]
        if isinstance(expected, float):
            if not math.isclose(float(got), float(expected), abs_tol=1e-6):
                failures.append(f"{key}: {got} != {expected}")
        elif got != expected:
            failures.append(f"{key}: {got} != {expected}")
    return _fail(d["test_id"], path, checks, failures) if failures else _pass(d["test_id"], path, checks)


def _digital_compiled(root: Path, path: Path, d: dict) -> ContractResult:
    plan = json.loads(_resolve(root, d["build_plan"]).read_text(encoding="utf-8"))
    exp = d["expected"]
    metrics = plan["metrics"]
    failures = []
    checks = 0
    values = {
        "master_events": metrics["master_events"],
        "playsound_commands": metrics["playsound_commands"],
        "active_ticks": metrics["active_game_ticks"],
        "max_commands_one_tick": metrics["max_commands_one_tick"],
        "sequence_collapses": metrics["timing"]["sequence_collapses"],
        "rms_error_ms": metrics["timing"]["rms_error_ms"],
        "max_abs_error_ms": metrics["timing"]["max_abs_error_ms"],
        "explicit_stopsound_commands": metrics["explicit_note_off_commands"],
    }
    for key, expected in exp.items():
        checks += 1
        got = values[key]
        if isinstance(expected, float):
            if not math.isclose(float(got), float(expected), abs_tol=1e-6):
                failures.append(f"{key}: {got} != {expected}")
        elif got != expected:
            failures.append(f"{key}: {got} != {expected}")
    return _fail(d["test_id"], path, checks, failures) if failures else _pass(d["test_id"], path, checks)


def _redstone_compiled(root: Path, path: Path, d: dict) -> ContractResult:
    plan = json.loads(_resolve(root, d["build_plan"]).read_text(encoding="utf-8"))
    exp = d["expected"]
    metrics = plan["metrics"]
    failures = []
    checks = 0
    values = {
        "master_events": metrics["master_events"],
        "timing_nodes": metrics["timing_nodes"],
        "sequence_collapses": metrics["source_tempo_timing"]["sequence_collapses"],
        "source_qpm": metrics["source_tempo_qpm"],
        "source_rms_error_ms": metrics["source_tempo_timing"]["rms_error_ms"],
        "source_weighted_rms_error_ms": metrics["source_tempo_timing"]["weighted_rms_error_ms"],
        "source_max_abs_error_ms": metrics["source_tempo_timing"]["max_abs_error_ms"],
        "note_blocks": metrics["physical_note_blocks"],
        "minimum_timing_trunk_repeaters": plan["layout"]["options"]["timing_trunk_repeater_lower_bound"],
        "geometry_status": plan["layout"]["options"]["geometry_pass"],
    }
    for key, expected in exp.items():
        checks += 1
        got = values[key]
        if isinstance(expected, float):
            if not math.isclose(float(got), float(expected), abs_tol=1e-6):
                failures.append(f"{key}: {got} != {expected}")
        elif got != expected:
            failures.append(f"{key}: {got} != {expected}")
    return _fail(d["test_id"], path, checks, failures) if failures else _pass(d["test_id"], path, checks)


HANDLERS = {
    "TIMING-MARS-001A-COMMAND": _timing_contract,
    "TIMING-MARS-001A-REDSTONE": _timing_contract,
    "COMMAND-RAIL-MARS-001A": _allocation_contract,
    "PROTOTYPE-MARS-COMMAND-RAIL-01": _prototype_contract,
    "ARRANGEMENT-MARS-001A-BACKEND-NEUTRALITY": _backend_neutrality,
    "ARRANGEMENT-MARS-001A-MASTER-INTEGRITY": _master_integrity,
    "COMMAND-RAIL-MARS-001A-COMPILED-B04": _compiled_command_rail,
    "INSTRUMENT-CUSTOM-001": _static_instrument_contract,
    "INSTRUMENT-STATIC-V05-001": _static_instrument_contract,
    "BACKEND-COMPARISON-MARS-001A-B04": _backend_comparison,
    "DIGITAL-MARS-001A-COMPILED-B04": _digital_compiled,
    "REDSTONE-MARS-001A-COMPILED-B04": _redstone_compiled,
}


def run_contracts(root: Path) -> list[ContractResult]:
    results: list[ContractResult] = []
    seen: set[str] = set()
    for path in sorted((root / "tests").rglob("*.yaml")):
        d = _yaml(path)
        test_id = d.get("test_id")
        if not test_id:
            results.append(
                ContractResult("<missing>", str(path.relative_to(root)), "FAIL", 0, ["missing test_id"])
            )
            continue
        if test_id in seen:
            results.append(
                ContractResult(test_id, str(path.relative_to(root)), "FAIL", 0, ["duplicate test_id"])
            )
            continue
        seen.add(test_id)
        handler = HANDLERS.get(test_id)
        if handler is None:
            results.append(
                ContractResult(
                    test_id,
                    str(path.relative_to(root)),
                    "STRUCTURAL_ONLY",
                    0,
                    [],
                    "YAML parses but semantic assertion handler is not implemented yet",
                )
            )
        else:
            result = handler(root, path, d)
            result.path = str(path.relative_to(root))
            results.append(result)
    return results
