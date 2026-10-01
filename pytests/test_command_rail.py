from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import tempfile
import unittest

from blockscore.command_rail import compile_command_rail, write_datapack
from blockscore.master import MasterEvent, load_master_events
from blockscore.registry import InstrumentRegistry
from blockscore.validate import validate_generated_pack


ROOT = Path(__file__).resolve().parents[1]


class CommandRailCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = InstrumentRegistry.load(ROOT)

    def test_mars_reproduces_prototype_core_metrics(self):
        _, events = load_master_events(ROOT / "fixtures/mars/master-events-m001-m008.yaml")
        result = compile_command_rail(
            events,
            self.registry,
            qpm=132,
            tps=20,
            pulse_ticks=1,
            busy_window_ticks=2,
        )
        self.assertEqual(result.metrics["master_events"], 349)
        self.assertEqual(result.metrics["physical_endpoint_count"], 16)
        self.assertEqual(result.metrics["endpoint_key_count"], 15)
        self.assertEqual(result.metrics["largest_pool_size"], 2)
        self.assertEqual(result.metrics["activate_actions"], 349)
        self.assertEqual(result.metrics["reset_actions"], 349)
        self.assertEqual(result.metrics["last_action_tick"], 356)
        self.assertEqual(result.metrics["max_activate_actions_one_tick"], 10)

    def test_simultaneous_duplicate_chaos_allocates_real_polyphony(self):
        events = [
            MasterEvent(
                id=f"chaos-{i:04d}",
                absolute_qn=Fraction(0),
                instrument="guitar",
                note_state=13,
                pitch="G3",
                priority="P5",
                onset_group="wall",
            )
            for i in range(100)
        ]
        result = compile_command_rail(
            events,
            self.registry,
            qpm=120,
            tps=20,
            pulse_ticks=1,
            busy_window_ticks=2,
        )
        self.assertEqual(result.metrics["physical_endpoint_count"], 100)
        self.assertEqual(result.metrics["max_activate_actions_one_tick"], 100)

    def test_rapid_retrigger_respects_busy_window(self):
        events = [
            MasterEvent(
                id=f"r-{i}",
                absolute_qn=Fraction(i, 10),
                instrument="guitar",
                note_state=13,
                pitch="G3",
                priority="P5",
                onset_group=None,
            )
            for i in range(5)
        ]
        result = compile_command_rail(
            events,
            self.registry,
            qpm=120,
            tps=20,
            pulse_ticks=1,
            busy_window_ticks=2,
        )
        # 0.1 QN at 120 QPM/20TPS is exactly one tick: two endpoints alternate.
        self.assertEqual(result.metrics["physical_endpoint_count"], 2)

    def test_generated_pack_has_no_embedded_tick_command(self):
        _, events = load_master_events(ROOT / "fixtures/mars/master-events-m001-m008.yaml")
        result = compile_command_rail(
            events,
            self.registry,
            qpm=132,
            tps=20,
            pulse_ticks=1,
            busy_window_ticks=2,
        )
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pack"
            write_datapack(
                result,
                self.registry,
                out,
                namespace="blockscore_test",
                title="Mars Test",
                required_tps=20,
            )
            validation = validate_generated_pack(out)
            self.assertTrue(validation.ok, validation.errors)

    def test_custom_v05_blocks_compile_physically(self):
        events = [
            MasterEvent(
                id="distorted",
                absolute_qn=Fraction(0),
                instrument="guitar_distorted_low",
                note_state=0,
                pitch="E2",
                priority="P5",
                onset_group="metal",
            ),
            MasterEvent(
                id="palm",
                absolute_qn=Fraction(1, 4),
                instrument="guitar_palm_mute_low",
                note_state=5,
                pitch="A2",
                priority="P5",
                onset_group="metal",
            ),
        ]
        result = compile_command_rail(
            events,
            self.registry,
            qpm=120,
            tps=100,
            pulse_ticks=5,
            busy_window_ticks=5,
        )
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pack"
            write_datapack(
                result,
                self.registry,
                out,
                namespace="blockscore_custom_test",
                title="Custom Test",
                required_tps=100,
            )
            bank = (out / "data/blockscore_custom_test/function/build/place_bank.mcfunction").read_text()
            self.assertIn("blockscore:guitar_distorted_low_note_block", bank)
            self.assertIn("blockscore:guitar_palm_mute_low_note_block", bank)
            self.assertTrue(validate_generated_pack(out).ok)

    def test_pack_linter_rejects_embedded_tick_command(self):
        _, events = load_master_events(ROOT / "fixtures/mars/master-events-m001-m008.yaml")
        result = compile_command_rail(
            events[:1],
            self.registry,
            qpm=132,
            tps=100,
            pulse_ticks=5,
            busy_window_ticks=5,
        )
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pack"
            write_datapack(
                result,
                self.registry,
                out,
                namespace="blockscore_tick_regression",
                title="Tick Regression",
                required_tps=100,
            )
            target = out / "data/blockscore_tick_regression/function/control/start.mcfunction"
            target.write_text(target.read_text(encoding="utf-8") + "tick rate 100\n", encoding="utf-8")
            validation = validate_generated_pack(out)
            self.assertFalse(validation.ok)
            self.assertTrue(any("/tick is user-side" in x for x in validation.errors))


if __name__ == "__main__":
    unittest.main()
