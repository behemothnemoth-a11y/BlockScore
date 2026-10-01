from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import re
import zipfile

import jsonschema
import yaml

from .contracts import run_contracts


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: int = 0
    contract_summary: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors

    def check(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.errors.append(message)


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _schema_validate(report: ValidationReport, instance, schema, label: str) -> None:
    report.checks += 1
    try:
        jsonschema.Draft202012Validator(schema).validate(instance)
    except jsonschema.ValidationError as exc:
        report.errors.append(f"{label}: schema error at {list(exc.path)}: {exc.message}")


def _validate_mcfunctions(
    report: ValidationReport,
    files: dict[str, str],
    *,
    forbid_tick_command: bool = True,
) -> None:
    function_paths = {
        p[len("data/") : -len(".mcfunction")].replace("/function/", ":", 1)
        for p in files
        if p.startswith("data/") and p.endswith(".mcfunction") and "/function/" in p
    }

    for path, text in files.items():
        if not path.endswith(".mcfunction"):
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if forbid_tick_command and re.match(r"^tick(?:\s|$)", stripped):
                report.errors.append(
                    f"{path}:{line_number}: /tick is user-side and forbidden inside generated functions"
                )
            for match in re.finditer(
                r"\bfunction\s+([a-z0-9_.-]+):([a-z0-9_./-]+)", stripped
            ):
                ref = f"{match.group(1)}:{match.group(2)}"
                report.check(ref in function_paths, f"{path}:{line_number}: missing function {ref}")


def validate_generated_pack(path: Path) -> ValidationReport:
    report = ValidationReport()
    files: dict[str, str] = {}

    if path.is_dir():
        for p in path.rglob("*"):
            if p.is_file():
                rel = p.relative_to(path).as_posix()
                try:
                    files[rel] = p.read_text(encoding="utf-8-sig")
                except UnicodeDecodeError:
                    pass
    else:
        report.check(path.suffix.lower() == ".zip", f"{path}: expected directory or ZIP")
        if not report.ok:
            return report
        try:
            with zipfile.ZipFile(path) as zf:
                bad = zf.testzip()
                report.check(bad is None, f"{path}: corrupt ZIP member {bad}")
                for name in zf.namelist():
                    if name.endswith("/"):
                        continue
                    try:
                        files[name] = zf.read(name).decode("utf-8-sig")
                    except UnicodeDecodeError:
                        pass
        except zipfile.BadZipFile as exc:
            report.errors.append(f"{path}: invalid ZIP: {exc}")
            return report

    report.check("pack.mcmeta" in files, "generated pack missing pack.mcmeta")
    for required in (
        "data/minecraft/tags/function/load.json",
        "data/minecraft/tags/function/tick.json",
    ):
        report.check(required in files, f"generated pack missing {required}")

    for name, text in files.items():
        if name.endswith(".json") or name == "pack.mcmeta":
            report.checks += 1
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                report.errors.append(f"{name}: invalid JSON: {exc}")

    _validate_mcfunctions(report, files, forbid_tick_command=True)

    # Pure physical Command Rail packs should not silently use playsound.
    for name, text in files.items():
        if name.endswith(".mcfunction") and re.search(r"(?m)^(?!\s*#).*\bplaysound\b", text):
            report.errors.append(f"{name}: physical pack contains playsound command")

    return report


def _validate_custom_resources(root: Path, report: ValidationReport) -> None:
    custom = _load_json(root / "data/java-26.2/custom-instruments.json")
    lang = _load_json(
        root
        / "fabric/blockscore-instruments/src/main/resources/assets/blockscore/lang/en_us.json"
    )
    sounds = _load_json(
        root
        / "fabric/blockscore-instruments/src/main/resources/assets/blockscore/sounds.json"
    )
    resource_root = (
        root / "fabric/blockscore-instruments/src/main/resources/assets/blockscore"
    )

    ids = [x["id"] for x in custom["instruments"]]
    blocks = [x["minecraft_block"] for x in custom["instruments"]]
    report.check(len(ids) == len(set(ids)), "duplicate custom instrument IDs")
    report.check(len(blocks) == len(set(blocks)), "duplicate custom Minecraft block IDs")

    for item in custom["instruments"]:
        block = item["minecraft_block"].split(":", 1)[1]
        for rel in (
            f"blockstates/{block}.json",
            f"items/{block}.json",
            f"models/block/{block}.json",
        ):
            report.check((resource_root / rel).exists(), f"{item['id']}: missing {rel}")
        report.check(
            f"block.blockscore.{block}" in lang,
            f"{item['id']}: missing language entry",
        )
        sound_event = item["sound_event"].split(":", 1)[1]
        report.check(
            sound_event in sounds,
            f"{item['id']}: missing sounds.json event {sound_event}",
        )

        strategy = item["sample_strategy"]
        asset_dir = strategy["asset_directory"].split(":", 1)[1]
        sample_dir = resource_root / asset_dir
        expected: list[str] = []
        pattern = strategy["file_pattern"]
        if "root_midi" in strategy:
            expected = [pattern.replace("{midi}", str(x)) for x in strategy["root_midi"]]
        elif "root_note_states" in strategy:
            expected = [
                pattern.replace("{note_state_2d}", f"{x:02d}")
                for x in strategy["root_note_states"]
            ]
        elif "register_note_states" in strategy:
            variants = "abcdefghijklmnopqrstuvwxyz"
            for register in strategy["register_note_states"]:
                for i in range(strategy["variants_per_register"]):
                    expected.append(
                        pattern.replace("{register}", register).replace(
                            "{variant}", variants[i]
                        )
                    )
        for filename in expected:
            report.check(
                (sample_dir / filename).exists(),
                f"{item['id']}: missing declared sample {asset_dir}/{filename}",
            )


def _validate_schemas(root: Path, report: ValidationReport) -> None:
    specs = root / "specs"
    instrument_schema = _load_json(specs / "instrument.schema.json")
    custom_schema = _load_json(specs / "custom-instrument.schema.json")
    event_schema = _load_json(specs / "event.schema.json")

    vanilla = _load_json(root / "data/java-26.2/instruments.json")
    custom = _load_json(root / "data/java-26.2/custom-instruments.json")
    events = _load_yaml(root / "fixtures/mars/master-events-m001-m008.yaml")

    for item in vanilla["instruments"]:
        _schema_validate(report, item, instrument_schema, f"instrument:{item['id']}")
    for item in custom["instruments"]:
        _schema_validate(report, item, custom_schema, f"custom-instrument:{item['id']}")
    for item in events["events"]:
        _schema_validate(report, item, event_schema, f"master-event:{item['id']}")


def validate_repo(root: Path, *, minimum_semantic_contracts: int = 12) -> ValidationReport:
    root = root.resolve()
    report = ValidationReport()

    # All machine-readable files must at least parse.
    for path in sorted(root.rglob("*.json")):
        if ".git" in path.parts or ".venv" in path.parts:
            continue
        report.checks += 1
        try:
            _load_json(path)
        except Exception as exc:
            report.errors.append(f"{path.relative_to(root)}: invalid JSON: {exc}")

    for path in sorted(root.rglob("*.yaml")) + sorted(root.rglob("*.yml")):
        if ".git" in path.parts or ".venv" in path.parts:
            continue
        report.checks += 1
        try:
            _load_yaml(path)
        except Exception as exc:
            report.errors.append(f"{path.relative_to(root)}: invalid YAML: {exc}")

    _validate_schemas(root, report)
    _validate_custom_resources(root, report)

    # Validate all repository datapack functions that exist today.
    for pack_mcmeta in root.rglob("pack.mcmeta"):
        if ".git" in pack_mcmeta.parts or ".venv" in pack_mcmeta.parts:
            continue
        pack_root = pack_mcmeta.parent
        files: dict[str, str] = {}
        for p in pack_root.rglob("*"):
            if p.is_file():
                try:
                    files[p.relative_to(pack_root).as_posix()] = p.read_text(
                        encoding="utf-8-sig"
                    )
                except UnicodeDecodeError:
                    pass
        _validate_mcfunctions(report, files, forbid_tick_command=True)

    contract_results = run_contracts(root)
    failed = [x for x in contract_results if x.status == "FAIL"]
    passed = [x for x in contract_results if x.status == "PASS"]
    structural = [x for x in contract_results if x.status == "STRUCTURAL_ONLY"]
    for result in failed:
        for failure in result.failures:
            report.errors.append(f"{result.test_id}: {failure}")

    report.check(
        len(passed) >= minimum_semantic_contracts,
        f"semantic contract coverage {len(passed)} < required {minimum_semantic_contracts}",
    )
    if structural:
        report.warnings.append(
            f"{len(structural)} YAML tests currently parse but do not yet have semantic handlers"
        )
    report.contract_summary = {
        "total": len(contract_results),
        "semantic_pass": len(passed),
        "semantic_fail": len(failed),
        "structural_only": len(structural),
        "results": [
            {
                "test_id": x.test_id,
                "path": x.path,
                "status": x.status,
                "checks": x.checks,
                "failures": x.failures,
                "note": x.note,
            }
            for x in contract_results
        ],
    }
    return report

