# BlockScore Mars Benchmark

## TEST-001A — Opening Measures 1–8

This fixture is the first real-music benchmark for BlockScore.

Piece:

- **Gustav Holst — Mars, the Bringer of War**
- First movement of *The Planets*, Op. 32
- Benchmark scope: measures 1–8
- Target Minecraft profile: Java 26.2

## Source Policy

Primary source family:

- Holst's published score and the public-domain 1924 Pay/Smith wind-band arrangement.
- IMSLP identifies the Pay/Smith condensed score as item `#1038645`, Boosey & Co. plate H.11069, published 1924, and Public Domain.
- The original orchestral score is used as a structural cross-reference.

Primary index:

https://imslp.org/wiki/The_Planets_Op.32_(Holst,_Gustav)

Analytical cross-checks used for this first fixture:

https://theplanetsonline.com/pages/musiccomp.html

https://athensdriveband.com/doc-talk-class-lesson-5-18-2020/

## What Is Locked in Batch 01

The first batch deliberately locks only source facts we can support confidently:

- meter: `5/4`
- working grouping: `3 + 2`
- opening ostinato pitch class: `G`
- ostinato rhythm:
  - triplet eighths occupying beat 1
  - quarter on beat 2
  - quarter on beat 3
  - two eighths on beat 4
  - quarter on beat 5
- exact ostinato attack offsets in quarter-note units:
  - `0`
  - `1/3`
  - `2/3`
  - `1`
  - `2`
  - `3`
  - `7/2`
  - `4`
- the first two bars begin with the ostinato texture before the first melodic fragment enters
- first melodic fragment contour:
  - `G`
  - up a perfect fifth to `D`
  - down a semitone to `Db/C#`
- the first melodic fragment spans four measures structurally

## What Is Not Yet Locked

Batch 01 does **not** pretend the complete orchestration of measures 1–8 has been transcribed.

Still pending:

- exact absolute register for every opening source voice
- exact duration/tie structure of every Theme A note
- exact source instrumentation for every individual event in measures 1–8
- dynamics at event-level resolution
- all doubling relationships
- final Minecraft instrument mapping
- final Minecraft Master events

These remain `SOURCE_TRANSCRIPTION_PENDING`.

## Benchmark Tempo

The source score is marked **Allegro**.

For deterministic timing tests, Batch 01 uses:

```text
working_qpm = 132
```

This is a **benchmark test value**, not a claim that the primary source prints quarter note = 132.

The fixture must preserve that distinction.

## Why Measures 1–8

This section is already enough to test important BlockScore behavior:

- quintuple meter
- additive grouping
- triplets against duple subdivisions
- repeated P5 rhythmic material
- absolute-time quantization
- game-tick versus redstone-tick loss
- endpoint reuse
- a low melodic entry over the ostinato
- onset-group preservation

## P5 Requirements

The following are identity-critical:

- 5/4 meter
- ostinato attack pattern
- ostinato cycle phase
- meter-defining accents
- pedal/low-pulse identity
- first-theme interval contour

No backend may silently simplify these.

## Batch 01 Status

```text
SOURCE AUDIT: PARTIAL_LOCK
OSTINATO: LOCKED
THEME_A_CONTOUR: LOCKED
FULL M1–8 TRANSCRIPTION: PENDING
MINECRAFT MASTER: NOT YET LOCKED
BACKEND COMPILES: TEST VECTORS ONLY
```

The purpose of Batch 01 is to prove that BlockScore's infrastructure can represent and test real musical structure before committing to the full event transcription.
