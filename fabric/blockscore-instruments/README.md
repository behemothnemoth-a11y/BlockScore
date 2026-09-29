# BlockScore Instruments — Fabric 26.2 v0.3

Physical custom guitar-articulation note blocks for BlockScore.

## Current blocks

```text
blockscore:guitar_natural_harmonic_note_block
blockscore:guitar_tapped_harmonic_note_block
blockscore:guitar_dead_note_block
```

Natural and tapped harmonics retain the accepted v0.2 multisample implementation.

### Dead-note semantics in v0.3

`guitar_dead_note_block` is **not chromatic**.

Its note state selects a percussion register:

```text
0..7   LOW
8..16  MID
17..24 HIGH
```

BlockScore-generated Crow v3 banks use the canonical states:

```text
LOW  = 0
MID  = 12
HIGH = 24
```

Each register randomly selects between two real-string-derived transient variants, and the Java block always plays them at pitch `1.0`.

The physical contract remains unchanged:

```text
note=0..24
powered=true|false
```

so the proven Command Rail redstone driver continues to work without modification.

## Requirements

- Minecraft Java 26.2
- Java 25
- Fabric Loader 0.19.5+
- Fabric API 0.161.0+26.2
