from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import yaml

from .util import parse_fraction


@dataclass(frozen=True)
class MasterEvent:
    id: str
    absolute_qn: Fraction
    instrument: str
    note_state: int
    pitch: str | None
    priority: str
    onset_group: str | None


def load_master_events(path: Path) -> tuple[dict, list[MasterEvent]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    events: list[MasterEvent] = []
    for item in raw.get("events", []):
        position = item["source"]["position"]
        minecraft = item["minecraft"]
        musical = item["musical"]
        backend = item.get("backend") or {}
        events.append(
            MasterEvent(
                id=item["id"],
                absolute_qn=parse_fraction(position["absolute_qn"]),
                instrument=minecraft["instrument"],
                note_state=int(minecraft["note_state"]),
                pitch=minecraft.get("pitch"),
                priority=musical["priority"],
                onset_group=backend.get("onset_group"),
            )
        )
    declared = raw.get("event_count")
    if declared is not None and int(declared) != len(events):
        raise ValueError(f"declared event_count={declared}, parsed={len(events)}")
    return raw, events
