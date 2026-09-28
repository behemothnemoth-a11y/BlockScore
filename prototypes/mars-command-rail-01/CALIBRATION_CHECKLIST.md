# Calibration Checklist

## CAL-003 — Command Rail physical driver behavior

Run:

```text
/function blockscore:cal/003_driver
```

Record:

- Did a real note block sound?
- Exactly one attack?
- Any neighboring endpoint?
- Did the driver visibly/reset correctly if inspected?

Pass means the command-created adjacent redstone block can serve as the current physical driver.

## CAL-004 — minimum same-endpoint retrigger

Test both:

```text
/function blockscore:cal/004_retrigger_1tick
/function blockscore:cal/004_retrigger_2tick
```

Record separately.

The critical question is not whether commands ran. It is whether the same physical note block audibly produced both intended attacks.

If 1-tick passes reliably, the current `busy_window_game_ticks = 2` may be overly conservative.

If 1-tick fails and 2-tick passes, the current allocator assumption is supported.

## CAL-005 — same-tick multi-endpoint synchronization

Run:

```text
/function blockscore:cal/005_same_tick_chord
```

This fires:

- Bass G1
- Guitar G2
- Bass G2
- Banjo G3
- Basedrum state 0

Record whether all five are audible and whether the onset sounds acceptably simultaneous.

## Reporting back

The most useful report is simply:

```text
CAL-003: pass/fail + what you heard
CAL-004 1t: pass/fail + what you heard
CAL-004 2t: pass/fail + what you heard
CAL-005: pass/fail + what you heard
```

A short video is even more useful if something behaves unexpectedly.
