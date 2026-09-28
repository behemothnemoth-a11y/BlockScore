# Mars TEST-001A Backend Comparison — Batch 04

## Scope

All three backends compile the same:

```text
fixtures/mars/master-events-m001-m008.yaml
```

Master event count:

```text
349
```

No backend is allowed to change the arrangement in this comparison.

## Timing at the 132-QPM benchmark

| Backend | Grid | RMS error | Weighted RMS | Mean abs. | Max abs. | Sequence collapses |
|---|---:|---:|---:|---:|---:|---:|
| Command Rail Physical | 20 TPS | 14.166 ms | 14.171 ms | 12.117 ms | 24.242 ms | 0 |
| Digital Playback | 20 TPS | 14.166 ms | 14.171 ms | 12.117 ms | 24.242 ms | 0 |
| Redstone Physical | 10 Hz | 28.430 ms | 28.458 ms | 24.268 ms | 48.485 ms | 0 |

Command Rail and Digital share the same timing grid in this test. Their musical timing metrics are therefore identical before physical-driver/runtime effects.

## Physical note-block count

```text
REDSTONE_PHYSICAL:
349 note blocks

COMMAND_RAIL_PHYSICAL:
16 reusable note-block endpoints
```

Command Rail reduces permanent note-block count by approximately:

```text
95.42%
```

Physical reuse ratio:

```text
349 / 16 = 21.8125:1
```

This is physical compression only. The 349 Master attacks remain musically present.

## Command Rail endpoint result

```text
endpoint keys: 15
physical endpoints: 16
largest pool: 2
largest pool key: Bass G2
```

Bass G2 requires two endpoints because Theme A and the G2 ostinato attack simultaneously at the m.3 and m.8 entries.

All other current endpoint keys need only one physical block under the provisional two-game-tick busy window.

## Command Rail rail size

Candidate `SINGLE_LINE` bank:

```text
X span: 22 blocks including six one-block instrument gaps
physical note blocks: 16
maximum listener distance from chosen performance origin: 13.20 blocks
```

This is comfortably inside the current practical audible-distance planning envelope.

The result is still not `GAME_TESTED`: CAL-003 through CAL-006 remain required.

## Redstone DUAL result

Canonical source-tempo candidate:

```text
132 QPM
weighted RMS error: 28.458 ms
```

The informational ±10% tempo search found:

```text
120.059 QPM
weighted RMS error: 22.892 ms
tempo deviation: -9.046%
```

That candidate is **not automatically selected**.

It gains timing-grid fit by slowing the benchmark by roughly nine percent, which is a musical decision rather than a backend implementation detail.

The exact-grid sanity point remains:

```text
100 QPM
```

but is not an arrangement recommendation.

## Redstone physical-layout status

Redstone timing compilation is complete enough to provide:

```text
64 timing nodes
349 event-per-occurrence note cells
maximum simultaneous onset: 10 events
minimum timing-trunk repeater lower bound: 75
```

However, a genuine physical geometry pass is still required before claiming:

- final repeater count
- redstone-dust count
- branch compensation count
- exact footprint
- signal-strength validity
- cross-trigger validity

Those values are intentionally not invented in Batch 04.

## Digital result

Digital Playback generates:

```text
349 /playsound event commands
64 active musical game ticks
maximum commands on one musical tick: 10
```

No explicit `/stopsound` note-off commands are generated.

Theme A uses the Master candidate's `NATURAL_DECAY` strategy.

## Shared unresolved sustain issue

The Master contains 16 tam-tam events with:

```text
TREMOLO
```

but no tremolo subdivision rate has been approved.

Batch 04 therefore compiles each event's **start attack** and reports:

```text
TAM_TAM_TREMOLO_RATE_UNSPECIFIED
```

instead of inventing extra notes.

This is the largest reason none of the backend packages should yet be considered a finished listening version.

## Current result

For the exact same 349-event Master:

- Command Rail keeps the 20 TPS timing quality of Digital Playback while using real note blocks.
- Command Rail needs only 16 reusable note blocks for the current attack vocabulary.
- Standard redstone requires 349 note cells before routing hardware.
- Standard redstone approximately doubles RMS onset error at the current benchmark tempo.
- Redstone can improve grid fit by changing tempo, but the useful near-source candidate requires a significant slowdown.
- Digital is the clean timing reference but has no physical-instrument requirement.

This is the first data-backed comparison of the three BlockScore backends.
