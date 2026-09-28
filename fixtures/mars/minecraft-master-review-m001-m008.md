# Mars TEST-001A — Minecraft Master Candidate A

## Purpose

This is the first complete Minecraft Master candidate for source measures 1–8.

It is **not user-locked yet**.

The candidate is intentionally backend-neutral: no game ticks, redstone ticks, physical lanes, or Command Rail endpoints are assigned.

## Ostinato

The source ostinato contains many exact octave doublings.

Candidate A preserves the three sounding octaves while reducing redundant source doublings into five functional Minecraft layers:

| Master voice | Minecraft sound | Pitch | Purpose |
|---|---|---:|---|
| OSTINATO_LOW_G1 | Bass | G1 | low foundation |
| OSTINATO_HARP_G2 | Guitar | G2 | plucked harp-color middle octave |
| OSTINATO_CELLO_G2 | Bass | G2 | lower-string body |
| OSTINATO_COL_LEGNO_G3 | Banjo | G3 | woody upper col-legno approximation |
| OSTINATO_TIMPANI_ATTACK | Basedrum | state 0 | timpani attack function |

All five voices use the exact locked ostinato attack positions.

The timpani's own Minecraft percussion event does not claim a definite G2 pitch. The simultaneous G2 tonal layers prevent the ostinato's G2 pitch identity from disappearing.

## Harps

Minecraft's Harp instrument cannot reach the source G1/G2 registers.

Candidate A therefore preserves the **actual source pitches** rather than moving the harps upward merely to retain the word "harp":

- lower harp octave contributes to Bass G1
- upper harp octave becomes Guitar G2

This is an explicit timbre substitution, not a hidden octave shift.

## Col legno strings

Violins I, Violins II, and Violas all carry the same G3 ostinato.

Candidate A merges those identical doublings and uses Banjo G3 as the upper attack.

The reason is envelope, not name: the banjo's short plucked/wooden character is a better first approximation of col legno than a sustained or metallic voice.

The cello G2 remains separate as Bass G2.

## Theme A

The low theme is preserved at exact concert pitch:

| Source function | Minecraft voice |
|---|---|
| Contrabassoon G1/D2/Db2 | Didgeridoo |
| Bassoons I-II G2/D3/Db3 | Bass |
| Horns V-VI G2/D3/Db3 | Weathered Trumpet |
| Bassoon III + Bass Oboe Db3 reinforcement | Didgeridoo Db3 |

The weathered trumpet is deliberately **not** the sole carrier of Theme A.

Bass and didgeridoo already carry the P5 pitch contour. Therefore a later CAL-001 correction cannot erase the theme; it would require re-orchestrating the horn-color layer.

## Theme sustain

Candidate A starts with:

```text
NATURAL_DECAY
```

for Theme A.

That is a conscious conservative choice.

Retriggering an 8-QN orchestral tone could preserve duration better but would introduce a new pulse against the ostinato. We will audition natural decay first, then compare controlled retrigger candidates.

This is recorded as a high-severity sustain approximation, not hidden.

## Tam-tam

The tam-tam remains the least settled voice.

Candidate A uses:

```text
snare
note_state 0
TREMOLO
```

as the first physical-note-block noise candidate.

This is explicitly user-review-required and source-review-dependent.

## Source accounting

The expanded source fixture contains:

```text
550 source events
```

Candidate A contains:

```text
349 master events
```

The reduction is from documented voice merging, not deletion.

Every one of the 550 source event IDs is referenced exactly once by a Master event.

```text
source events removed: 0
P5 source events removed: 0
silent source disappearance: 0
```

## Calibration dependency

Candidate A uses:

```text
trumpet_weathered
```

for Horns V-VI.

Therefore:

```text
CAL-001
CAL-002
```

remain dependencies.

The rest of the P5 pitch structure uses established instruments.

## Status

```text
ARRANGED_DRAFT
USER APPROVAL: PENDING
LOCKED: NO
BACKEND COMPILATION: NOT YET
```

Next, compile this exact candidate into Command Rail, Physical Redstone, and Digital Playback without changing the Master.
