# BlockScore Instruments — Fabric 26.2 Prototype

This module is the first runnable BlockScore custom-instrument implementation.

## Implemented

```text
blockscore:guitar_natural_harmonic_note_block
```

State:

```text
note=0..24
powered=true|false
```

Behavior:

- right-click with an empty hand advances the note
- left-click plays the current note
- a redstone rising edge plays the current note
- sustained power does not retrigger
- a falling edge resets the powered state
- air is required above the block
- no block entity
- no `/playsound` Command Rail substitution
- seven multisample roots: 0, 4, 8, 12, 16, 20, 24

## Requirements

- Minecraft Java 26.2
- Java 25
- Fabric Loader 0.19.5+
- Fabric API 0.161.0+26.2

## Build

From this directory:

```text
gradle build
```

The repository GitHub Action also builds this module with Java 25 and Gradle 9.7.1.

## In-game smoke test

Install the resulting JAR plus Fabric API.

Give yourself the block:

```text
/give @s blockscore:guitar_natural_harmonic_note_block
```

Place it with air above it.

1. Empty-hand right click: pitch advances and plays.
2. Left click: current pitch plays.
3. Put a lever beside it.
4. Lever OFF → ON: one attack.
5. Leave lever ON: no repeated attack.
6. Lever ON → OFF: no attack.
7. Lever OFF → ON again: same pitch attacks again.

## Command Rail test

Use it anywhere the existing Command Rail bank would normally use a vanilla note block.

The controller should continue toggling an adjacent redstone driver. It should not need to know how the custom block chooses its sample.

## Current audio quality

The included seven OGG files are procedural prototypes so the code can be tested immediately.

Once mechanics pass, the next step is replacing those files with real guitar natural-harmonic multisamples and then recompiling Crow.
