# BlockScore Instruments v0.5 — Static Articulation Batch

This batch expands the physical guitar vocabulary while preserving the existing
100 TPS Command Rail contract.

## New physical blocks

### Clean / general guitar
- `blockscore:guitar_steel_clean_low_note_block`
- `blockscore:guitar_steel_clean_high_note_block`

### Distorted guitar
- `blockscore:guitar_distorted_low_note_block`
- `blockscore:guitar_distorted_high_note_block`

### Palm mute
- `blockscore:guitar_palm_mute_low_note_block`
- `blockscore:guitar_palm_mute_high_note_block`
- `blockscore:guitar_palm_mute_ghost_low_note_block`
- `blockscore:guitar_palm_mute_ghost_high_note_block`

### Harmonics
- `blockscore:guitar_artificial_harmonic_note_block`
- `blockscore:guitar_pinch_harmonic_note_block`

### Guitar percussion
- `blockscore:guitar_acoustic_body_hit_block`

## Ranges

LOW pitched blocks: E2-E4  
HIGH pitched blocks: G3-G5  
Artificial harmonic: F#3-F#5  
Pinch harmonic: F#4-F#6

Body hit uses the established register convention:

- note 0 -> LOW
- note 12 -> MID
- note 24 -> HIGH

## Source/audio status

The v0.5 banks are **first-pass audition banks** derived from the existing
CC0 SpeedY guitar recordings already used by BlockScore.

- Steel Clean: brightened real picked-guitar samples; prototype timbre.
- Distorted: amp-style processed real picked-guitar samples; prototype timbre.
- Palm Mute: damped/amp-processed real picked-guitar samples; prototype timbre.
- Artificial Harmonic: accepted harmonic bodies plus a picked transient.
- Pinch Harmonic: octave-up saturated harmonic derivation.
- Acoustic Body Hit: guitar-attack-derived wood/percussion synthesis.

The Java/block/compiler contracts are intended to remain stable even if any
sample bank is replaced after listening tests.

## Deliberately still separate

Slides, hammer-ons/pull-offs, bends and vibrato are not implemented as ordinary
static note blocks in v0.5. They require transition/articulation logic.
