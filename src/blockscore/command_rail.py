from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
import heapq
import json
from pathlib import Path
import shutil

from .master import MasterEvent
from .registry import InstrumentRegistry
from .util import round_fraction, safe_id, scoreboard_objective


@dataclass(frozen=True)
class Endpoint:
    id: str
    instrument: str
    note_state: int
    pitch: str | None
    pool_index: int
    x: int
    y: int
    z: int

    @property
    def driver(self) -> tuple[int, int, int]:
        return (self.x, self.y + 1, self.z + 1)


@dataclass(frozen=True)
class CompiledAttack:
    event: MasterEvent
    tick: int
    exact_tick: Fraction
    endpoint_id: str


@dataclass
class CommandRailCompilation:
    attacks: list[CompiledAttack]
    endpoints: list[Endpoint]
    actions: dict[int, dict[str, list[str]]]
    metrics: dict
    build_plan: dict


def _endpoint_key(event: MasterEvent) -> tuple[str, int]:
    return (event.instrument, event.note_state)


def _quantize(event: MasterEvent, qpm: int, tps: int) -> tuple[int, Fraction]:
    exact_tick = event.absolute_qn * Fraction(tps * 60, qpm)
    return round_fraction(exact_tick), exact_tick


def _allocate_pools(
    events: list[tuple[MasterEvent, int, Fraction]],
    busy_window_ticks: int,
) -> tuple[dict[str, tuple[tuple[str, int], int]], dict[tuple[str, int], int]]:
    by_key: dict[tuple[str, int], list[tuple[MasterEvent, int, Fraction]]] = defaultdict(list)
    for row in events:
        by_key[_endpoint_key(row[0])].append(row)

    assignment: dict[str, tuple[tuple[str, int], int]] = {}
    pool_sizes: dict[tuple[str, int], int] = {}

    for key in sorted(by_key):
        rows = sorted(by_key[key], key=lambda r: (r[1], r[0].id))
        available: list[tuple[int, int]] = []
        next_pool = 0
        for event, tick, _ in rows:
            if available and available[0][0] <= tick:
                _, pool_index = heapq.heappop(available)
            else:
                pool_index = next_pool
                next_pool += 1
            assignment[event.id] = (key, pool_index)
            # The endpoint is not reusable until the busy window has elapsed.
            heapq.heappush(available, (tick + busy_window_ticks, pool_index))
        pool_sizes[key] = next_pool
    return assignment, pool_sizes


def _layout_endpoints(
    registry: InstrumentRegistry,
    pool_sizes: dict[tuple[str, int], int],
    pitch_by_key: dict[tuple[str, int], str | None],
    instrument_gap: int,
) -> tuple[list[Endpoint], dict[tuple[tuple[str, int], int], Endpoint]]:
    by_instrument: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for key in pool_sizes:
        by_instrument[key[0]].append(key)

    endpoints: list[Endpoint] = []
    lookup: dict[tuple[tuple[str, int], int], Endpoint] = {}
    x = 0
    instruments = sorted(by_instrument, key=registry.order_key)

    for instrument_index, instrument in enumerate(instruments):
        for key in sorted(by_instrument[instrument], key=lambda k: k[1]):
            for pool_index in range(pool_sizes[key]):
                pitch = pitch_by_key.get(key)
                pitch_label = (pitch or f"state{key[1]}").replace("#", "s").replace("b", "f")
                endpoint_id = safe_id(
                    f"{instrument}_{pitch_label}_{pool_index + 1:02d}",
                    "endpoint",
                )
                endpoint = Endpoint(
                    id=endpoint_id,
                    instrument=instrument,
                    note_state=key[1],
                    pitch=pitch,
                    pool_index=pool_index,
                    x=x,
                    y=0,
                    z=0,
                )
                endpoints.append(endpoint)
                lookup[(key, pool_index)] = endpoint
                x += 1
        if instrument_index != len(instruments) - 1:
            x += instrument_gap
    return endpoints, lookup


def compile_command_rail(
    events: list[MasterEvent],
    registry: InstrumentRegistry,
    *,
    qpm: int,
    tps: int = 20,
    pulse_ticks: int = 1,
    busy_window_ticks: int = 2,
    instrument_gap: int = 1,
    profile: str = "java-26.2",
) -> CommandRailCompilation:
    if qpm <= 0 or tps <= 0:
        raise ValueError("qpm and tps must be positive")
    if pulse_ticks < 1:
        raise ValueError("pulse_ticks must be >= 1")
    if busy_window_ticks < pulse_ticks:
        raise ValueError("busy_window_ticks must be >= pulse_ticks")
    if len({e.id for e in events}) != len(events):
        raise ValueError("master event IDs must be unique")

    quantized: list[tuple[MasterEvent, int, Fraction]] = []
    pitch_by_key: dict[tuple[str, int], str | None] = {}
    errors_ms: list[float] = []

    for event in events:
        definition = registry[event.instrument]
        if not (definition.note_state_min <= event.note_state <= definition.note_state_max):
            raise ValueError(f"{event.id}: invalid note state {event.note_state}")
        tick, exact_tick = _quantize(event, qpm, tps)
        quantized.append((event, tick, exact_tick))
        key = _endpoint_key(event)
        pitch_by_key.setdefault(key, event.pitch)
        errors_ms.append(float(Fraction(tick, tps) - event.absolute_qn * Fraction(60, qpm)) * 1000.0)

    assignment, pool_sizes = _allocate_pools(quantized, busy_window_ticks)
    endpoints, endpoint_lookup = _layout_endpoints(
        registry, pool_sizes, pitch_by_key, instrument_gap
    )

    attacks: list[CompiledAttack] = []
    actions: dict[int, dict[str, list[str]]] = defaultdict(lambda: {"activate": [], "reset": []})
    for event, tick, exact_tick in sorted(quantized, key=lambda r: (r[1], r[0].id)):
        key, pool_index = assignment[event.id]
        endpoint = endpoint_lookup[(key, pool_index)]
        attacks.append(CompiledAttack(event, tick, exact_tick, endpoint.id))
        actions[tick]["activate"].append(endpoint.id)
        actions[tick + pulse_ticks]["reset"].append(endpoint.id)

    endpoint_by_id = {e.id: e for e in endpoints}
    max_commands = 0
    max_activates = 0
    for action in actions.values():
        action["activate"].sort()
        action["reset"].sort()
        max_commands = max(max_commands, len(action["activate"]) + len(action["reset"]))
        max_activates = max(max_activates, len(action["activate"]))

    last_action_tick = max(actions) if actions else 0
    metrics = {
        "master_events": len(events),
        "physical_endpoint_count": len(endpoints),
        "endpoint_key_count": len(pool_sizes),
        "largest_pool_size": max(pool_sizes.values(), default=0),
        "activate_actions": len(attacks),
        "reset_actions": len(attacks),
        "action_tick_count": len(actions),
        "last_action_tick": last_action_tick,
        "max_activate_actions_one_tick": max_activates,
        "max_total_actions_one_tick": max_commands,
        "max_abs_onset_error_ms": max((abs(x) for x in errors_ms), default=0.0),
        "mean_abs_onset_error_ms": (
            sum(abs(x) for x in errors_ms) / len(errors_ms) if errors_ms else 0.0
        ),
        "tps": tps,
        "qpm": qpm,
        "pulse_ticks": pulse_ticks,
        "busy_window_ticks": busy_window_ticks,
    }

    x_values = [e.x for e in endpoints] or [0]
    build_plan = {
        "profile": profile,
        "backend": "COMMAND_RAIL_PHYSICAL",
        "status": "COMPILED",
        "origin": {"x": 0, "y": 0, "z": 0},
        "performance_origin": None,
        "layout": {
            "type": "SINGLE_LINE",
            "direction": "EAST",
            "options": {
                "instrument_gap": instrument_gap,
                "endpoint_count": len(endpoints),
                "x_min": min(x_values),
                "x_max": max(x_values),
                "bank_span_blocks": max(x_values) - min(x_values) + 1,
                "driver_depth_blocks": 2,
                "required_height_blocks": 3,
            },
        },
        "materials": {},
        "metrics": metrics,
        "warnings": [
            "TICK_RATE_USER_MANAGED",
            "WORLD_COLLISION_PREFLIGHT_NOT_IMPLEMENTED",
        ],
        "failures": [],
        "calibration_dependencies": ["CAL-003", "CAL-004", "CAL-005", "CAL-006"],
        "artifacts": [],
    }

    # Useful deterministic lookup for generated artifacts.
    build_plan["_endpoint_registry"] = [
        {
            "id": e.id,
            "instrument": e.instrument,
            "pitch": e.pitch,
            "note_state": e.note_state,
            "pool_index": e.pool_index,
            "note": [e.x, e.y + 1, e.z],
            "support": [e.x, e.y, e.z],
            "driver": list(e.driver),
        }
        for e in endpoints
    ]
    build_plan["_schedule"] = {
        str(tick): actions[tick] for tick in sorted(actions)
    }
    return CommandRailCompilation(attacks, endpoints, dict(actions), metrics, build_plan)


def write_datapack(
    compilation: CommandRailCompilation,
    registry: InstrumentRegistry,
    output_dir: Path,
    *,
    namespace: str,
    title: str,
    required_tps: int,
    pack_format: tuple[int, int] = (107, 1),
) -> Path:
    namespace = safe_id(namespace)
    objective = scoreboard_objective(namespace)
    anchor_tag = f"{namespace}_anchor"

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    fn_root = output_dir / "data" / namespace / "function"
    for sub in ("build", "control", "song/action", "song/dispatch"):
        (fn_root / sub).mkdir(parents=True, exist_ok=True)
    tag_root = output_dir / "data" / "minecraft" / "tags" / "function"
    tag_root.mkdir(parents=True, exist_ok=True)

    def write(rel: str, text: str) -> None:
        path = output_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")

    endpoint_by_id = {e.id: e for e in compilation.endpoints}

    place: list[str] = [
        "# Generated by BlockScore core.",
        "# User is responsible for choosing a safe empty placement region.",
    ]
    clear: list[str] = ["# Clears only coordinates used by this generated bank."]
    reset: list[str] = ["# Reset every generated driver cell to air."]

    for endpoint in compilation.endpoints:
        support = registry[endpoint.instrument].support_block
        note = registry.block_state(endpoint.instrument, endpoint.note_state)
        x, y, z = endpoint.x, endpoint.y, endpoint.z
        place.extend(
            [
                f"setblock ~{x} ~{y} ~{z} {support}",
                f"setblock ~{x} ~{y + 1} ~{z} {note}",
                f"setblock ~{x} ~{y + 2} ~{z} minecraft:air",
                f"setblock ~{x} ~{y + 1} ~{z + 1} minecraft:air",
            ]
        )
        clear.extend(
            [
                f"setblock ~{x} ~{y + 1} ~{z + 1} minecraft:air",
                f"setblock ~{x} ~{y + 2} ~{z} minecraft:air",
                f"setblock ~{x} ~{y + 1} ~{z} minecraft:air",
                f"setblock ~{x} ~{y} ~{z} minecraft:air",
            ]
        )
        reset.append(f"setblock ~{x} ~{y + 1} ~{z + 1} minecraft:air")

    # Standard physical play/stop lever, tick-rate remains explicitly user-side.
    place.extend(
        [
            "setblock ~-3 ~0 ~0 minecraft:polished_blackstone",
            "setblock ~-3 ~1 ~0 minecraft:lever[face=floor,facing=north,powered=false]",
        ]
    )
    clear.extend(
        [
            "setblock ~-3 ~1 ~0 minecraft:air",
            "setblock ~-3 ~0 ~0 minecraft:air",
        ]
    )

    write(f"data/{namespace}/function/build/place_bank.mcfunction", "\n".join(place))
    write(f"data/{namespace}/function/build/clear_bank.mcfunction", "\n".join(clear))
    write(f"data/{namespace}/function/build/reset_drivers.mcfunction", "\n".join(reset))

    for tick in sorted(compilation.actions):
        action = compilation.actions[tick]
        lines = [f"# {title} action tick {tick}"]
        # Reset before activate if a future allocator permits same-tick reuse.
        for endpoint_id in action["reset"]:
            e = endpoint_by_id[endpoint_id]
            x, y, z = e.driver
            lines.append(
                f"execute at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"run setblock ~{x} ~{y} ~{z} minecraft:air"
            )
        for endpoint_id in action["activate"]:
            e = endpoint_by_id[endpoint_id]
            x, y, z = e.driver
            lines.append(
                f"execute at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"run setblock ~{x} ~{y} ~{z} minecraft:redstone_block"
            )
        write(
            f"data/{namespace}/function/song/action/t{tick:06d}.mcfunction",
            "\n".join(lines),
        )

    action_ticks = sorted(compilation.actions)
    node_counter = 0

    def dispatch_node(ticks: list[int]) -> str:
        nonlocal node_counter
        name = f"n{node_counter:05d}"
        node_counter += 1
        if len(ticks) <= 8:
            lines = [
                f"execute if score #tick {objective} matches {tick} "
                f"run function {namespace}:song/action/t{tick:06d}"
                for tick in ticks
            ]
        else:
            middle = len(ticks) // 2
            left = dispatch_node(ticks[:middle])
            right = dispatch_node(ticks[middle:])
            lines = [
                f"execute if score #tick {objective} matches {ticks[0]}..{ticks[middle - 1]} "
                f"run function {namespace}:song/dispatch/{left}",
                f"execute if score #tick {objective} matches {ticks[middle]}..{ticks[-1]} "
                f"run function {namespace}:song/dispatch/{right}",
            ]
        write(f"data/{namespace}/function/song/dispatch/{name}.mcfunction", "\n".join(lines))
        return name

    root_node = dispatch_node(action_ticks) if action_ticks else None
    root_text = (
        f"function {namespace}:song/dispatch/{root_node}"
        if root_node
        else "# no scheduled actions"
    )
    write(f"data/{namespace}/function/song/dispatch/root.mcfunction", root_text)

    write(
        f"data/{namespace}/function/load.mcfunction",
        "\n".join(
            [
                f"scoreboard objectives add {objective} dummy",
                f"execute if entity @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"run function {namespace}:build/reset_drivers",
                f"scoreboard players set #state {objective} 0",
                f"scoreboard players set #tick {objective} 0",
                f"scoreboard players set #lever {objective} 0",
            ]
        ),
    )

    write(
        f"data/{namespace}/function/install.mcfunction",
        "\n".join(
            [
                f"execute if entity @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"run function {namespace}:build/clear_bank",
                f"kill @e[type=minecraft:marker,tag={anchor_tag}]",
                "execute at @s align xyz run summon minecraft:marker ~ ~ ~",
                "execute at @s align xyz run tag "
                f"@e[type=minecraft:marker,sort=nearest,limit=1,distance=..0.1] add {anchor_tag}",
                f"execute at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"run function {namespace}:build/place_bank",
                f"scoreboard players set #state {objective} 0",
                f"scoreboard players set #tick {objective} 0",
                f"scoreboard players set #lever {objective} 0",
                f'tellraw @s {{"text":"{title} installed. Set /tick rate {required_tps}, '
                f'then flip the lever.","color":"green"}}',
            ]
        ),
    )

    write(
        f"data/{namespace}/function/control/lever_on.mcfunction",
        "\n".join(
            [
                f"function {namespace}:build/reset_drivers",
                f"scoreboard players set #tick {objective} 0",
                f"scoreboard players set #state {objective} 1",
                f"scoreboard players set #lever {objective} 1",
            ]
        ),
    )
    write(
        f"data/{namespace}/function/control/lever_off.mcfunction",
        "\n".join(
            [
                f"scoreboard players set #state {objective} 0",
                f"scoreboard players set #lever {objective} 0",
                f"function {namespace}:build/reset_drivers",
            ]
        ),
    )
    write(
        f"data/{namespace}/function/control/start.mcfunction",
        "\n".join(
            [
                f"execute unless entity @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f'run tellraw @s {{"text":"Install {title} first.","color":"red"}}',
                f"execute if entity @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                "run setblock ~-3 ~1 ~0 minecraft:lever[face=floor,facing=north,powered=true]",
                f"execute if entity @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"run function {namespace}:control/lever_on",
            ]
        ),
    )
    write(
        f"data/{namespace}/function/control/stop.mcfunction",
        "\n".join(
            [
                f"execute if entity @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                "run setblock ~-3 ~1 ~0 minecraft:lever[face=floor,facing=north,powered=false]",
                f"scoreboard players set #state {objective} 0",
                f"scoreboard players set #lever {objective} 0",
                f"execute if entity @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"run function {namespace}:build/reset_drivers",
            ]
        ),
    )
    write(
        f"data/{namespace}/function/control/pause.mcfunction",
        f"scoreboard players set #state {objective} 0",
    )
    write(
        f"data/{namespace}/function/control/resume.mcfunction",
        "\n".join(
            [
                f"execute if entity @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"run function {namespace}:build/reset_drivers",
                f"scoreboard players set #state {objective} 1",
                f"scoreboard players set #lever {objective} 1",
            ]
        ),
    )
    write(
        f"data/{namespace}/function/control/reset.mcfunction",
        "\n".join(
            [
                f"scoreboard players set #state {objective} 0",
                f"scoreboard players set #tick {objective} 0",
                f"execute if entity @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"run function {namespace}:build/reset_drivers",
            ]
        ),
    )
    write(
        f"data/{namespace}/function/control/status.mcfunction",
        f'tellraw @s [{{"text":"{title} state="}},'
        f'{{"score":{{"name":"#state","objective":"{objective}"}}}},'
        f'{{"text":" tick="}},'
        f'{{"score":{{"name":"#tick","objective":"{objective}"}}}}]',
    )

    last_tick = compilation.metrics["last_action_tick"]
    write(
        f"data/{namespace}/function/control/finish.mcfunction",
        "\n".join(
            [
                f"scoreboard players set #state {objective} 0",
                f"scoreboard players set #lever {objective} 0",
                f"execute at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"run function {namespace}:build/reset_drivers",
                f"execute at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                "run setblock ~-3 ~1 ~0 minecraft:lever[face=floor,facing=north,powered=false]",
            ]
        ),
    )
    write(
        f"data/{namespace}/function/tick.mcfunction",
        "\n".join(
            [
                f"execute at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                "if block ~-3 ~1 ~0 minecraft:lever[powered=true] "
                f"if score #lever {objective} matches 0 run function {namespace}:control/lever_on",
                f"execute at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                "if block ~-3 ~1 ~0 minecraft:lever[powered=false] "
                f"if score #lever {objective} matches 1 run function {namespace}:control/lever_off",
                f"execute if score #state {objective} matches 1 "
                f"run function {namespace}:song/dispatch/root",
                f"execute if score #state {objective} matches 1 "
                f"run scoreboard players add #tick {objective} 1",
                f"execute if score #state {objective} matches 1 "
                f"if score #tick {objective} matches {last_tick + 1}.. "
                f"run function {namespace}:control/finish",
            ]
        ),
    )
    write(
        f"data/{namespace}/function/uninstall.mcfunction",
        "\n".join(
            [
                f"function {namespace}:control/stop",
                f"execute at @e[type=minecraft:marker,tag={anchor_tag},limit=1] "
                f"run function {namespace}:build/clear_bank",
                f"kill @e[type=minecraft:marker,tag={anchor_tag}]",
            ]
        ),
    )

    write(
        "data/minecraft/tags/function/load.json",
        json.dumps({"values": [f"{namespace}:load"]}, indent=2),
    )
    write(
        "data/minecraft/tags/function/tick.json",
        json.dumps({"values": [f"{namespace}:tick"]}, indent=2),
    )
    write(
        "pack.mcmeta",
        json.dumps(
            {
                "pack": {
                    "description": f"BlockScore {title} Command Rail",
                    "min_format": list(pack_format),
                    "max_format": list(pack_format),
                }
            },
            indent=2,
        ),
    )

    report = dict(compilation.build_plan)
    report.pop("_endpoint_registry", None)
    report.pop("_schedule", None)
    report["artifacts"] = ["blockscore-build-plan.json"]
    report["required_user_tick_rate"] = required_tps
    write("blockscore-build-plan.json", json.dumps(report, indent=2))

    endpoint_registry = compilation.build_plan["_endpoint_registry"]
    write("blockscore-endpoints.json", json.dumps(endpoint_registry, indent=2))
    write(
        "README.txt",
        "\n".join(
            [
                f"BlockScore — {title}",
                f"Required playback tick rate: {required_tps} TPS (user-managed)",
                "",
                "Install this datapack on the user side.",
                f"Run /tick rate {required_tps} before playback.",
                f"Run /function {namespace}:install while standing at the desired bank origin.",
                "Flip the generated lever to start/stop.",
                "Restore your preferred tick rate manually after listening.",
                "",
                "The datapack intentionally never executes the /tick command.",
            ]
        ),
    )
    return output_dir
