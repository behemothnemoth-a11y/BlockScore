from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class InstrumentDef:
    id: str
    index: int
    custom: bool
    minecraft_instrument: str | None
    minecraft_block: str | None
    support_block: str
    note_state_min: int
    note_state_max: int
    pitch_mode: str


class InstrumentRegistry:
    def __init__(self, instruments: dict[str, InstrumentDef]):
        self.instruments = instruments

    def __getitem__(self, instrument_id: str) -> InstrumentDef:
        return self.instruments[instrument_id]

    def order_key(self, instrument_id: str) -> tuple[int, str]:
        d = self[instrument_id]
        return (d.index, d.id)

    @classmethod
    def load(cls, repo_root: Path, profile: str = "java-26.2") -> "InstrumentRegistry":
        data_dir = repo_root / "data" / profile
        vanilla = json.loads((data_dir / "instruments.json").read_text(encoding="utf-8"))
        custom = json.loads((data_dir / "custom-instruments.json").read_text(encoding="utf-8"))
        out: dict[str, InstrumentDef] = {}
        for item in vanilla["instruments"]:
            out[item["id"]] = InstrumentDef(
                id=item["id"],
                index=int(item["index"]),
                custom=False,
                minecraft_instrument=item["minecraft_instrument"],
                minecraft_block=None,
                support_block=item["canonical_support_block"],
                note_state_min=int(item["note_state_min"]),
                note_state_max=int(item["note_state_max"]),
                pitch_mode=item["pitch_mode"],
            )
        base = 1000
        for offset, item in enumerate(custom["instruments"]):
            out[item["id"]] = InstrumentDef(
                id=item["id"],
                index=base + offset,
                custom=True,
                minecraft_instrument=None,
                minecraft_block=item["minecraft_block"],
                support_block="minecraft:polished_blackstone",
                note_state_min=int(item["note_state_min"]),
                note_state_max=int(item["note_state_max"]),
                pitch_mode=item["pitch_mode"],
            )
        return cls(out)

    def block_state(self, instrument_id: str, note_state: int) -> str:
        d = self[instrument_id]
        if not (d.note_state_min <= note_state <= d.note_state_max):
            raise ValueError(
                f"{instrument_id}: note state {note_state} outside "
                f"{d.note_state_min}..{d.note_state_max}"
            )
        if d.custom:
            return f"{d.minecraft_block}[note={note_state},powered=false]"
        return (
            "minecraft:note_block"
            f"[instrument={d.minecraft_instrument},note={note_state},powered=false]"
        )
