# BlockScore Custom Instruments

## Status

**Batch 03 / v0.2:** the custom physical guitar articulation layer now contains three blocks:

```text
blockscore:guitar_natural_harmonic_note_block
blockscore:guitar_tapped_harmonic_note_block
blockscore:guitar_dead_note_block
```

All three retain the proven BlockScore physical contract:

```text
note = 0..24
powered = true|false
```

They are driven by the same rising-edge redstone behavior used by Command Rail.

## Why Crow changed the plan

Jinsan Kim — *Crow* was used as the acceptance source.

The GPX explicitly contains:

- natural harmonics
- tapped harmonics
- a very large number of muted/dead-string attacks

Fixing only natural harmonics would leave a major part of the guitar language represented by unrelated vanilla percussion. Batch 03 therefore implements the smallest articulation set that gives Crow a meaningful test.

## Multisample roots

The original synthetic prototype used evenly spaced roots.

The real CC0 guitar recordings support a better root layout:

```text
0, 3, 8, 13, 17, 22, 24
```

This corresponds to source/target roots near:

```text
F#3, A3, D4, G4, B4, E5, F#5
```

for harmonic blocks, and one octave lower for the dead-note block.

The largest residual per-note pitch shift remains two semitones.

## Physical behavior

Every custom block:

1. exposes `note=0..24`
2. exposes `powered=true|false`
3. plays once on OFF→ON redstone edge
4. does not repeat while held powered
5. resets on ON→OFF
6. retriggers normally on a later rising edge
7. tunes on empty-hand right click
8. requires air above
9. uses no block entity
10. produces physical in-world sound rather than `/playsound`

## Audio source

Batch 03 replaces the synthetic natural-harmonic bank with derived samples from SpeedY's Freesound pack **Nylon Guitar Single notes** (pack 469), supplied under **Creative Commons Zero / CC0**.

The tapped-harmonic bank uses the CC0 natural-harmonic body with a short CC0 picked-string transient to create a sharper tapped attack.

The dead-note bank is derived from short damped transients of the same CC0 picked-string recordings.

See:

```text
fabric/blockscore-instruments/THIRD_PARTY_AUDIO.md
```

## Crow acceptance test

Crow should compile with:

- ordinary notes → vanilla guitar
- natural harmonic → custom natural-harmonic block
- tapped harmonic → custom tapped-harmonic block
- muted/dead string → custom dead-note block
- percussion → vanilla note-block percussion

The 100 TPS Command Rail controller remains unchanged.

## Governing rule

> Improve the instrument vocabulary without rewriting the playback engine that already works.


---

# Dead/Muted Strings — v0.3 rule

A GPX `Muted`/dead-string note is not treated as a chromatic pitch.

BlockScore preserves the source **string register**:

```text
GPX string 0-1 -> LOW  -> note_state 0
GPX string 2-3 -> MID  -> note_state 12
GPX string 4-5 -> HIGH -> note_state 24
```

The custom block does not pitch-shift these samples. `note` is retained as a Command Rail-compatible block property and register selector.

This is intentionally distinct from **palm mute**, which remains a future pitched articulation.
