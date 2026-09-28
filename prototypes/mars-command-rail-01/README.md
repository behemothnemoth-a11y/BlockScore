# Mars Command Rail Prototype 01

## Target

Minecraft Java Edition **26.2**.

This is BlockScore's first executable Command Rail prototype for Mars TEST-001A, measures 1–8.

The datapack is configured for Data Pack version **107.1**.

## What this prototype does

- places the 16-endpoint Batch 04 physical note bank
- preserves the exact endpoint tuning/support materials from the compiled plan
- stores a physical bank anchor with a `minecraft:marker`
- plays the 349-attack Batch 04 Command Rail schedule at the 132-QPM benchmark
- uses real redstone-block power transitions beside real note blocks
- contains no `/playsound` commands for normal song attacks
- provides CAL-003, CAL-004, and CAL-005 listening tests

## What this prototype does NOT claim yet

It is not `GAME_TESTED`.

The following remain provisional:

- whether the command-created redstone-block transition reliably triggers the physical note in Java 26.2
- whether one-game-tick same-endpoint retrigger works
- whether the current conservative two-game-tick busy window is necessary
- whether dense same-tick endpoint activation is perceptually simultaneous
- weathered-trumpet register calibration
- waxed-copper equivalence
- tam-tam tremolo rate
- Theme A sustain quality

## Install the datapack

Copy the folder:

```text
BlockScore_Mars_CR_01
```

into:

```text
<world>/datapacks/
```

Then load/reload the world:

```text
/reload
```

You can confirm that Minecraft sees it with:

```text
/datapack list
```

## Place the bank

Stand on the block where you want the **first support block** of the rail.

Face direction does not currently matter; Prototype 01 always builds toward world +X (east).

Run:

```text
/function blockscore:install
```

The bank occupies roughly:

```text
X: 0 through 21 from the anchor
Y: anchor through anchor + 2
Z: anchor through anchor + 1
```

Use a clear area before installing.

## First calibration sequence

Run these before attempting the song.

### CAL-003 — physical driver

```text
/function blockscore:cal/003_driver
```

Expected by design:

- one real Bass G1 note
- caused by a temporary adjacent redstone block
- driver resets to air one game tick later

If it works:

```text
/function blockscore:cal/mark_003_pass
```

Otherwise:

```text
/function blockscore:cal/mark_003_fail
```

### CAL-004 — retrigger

One-game-tick candidate:

```text
/function blockscore:cal/004_retrigger_1tick
```

Listen for two Bass G1 attacks approximately 50 ms apart.

Record:

```text
/function blockscore:cal/mark_004_1tick_pass
```

or:

```text
/function blockscore:cal/mark_004_1tick_fail
```

Then test the current conservative two-tick assumption:

```text
/function blockscore:cal/004_retrigger_2tick
```

Listen for two attacks approximately 100 ms apart.

Record with:

```text
/function blockscore:cal/mark_004_2tick_pass
/function blockscore:cal/mark_004_2tick_fail
```

### CAL-005 — same-tick synchronization

```text
/function blockscore:cal/005_same_tick_chord
```

This triggers five ostinato layers from one function call.

Listen for:

- missing notes
- obvious smear
- unexpected double triggers

Record:

```text
/function blockscore:cal/mark_005_pass
```

or:

```text
/function blockscore:cal/mark_005_fail
```

## View recorded calibration status

```text
/function blockscore:cal/status
```

Scores:

```text
1  = pass
0  = not recorded
-1 = fail
```

## Play Mars TEST-001A

After CAL-003 works:

```text
/function blockscore:control/start
```

Controls:

```text
/function blockscore:control/pause
/function blockscore:control/resume
/function blockscore:control/stop
/function blockscore:control/reset
```

The song controller:

- dispatches before incrementing the song tick
- starts at song tick 0
- performs the final driver reset on tick 356
- stops after that reset has run

## Command-block controls

If you want physical buttons, place ordinary impulse command blocks and put one of these commands in each:

```text
function blockscore:control/start
function blockscore:control/pause
function blockscore:control/resume
function blockscore:control/stop
function blockscore:control/reset
```

No special command-block NBT is required by the datapack itself.

## Remove prototype

```text
/function blockscore:uninstall
```

This clears only the known endpoint/support/driver cells and removes the anchor marker.

## Important weathered-copper note

The Horn Color endpoints currently use **unwaxed weathered copper**, because CAL-002 has not yet verified waxed-copper instrument equivalence.

For a short test this is acceptable.

Do not treat this as the final permanent-bank material policy.

## Files

The datapack source is kept unpacked in this prototype directory so the repository remains reviewable.

The standalone datapack ZIP supplied with Batch 05 contains the same pack ready to place in a world's `datapacks` folder.
