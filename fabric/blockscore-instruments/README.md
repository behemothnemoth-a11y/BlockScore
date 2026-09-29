# BlockScore Instruments — Fabric 26.2

Version 0.2 expands the proven custom physical note-block architecture to the three guitar articulations needed for the Crow acceptance test.

## Blocks

```text
blockscore:guitar_natural_harmonic_note_block
blockscore:guitar_tapped_harmonic_note_block
blockscore:guitar_dead_note_block
```

Each block uses:

```text
note=0..24
powered=true|false
```

and works with ordinary redstone rising edges and the existing BlockScore Command Rail endpoint driver.

## Multisample roots

```text
0, 3, 8, 13, 17, 22, 24
```

The harmonic blocks cover F#3–F#5.

The dead-note block covers F#2–F#4.

## Audio

The v0.2 samples are derived from SpeedY's CC0 `Nylon Guitar Single notes` Freesound pack.

See `THIRD_PARTY_AUDIO.md`.

## Build

```text
gradle build
```

Requirements:

- Minecraft Java 26.2
- Java 25
- Fabric Loader 0.19.5+
- Fabric API 0.161.0+26.2

## Smoke test

```text
/give @s blockscore:guitar_natural_harmonic_note_block
/give @s blockscore:guitar_tapped_harmonic_note_block
/give @s blockscore:guitar_dead_note_block
```

For each block:

1. keep air above it
2. right click to tune/play
3. left click to play current state
4. test lever OFF→ON
5. confirm held power does not repeat
6. confirm OFF→ON retriggers

## Crow

Crow is the first full musical acceptance test for this version.

The song datapack should use the same 100 TPS Command Rail controller that already passed Rush E.
