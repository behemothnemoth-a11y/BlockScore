# BlockScore Timing Model

## Minecraft Java Edition 26.2

This document defines how BlockScore represents musical time and compiles that time into Minecraft playback systems.

Timing is one of the core architectural components of BlockScore.

The governing rule is:

> Preserve exact musical relationships first. Quantize only when compiling a specific playback backend.

BlockScore must never allow backend timing limitations to contaminate Source Score timing.

---

# 1. Timing Layers

BlockScore uses four timing layers:

```text
NOTATED TIME
     ↓
PERFORMANCE TIME
     ↓
ABSOLUTE MASTER TIME
     ↓
BACKEND TIME
```

These layers have different purposes.

---

# 2. Notated Time

Notated Time describes where an event exists musically.

Example:

```yaml
measure: 14
beat: 3
offset: 2/3
```

This should remain an exact rational musical position.

Do not immediately reduce it to:

```text
7.483 seconds
```

or:

```text
149 game ticks
```

Notated Time is independent of Minecraft.

---

# 3. Performance Time

Performance Time represents deliberate deviations from literal notation.

Examples include:

- swing
- rubato
- fermata
- pushed or delayed accents
- humanized timing
- intentional laid-back groove
- tempo ramps

For mechanically precise music, Notated Time and Performance Time may be identical.

For expressive music they may differ.

Minecraft backend limitations do not belong in Performance Time.

---

# 4. Absolute Master Time

Absolute Master Time converts the musical timeline into elapsed time from the beginning of the song.

Canonical unit:

```text
seconds
```

Internally, implementations should retain sufficient numeric precision to avoid cumulative error.

Where possible, exact rational musical values should be retained until tempo integration requires floating-point calculations.

Absolute Master Time is the timing authority used by all backends.

---

# 5. Backend Time

Each backend translates Absolute Master Time into its own legal timing grid.

Current backend clocks:

```text
COMMAND_RAIL_PHYSICAL
20 Hz game-tick grid

COMMAND_RAIL_ENHANCED
20 Hz game-tick grid

DIGITAL_PLAYBACK
20 Hz game-tick grid

REDSTONE_PHYSICAL
10 Hz default redstone-tick grid
```

Future advanced backends may introduce other timing capabilities.

They must still compile from Absolute Master Time.

---

# 6. Minecraft Game Tick

BlockScore uses the standard Minecraft target:

```text
20 game ticks per second
```

Therefore:

```text
1 game tick = 0.05 seconds
```

or:

```text
50 milliseconds
```

Canonical constants:

```text
GAME_TICKS_PER_SECOND = 20

SECONDS_PER_GAME_TICK = 0.05
```

---

# 7. Redstone Tick

A normal redstone repeater delay unit is:

```text
1 redstone tick
=
2 game ticks
=
0.1 seconds
```

Therefore:

```text
REDSTONE_TICKS_PER_SECOND = 10

GAME_TICKS_PER_REDSTONE_TICK = 2

SECONDS_PER_REDSTONE_TICK = 0.1
```

The standard BlockScore Redstone Physical backend uses this 10 Hz timing grid.

---

# 8. Repeater Delays

A normal repeater can be configured to:

```text
1 redstone tick

2 redstone ticks

3 redstone ticks

4 redstone ticks
```

Equivalent delays:

```text
100 ms

200 ms

300 ms

400 ms
```

Longer delays are created by chaining repeaters.

Example:

```text
4-tick repeater
+
3-tick repeater
=
7 redstone ticks
=
700 ms
```

---

# 9. Redstone Delay Is Not Distance

BlockScore must not model redstone-wire distance as musical delay.

Wire routing and musical timing are separate concerns.

Repeater insertion, however, creates real delay.

Therefore physical routing must account for every repeater added for:

- timing
- signal restoration
- direction control
- branch isolation
- other circuitry

If one chord branch requires an extra repeater for routing, other branches must compensate if simultaneous arrival is required.

---

# 10. Canonical Musical Unit

Internally, BlockScore should use:

```text
quarter-note units
```

abbreviated:

```text
QN
```

Examples:

```text
quarter note = 1 QN

eighth note = 1/2 QN

sixteenth note = 1/4 QN

half note = 2 QN

whole note = 4 QN
```

Triplet eighth:

```text
1/3 QN
```

Quintuplet subdivision across one quarter:

```text
1/5 QN
```

This makes mixed meter and tuplets straightforward.

---

# 11. Rational Musical Positions

Musical offsets should use rational numbers whenever possible.

Preferred:

```text
1/3

2/3

3/8

7/16
```

Avoid storing these as rounded decimals such as:

```text
0.333333

0.666667
```

until a calculation actually requires floating-point representation.

---

# 12. Measure Length

For a meter:

```text
numerator / denominator
```

measure length in quarter-note units is:

```text
measure_qn =
numerator * (4 / denominator)
```

Examples:

```text
4/4
4 QN

5/4
5 QN

7/8
3.5 QN

6/8
3 QN

12/8
6 QN
```

---

# 13. Meter Grouping

Meter length and meter grouping are separate.

Example:

```yaml
meter: 7/8
grouping:
  - 2
  - 2
  - 3
```

is not treated as musically identical to:

```yaml
meter: 7/8
grouping:
  - 3
  - 2
  - 2
```

The total length is identical.

The accent structure is not.

Grouping metadata is used by the rhythm-preservation solver.

---

# 14. Absolute Musical Position

Each event should eventually receive:

```text
absolute_qn
```

representing its total musical position from the beginning of the song.

Example:

```yaml
measure: 12
offset_qn: 7/3
absolute_qn: 163/3
```

Once calculated, backend timing does not need to walk sequentially through previous events.

This is critical to preventing drift.

---

# 15. Tempo Representation

A tempo event should contain:

```yaml
position_qn:
bpm:
beat_unit:
transition:
```

Example:

```yaml
position_qn: 0
bpm: 120
beat_unit: quarter
transition: STEP
```

BlockScore must preserve the actual beat unit specified by the source.

---

# 16. Tempo Beat Units

Examples:

```text
quarter
eighth
half
dotted_quarter
dotted_eighth
```

Each beat unit is converted to quarter-note units.

Examples:

```text
quarter
1 QN

eighth
1/2 QN

half
2 QN

dotted quarter
3/2 QN

dotted eighth
3/4 QN
```

---

# 17. Normalized Quarter Tempo

BlockScore normalizes tempo to:

```text
quarter notes per minute
```

abbreviated:

```text
QPM
```

Formula:

```text
QPM =
source BPM
*
beat_unit_length_in_QN
```

Example:

```text
dotted quarter = 90 BPM

beat unit = 1.5 QN

QPM = 90 * 1.5
QPM = 135
```

---

# 18. Constant Tempo Conversion

At constant QPM:

```text
seconds_per_QN = 60 / QPM
```

Elapsed time across:

```text
delta_QN
```

is:

```text
seconds =
delta_QN * 60 / QPM
```

---

# 19. Game Ticks Per Quarter

At constant quarter tempo:

```text
game_ticks_per_QN =
1200 / QPM
```

because:

```text
20 ticks/sec * 60 sec/min = 1200
```

Example:

```text
QPM = 120

game ticks per quarter = 10
```

---

# 20. Redstone Ticks Per Quarter

At constant quarter tempo:

```text
redstone_ticks_per_QN =
600 / QPM
```

because:

```text
10 redstone ticks/sec * 60 sec/min = 600
```

Example:

```text
QPM = 120

redstone ticks per quarter = 5
```

---

# 21. Subdivision Timing

For a subdivision containing:

```text
N equal attacks per quarter note
```

game-tick spacing is:

```text
1200 / (QPM * N)
```

redstone-tick spacing is:

```text
600 / (QPM * N)
```

Example:

```text
QPM = 150
sixteenth notes
N = 4
```

Game ticks:

```text
1200 / (150 * 4)
=
2
```

Redstone ticks:

```text
600 / (150 * 4)
=
1
```

Therefore sixteenth notes are grid-exact in both standard Minecraft timing systems at 150 QPM.

---

# 22. Backend Grid Exactness

A rhythm is:

```text
GRID_EXACT
```

when all required event positions map to integers on the target backend grid.

Example:

```text
ideal game tick = 28
```

is exact.

Example:

```text
ideal game tick = 28.5
```

requires quantization for a normal 20 TPS backend.

---

# 23. Absolute Quantization

BlockScore quantizes each event from Absolute Master Time.

Correct:

```text
master event A → backend grid

master event B → backend grid

master event C → backend grid
```

Incorrect:

```text
quantized A
    ↓
calculate B from A
    ↓
quantize B
    ↓
calculate C from B
```

The incorrect method accumulates error.

BlockScore forbids it.

---

# 24. Game-Tick Ideal Position

For an event at:

```text
master_seconds
```

ideal game-tick position is:

```text
ideal_game_tick =
master_seconds * 20
```

This value may not be an integer.

Example:

```text
master_seconds = 6.375

ideal_game_tick = 127.5
```

---

# 25. Redstone-Tick Ideal Position

For Redstone Physical:

```text
ideal_redstone_tick =
master_seconds * 10
```

Example:

```text
master_seconds = 6.35

ideal_redstone_tick = 63.5
```

---

# 26. Compiled Position

A legal backend position is an integer backend tick.

Example:

```text
ideal = 63.5

legal candidates:
63
64
```

The timing solver decides which candidate best preserves the music.

Do not simply round every event independently when doing so would damage an important rhythmic relationship.

---

# 27. Onset Groups

Events that are simultaneous in the Minecraft Master belong to the same:

```text
ONSET_GROUP
```

Example:

```text
E4 trumpet

G4 trumpet

B4 harp

kick
```

at the same Master position belong to one onset group.

An onset group is quantized as one timing object.

Its events must not independently land on different backend ticks unless the arrangement explicitly requests a spread.

---

# 28. Chord Spread

For normal simultaneous events:

```text
CHORD_SPREAD = 0 backend ticks
```

If physical routing creates:

```text
E4 at tick 100

G4 at tick 101

B4 at tick 100
```

the backend has introduced a timing defect.

The routing compiler must compensate.

---

# 29. Timing Error

For each onset:

```text
signed_error_seconds =
compiled_time_seconds
-
ideal_time_seconds
```

and:

```text
absolute_error_seconds =
abs(signed_error_seconds)
```

Milliseconds:

```text
signed_error_ms =
signed_error_seconds * 1000
```

---

# 30. Game-Tick Quantization Error

At 20 TPS, nearest-grid quantization can create up to approximately:

```text
25 ms
```

of absolute onset error when nearest rounding is possible.

This does not mean every 25 ms error is musically acceptable.

Musical context matters.

---

# 31. Redstone Quantization Error

At 10 Hz redstone timing, nearest-grid quantization can create up to approximately:

```text
50 ms
```

of absolute onset error.

Again, musical significance depends on context.

A 50 ms displacement of a background doubling may be insignificant.

A 50 ms displacement of an identity-critical syncopation may not be.

---

# 32. Priority Weighting

Timing optimization uses event priority.

Initial solver weights:

```text
P1 = 1

P2 = 2

P3 = 4

P4 = 8

P5 = 16
```

These are BlockScore optimization weights.

They are not physical Minecraft constants.

Future benchmark testing may adjust them.

---

# 33. Rhythmic Function Weighting

Priority alone is insufficient.

Events may receive additional rhythmic roles:

```text
DOWNBEAT

METER_ACCENT

RIFF_ANCHOR

SYNCOPATION

BACKBEAT

POLYRHYTHM_ANCHOR

PHRASE_BOUNDARY

DECORATIVE
```

Identity-defining rhythmic roles may increase solver weight.

---

# 34. Inter-Onset Interval

For two consecutive events in the same voice:

```text
IOI =
time_B - time_A
```

where IOI means:

```text
inter-onset interval
```

BlockScore calculates both:

```text
ideal_IOI

compiled_IOI
```

and:

```text
IOI_error =
compiled_IOI - ideal_IOI
```

This helps detect groove damage that individual event error alone may hide.

---

# 35. Why IOI Matters

Consider:

```text
event A error = +25 ms

event B error = -25 ms
```

Each event individually appears close.

But the interval between them has changed by:

```text
50 ms
```

That may significantly change a fast groove.

Therefore timing QA must analyze both:

```text
absolute onset error
```

and:

```text
interval distortion
```

---

# 36. Sequence Collapse

Two distinct source attacks may quantize to the same backend tick.

Example:

```text
source:
tick ideal 40.2
tick ideal 40.7

compiled:
40
40
```

This creates:

```text
SEQUENCE_COLLAPSE
```

The original rhythm contained two attacks.

The backend now contains one timing position.

This must never be treated as lossless.

---

# 37. Sequence Collapse Resolution

Possible solutions include:

```text
choose different neighboring ticks

slightly alter local timing

slightly alter tempo

use a higher-resolution backend

redesign rhythmic approximation

report unrepresentable passage
```

P5 sequence collapse requires explicit review.

---

# 38. Ordering Rule

Quantization must never reverse musical event order.

If:

```text
A occurs before B
```

then compiled timing must satisfy:

```text
compiled_A <= compiled_B
```

If equality occurs for originally separate attacks:

```text
SEQUENCE_COLLAPSE
```

must be reported.

---

# 39. Tuplets

Tuplets remain rational in Master timing.

Examples:

Triplet:

```text
1/3 QN
```

Quintuplet:

```text
1/5 QN
```

Septuplet:

```text
1/7 QN
```

No backend approximation is applied until compilation.

---

# 40. Tuplet Example

At:

```text
QPM = 120
```

one quarter lasts:

```text
10 game ticks
```

A triplet subdivision lasts:

```text
10 / 3
=
3.333333... game ticks
```

Therefore ordinary 20 TPS playback cannot make every triplet subdivision exact at 120 QPM.

BlockScore preserves the exact triplet in the Master and reports the backend approximation.

---

# 41. Tuplet Distribution

Do not convert a three-note triplet by repeatedly rounding:

```text
3
3
3 ticks
```

because the total becomes:

```text
9 ticks
```

instead of:

```text
10 ticks
```

A better absolute placement may become:

```text
0

3

7

10
```

relative game ticks.

This preserves the total beat duration while distributing the local error.

The exact selected pattern is determined by the rhythmic solver.

---

# 42. Error Distribution

For repeated non-grid-exact rhythms, BlockScore should prefer:

```text
distributed local error
```

over:

```text
cumulative drift
```

Example:

```text
3
4
3
```

may preserve a 10-tick triplet span better than:

```text
3
3
3
```

when the next beat must return to the correct anchor.

---

# 43. Anchor Points

Important timing locations should be marked:

```text
ANCHOR
```

Examples:

- measure start
- phrase start
- phrase end
- riff-cycle reset
- major downbeat
- tempo change
- loop boundary
- synchronization point

The solver should avoid moving an anchor when surrounding events can absorb the error instead.

---

# 44. Barline Phase Error

A barline may itself fall between backend ticks.

BlockScore records:

```text
BARLINE_PHASE_ERROR
```

This is different from cumulative drift.

If every event is compiled from absolute time, phase error does not automatically accumulate across measures.

---

# 45. Cumulative Drift

BlockScore defines:

```text
CUMULATIVE_DRIFT
```

as timing error introduced because compiled timing was derived from previous rounded timing instead of the authoritative Master.

Required target:

```text
CUMULATIVE_DRIFT = 0
```

for the timing compiler itself.

Individual quantization error is allowed.

Uncontrolled cumulative rounding drift is not.

---

# 46. Mixed Meter

All meters share one absolute QN timeline.

Example:

```text
measure 1:
5/4
length = 5 QN

measure 2:
7/8
length = 3.5 QN

measure 3:
3/4
length = 3 QN
```

The absolute timeline continues normally through each change.

Backend clocks do not care where meter changes occur.

Meter remains essential for musical analysis and accent preservation.

---

# 47. Polymeter

Different voices may have independent local meter interpretations while sharing the same absolute timeline.

Example:

```text
VOICE A:
4/4 phrasing

VOICE B:
7-eighth-note repeating cycle
```

Both are stored against common Absolute Master Time.

Do not force local cycles to reset at global barlines.

---

# 48. Riff Cycles

A riff receives its own cycle metadata.

Example:

```yaml
riff_id: RIFF_A
length_qn: 7/2
reset_policy: continuous
```

The timing solver uses riff boundaries as musical information.

They are not automatically equivalent to measure boundaries.

---

# 49. Polyrhythm

Independent rhythmic layers are compiled from the same master clock.

Example:

```text
Layer A:
3 attacks across one beat

Layer B:
2 attacks across one beat
```

Each layer receives exact rational positions before backend quantization.

Never derive one layer from the already-quantized timing of another layer.

---

# 50. Common Reset

Polyrhythmic material may define:

```text
COMMON_RESET
```

where all participating patterns realign.

Common Reset should normally receive anchor status.

This helps prevent backend approximation from gradually destroying phase relationships.

---

# 51. Swing

Swing is not represented only by a text label.

BlockScore should store an explicit ratio.

Example:

```text
2:1 swing
```

For an eighth-note pair spanning:

```text
1 QN
```

the attacks occur at:

```text
0

2/3 QN
```

rather than:

```text
0

1/2 QN
```

Other swing ratios are allowed.

---

# 52. Rubato

Rubato should be represented by timing transformations or tempo-map changes rather than arbitrary backend offsets.

Preferred:

```text
Master timing changes
```

rather than:

```text
move command by two ticks
```

unless the two-tick movement itself is an intentional backend compromise.

---

# 53. Microtiming

Performance timing may include:

```text
micro_offset_ms
```

for deliberate pushes or delays.

Example:

```yaml
event:
  notated_position_qn: 8
  micro_offset_ms: -18
```

Absolute Master Time incorporates the offset before backend compilation.

A backend may quantize the offset away.

If the microtiming is musically important, it should receive appropriate priority.

---

# 54. Tempo Changes

Tempo changes belong to the Master timing model.

Minimum supported transition types:

```text
STEP

LINEAR_QPM
```

Additional transition types may be added later.

---

# 55. Step Tempo Change

For:

```text
STEP
```

the previous tempo remains active until the exact change position.

The new QPM applies immediately afterward.

---

# 56. Linear Tempo Ramp

For:

```text
LINEAR_QPM
```

tempo varies linearly with musical position between two QPM values.

The wall-time conversion must integrate tempo across the segment rather than average the two endpoint tempos blindly.

For a full ramp of length:

```text
L QN
```

from:

```text
QPM_A
```

to:

```text
QPM_B
```

the exact elapsed time for a linear-QPM ramp is:

```text
seconds =
60 * L * ln(QPM_B / QPM_A)
/
(QPM_B - QPM_A)
```

when:

```text
QPM_A != QPM_B
```

If the two values are equal, use normal constant-tempo conversion.

---

# 57. Fermata

A fermata cannot always be inferred from normal tempo.

BlockScore may represent it as:

```text
explicit hold duration
```

Example:

```yaml
type: FERMATA
position_qn: 40
additional_seconds: 1.25
```

This becomes part of Master time before backend compilation.

---

# 58. Timing Modes

Each backend compilation selects a timing mode.

Available modes:

```text
EXACT

SOURCE_TEMPO

NEAR_EXACT

GROOVE_PRESERVE

REDSTONE_OPTIMIZED

DUAL
```

---

# 59. EXACT

Use when every required onset maps exactly to the backend timing grid.

No timing alteration is required.

Status:

```text
GRID_EXACT
```

---

# 60. SOURCE_TEMPO

Preserve original tempo exactly.

Quantize event timing as required.

Report all backend errors.

No tempo optimization is permitted.

---

# 61. NEAR_EXACT

Preserve source tempo.

Allow small event displacement where musical QA accepts the result.

No important rhythmic identity may be silently changed.

---

# 62. GROOVE_PRESERVE

When exact timing is impossible, prioritize:

- accent pattern
- inter-onset relationships
- riff identity
- backbeat
- important syncopations
- phrase anchors

over mathematically minimizing every independent event error.

This is especially useful for:

- swing
- tuplets
- groove-based rock
- complex repeated patterns

---

# 63. REDSTONE_OPTIMIZED

Permit a small deliberate tempo adjustment to create a cleaner physical timing grid.

Tempo change must be reported.

The optimizer searches near the source tempo for lower timing error.

This mode should never activate automatically without being requested by the backend configuration.

---

# 64. DUAL

Generate both:

```text
SOURCE_TEMPO version
```

and:

```text
OPTIMIZED version
```

Then compare:

- timing error
- tempo difference
- rhythmic collisions
- physical complexity

This is the default experimental mode for difficult Redstone Physical benchmark material.

---

# 65. Tempo Optimization

The tempo optimizer evaluates candidate tempos close to the source.

Configuration should include:

```yaml
enabled: true
maximum_percent_change:
step_size:
priority_weighting: true
preserve_tempo_ratios: true
```

A default maximum change may eventually be established through listening tests.

Until then, the allowed range should be explicit in each project.

---

# 66. Global Tempo Scaling

For songs with multiple tempo changes, the preferred optimization method is initially:

```text
GLOBAL SCALE
```

Example:

```text
scale factor = 1.012
```

Then:

```text
100 QPM → 101.2 QPM

120 QPM → 121.44 QPM

90 QPM → 91.08 QPM
```

This preserves relationships between tempo sections.

Independent optimization of each section should require explicit permission.

---

# 67. Quantization Objective

A candidate timing solution should consider:

```text
weighted absolute onset error

weighted squared onset error

IOI distortion

sequence collapse

anchor displacement

riff-cycle distortion

bar grouping

simultaneity
```

No single statistic is sufficient.

---

# 68. Hard Constraints

The solver must obey:

```text
event ordering preserved

onset groups remain simultaneous

legal integer backend ticks

no negative event times after preroll

explicit minimum endpoint reuse rules

locked anchors obey backend policy
```

Violating a hard constraint makes a candidate invalid.

---

# 69. Soft Constraints

Soft constraints may include:

```text
minimum average error

minimum maximum error

preserve groove

preserve local pattern ratios

prefer fewer distinct delay lengths

prefer simpler redstone
```

Musical soft constraints outrank physical convenience unless project settings say otherwise.

---

# 70. Command Rail Timing Grid

Command Rail uses:

```text
1 game tick
```

as its default scheduler unit.

Therefore its basic sequencer grid is:

```text
50 ms
```

This gives it twice the normal temporal resolution of a repeater-only redstone timeline.

---

# 71. Command Rail Controller

BlockScore should support at least two controller implementations:

```text
COMMAND_BLOCK_CONTROLLER

DATAPACK_CONTROLLER
```

Both use the same compiled game-tick event schedule.

The controller implementation does not change musical timing.

---

# 72. Command Block Controller

A practical command-block architecture may use:

```text
repeating command block
        ↓
increment song tick
        ↓
chain/conditional dispatch
        ↓
trigger endpoint commands
```

A repeating command block can operate once per game tick.

Multiple commands belonging to the same song tick should be treated as simultaneous for BlockScore timing purposes.

---

# 73. Datapack Controller

A datapack controller may use:

```text
tick function

scoreboard clock

scheduled functions

generated per-tick dispatch functions
```

The precise implementation is a backend engineering choice.

The canonical compiled schedule remains:

```text
game_tick → events
```

---

# 74. Dense Command Rail Recommendation

For dense songs, BlockScore should prefer a persistent tick counter over scheduling every individual note independently.

Conceptually:

```text
song_tick += 1

if song_tick == 127:
    dispatch events for 127
```

This provides:

- centralized pause/reset behavior
- easy looping
- deterministic event grouping
- easier debugging
- easier section seeking

---

# 75. Command Rail Endpoint Pulse

A physical note block must experience a valid power transition.

Initial conservative model:

```text
tick T:
activate endpoint driver

tick T+1:
deactivate endpoint driver
```

Exact driver implementation remains subject to:

```text
CAL-003
```

and endpoint retrigger behavior to:

```text
CAL-004
```

---

# 76. Endpoint Busy Window

Until calibration proves otherwise, BlockScore should conservatively treat a physical Command Rail endpoint as unavailable for immediate same-endpoint reuse on the next attack without checking reset state.

Initial planning rule:

```text
busy_window_game_ticks = 2
```

This is a conservative allocator rule, not a verified Minecraft limit.

Status:

```text
PROVISIONAL
```

---

# 77. Rapid Repeated Notes

If the same:

```text
instrument + pitch
```

must attack on consecutive game ticks, Command Rail may allocate alternating endpoints.

Example:

```text
tick 100:
guitar_e4_A ON

tick 101:
guitar_e4_A OFF
guitar_e4_B ON

tick 102:
guitar_e4_B OFF
guitar_e4_A ON
```

This allows rapid repeated attacks without requiring one physical endpoint to reset and retrigger impossibly quickly.

Actual behavior must be game-tested.

---

# 78. Command Rail Timing Versus Polyphony

Timing resolution and endpoint polyphony are separate.

A 50 ms event grid does not mean one endpoint can necessarily retrigger every 50 ms.

When endpoint recovery is slower than event spacing, BlockScore increases the endpoint pool.

Do not solve an endpoint reuse problem by changing the song timing unless necessary.

---

# 79. Command Rail Same-Tick Chords

All notes in a same-tick chord can use separate endpoint drivers.

Conceptually:

```text
tick 200:

activate bass_c2
activate guitar_g3
activate trumpet_e4
activate trumpet_g4
activate kick
```

These should be dispatched within the same game tick.

Command ordering inside that tick is not treated as intentional musical arpeggiation.

---

# 80. Digital Playback Timing

Digital Playback uses the game-tick grid unless a future supported mechanism offers a stronger guarantee.

Normal target:

```text
20 scheduling buckets per second
```

Sub-game-tick onset timing should not be claimed.

---

# 81. Digital Playback Advantage

Although its basic scheduling grid is the same as Command Rail, Digital Playback does not have:

- physical endpoint reset limitations
- support-block routing
- redstone branch propagation
- physical polyphony limits

Therefore its timing compiler may accept schedules that require more endpoint duplication in Command Rail.

---

# 82. Redstone Physical Timing

The standard Redstone Physical backend uses:

```text
integer redstone ticks
```

Every compiled onset receives:

```text
compiled_redstone_tick
```

The physical timing trunk realizes differences between consecutive compiled onset positions.

---

# 83. Redstone Delta Construction

Suppose compiled onset groups occur at:

```text
0
3
8
12
```

redstone ticks.

Required timing deltas are:

```text
3
5
4
```

The physical circuit constructs those delays using repeater combinations.

Example:

```text
5 =
4 + 1
```

---

# 84. Do Not Chain Rounded Musical Durations

The physical backend must first determine absolute compiled positions.

Only then may it calculate circuit deltas.

Correct:

```text
Master absolute times
      ↓
quantized absolute redstone ticks
      ↓
subtract adjacent ticks
      ↓
build repeater delays
```

Incorrect:

```text
round duration 1
      ↓
build
      ↓
round duration 2
      ↓
build
```

---

# 85. Redstone Branch Equalization

When one onset fans out into several instruments:

```text
TIMING TRUNK
    ├── note A
    ├── note B
    └── note C
```

all branches must have equal effective delay.

If geometry requires:

```text
branch A = +1 redstone tick
```

then B and C must receive compensation or routing must change.

---

# 86. Redstone Timing Versus Layout

Physical layout may force additional repeater delays.

Therefore Redstone Physical compilation has two timing passes:

```text
LOGICAL TIMING

GEOMETRY-AWARE TIMING
```

The second pass verifies that routing did not alter the intended compiled schedule.

---

# 87. Advanced Redstone Timing

Future BlockScore versions may support an:

```text
ADVANCED_REDSTONE
```

backend using mechanics beyond ordinary repeater timing.

Possible examples include specialized pulse circuits or other game-tick-scale redstone behavior.

These mechanisms are excluded from the standard backend until individually specified and tested.

The normal backend prioritizes robustness over cleverness.

---

# 88. Start Time

A song backend may have constant startup latency.

Example:

```text
button pressed

4 game ticks preparation

first musical event
```

Constant pre-roll is not considered musical timing error.

BlockScore stores:

```text
PREROLL_TICKS
```

separately from song time.

---

# 89. Song Tick Zero

The first Master musical position is:

```text
song_time = 0
```

Backend implementations may map that to:

```text
world game tick 458312
```

or:

```text
controller tick 4
```

The mapping is irrelevant to the score.

---

# 90. Pause

Command-controlled backends should eventually support pause.

Pausing freezes:

```text
song_tick
```

without altering the compiled event map.

Physical Redstone playback may not support clean pause without additional circuitry.

Pause capability is backend-specific.

---

# 91. Seeking

Command-controlled backends may eventually support:

```text
seek to section

seek to measure

seek to song tick
```

Because the canonical timing model is absolute, seeking does not require replaying all previous timing calculations.

Stateful musical effects may still require special handling.

---

# 92. Loop Timing

Loop boundaries must be explicit anchors.

Store:

```text
loop_start_master_time

loop_end_master_time

ideal_loop_duration

compiled_loop_duration
```

---

# 93. Loop Drift

If the ideal loop duration is:

```text
127.5 game ticks
```

but the backend repeats every:

```text
128 game ticks
```

the loop differs from source duration.

However, it must not compound by repeatedly rounding from the prior loop.

Every iteration uses the same compiled loop period.

Report:

```text
LOOP_PERIOD_ERROR
```

rather than allowing hidden drift.

---

# 94. Loop Seam

The timing solver must inspect:

```text
last attack before loop end

first attack after loop restart
```

A mathematically close loop can still produce a bad seam.

Loop QA therefore includes:

```text
SEAM_IOI_ERROR
```

---

# 95. Simulation Time Versus Wall Time

Minecraft timing is simulation-tick based.

At healthy performance:

```text
20 TPS
```

corresponds to:

```text
50 ms per game tick
```

If the game/server falls behind, tick-based playback takes longer in real-world wall time.

Therefore BlockScore distinguishes:

```text
SIMULATION_TIME_ACCURACY
```

from:

```text
WALL_CLOCK_ACCURACY
```

---

# 96. Lag Behavior

A perfectly compiled:

```text
120 BPM
```

Minecraft sequence may sound slower in real time if the game runs below 20 TPS.

The compiler cannot solve machine/server lag through note placement.

Performance testing should eventually record:

```text
TPS

MSPT
```

during playback.

---

# 97. Lag Does Not Change Score Validity

A lag spike does not mean the event map is mathematically wrong.

QA should report:

```text
COMPILED_TIMING_VALID
```

separately from:

```text
RUNTIME_PERFORMANCE_VALID
```

---

# 98. Timing Metrics

Each compiled section should eventually report:

```text
event_count

exact_event_count

quantized_event_count

sequence_collapse_count

maximum_absolute_error_ms

mean_absolute_error_ms

RMS_error_ms

maximum_IOI_error_ms

mean_IOI_error_ms

anchor_error_ms

loop_period_error_ms

timing_collision_count
```

---

# 99. Weighted RMS Error

A useful optimization metric is:

```text
weighted_RMS =
sqrt(
    sum(weight_i * error_i^2)
    /
    sum(weight_i)
)
```

where:

```text
weight_i
```

includes musical priority and optionally rhythmic-function weighting.

This metric should guide the solver.

It should not be the only PASS criterion.

---

# 100. No Universal Millisecond Pass Threshold

BlockScore should not initially declare:

```text
all errors below X ms = good
```

Music is context dependent.

The significance of timing error depends on:

- tempo
- local subdivision
- voice priority
- groove
- repetition
- accent placement
- neighboring errors

Benchmark testing will eventually establish useful default warning thresholds.

---

# 101. Normalized Timing Error

In addition to milliseconds, BlockScore may calculate:

```text
normalized_error =
absolute_error
/
local_critical_subdivision_duration
```

This gives musical context.

Example:

```text
25 ms error
```

has different significance in:

```text
slow half notes
```

than in:

```text
fast thirty-second notes
```

---

# 102. Timing Warning Classes

Use:

```text
GRID_EXACT

QUANTIZED_LOW_RISK

GROOVE_CHANGE

SEQUENCE_COLLAPSE

ANCHOR_DISPLACEMENT

IOI_DISTORTION

LOOP_SEAM_WARNING

UNREPRESENTABLE_AT_CURRENT_GRID
```

---

# 103. Timing Decision Record

Any nontrivial timing correction should be recordable.

Example:

```yaml
type: TIMING_DECISION

section: A
measure: 7

voice: OSTINATO_A
priority: P5

ideal_game_tick: 127.5
compiled_game_tick: 128

error_ms: 25

reason:
  preserved following accent interval

status:
  APPROVED
```

---

# 104. Backend Comparison

When more than one backend is compiled, produce a comparison.

Example:

```text
COMMAND RAIL
max error: 25 ms
collapses: 0

REDSTONE SOURCE TEMPO
max error: 50 ms
collapses: 4

REDSTONE OPTIMIZED
tempo change: +1.2%
max error: 18 ms
collapses: 0
```

This lets the user choose based on actual musical consequences.

---

# 105. Mars TEST-001 Timing Policy

TEST-001A uses:

```text
MASTER:
exact source timing

COMMAND RAIL:
SOURCE_TEMPO

REDSTONE PHYSICAL:
DUAL
```

The Redstone Physical comparison should include:

```text
source-tempo compile

tempo-optimized candidate
```

No optimized version replaces the source-tempo version automatically.

---

# 106. Mars Priority

For Mars, the following timing elements are P5:

```text
5/4 identity

opening ostinato

meter-defining accents

primary low pulse

major thematic attacks
```

A lower numerical average error is not considered better if it damages these structures.

---

# 107. Future Tool-Like Material

BlockScore's timing architecture is intentionally designed to support material with:

- changing meter
- riffs crossing barlines
- additive groupings
- polymetric cycles
- syncopated bass/drum relationships
- tuplets
- long common-reset cycles

The central requirement is:

```text
every layer resolves against one authoritative absolute timeline
```

---

# 108. Canonical Timing Object

Future machine-readable timing objects should resemble:

```yaml
notation:
  measure: 12
  offset_qn: "7/3"

master:
  absolute_qn: "163/3"
  seconds: 31.728394

backend:
  type: COMMAND_RAIL_PHYSICAL
  grid_hz: 20

  ideal_tick: 634.56788
  compiled_tick: 635

  signed_error_ms: 21.606
  absolute_error_ms: 21.606

analysis:
  priority: P5
  rhythmic_role: RIFF_ANCHOR
  sequence_collapse: false
  warning: null
```

Exact schema will eventually live in:

```text
specs/timing.schema.json
```

---

# 109. Timing Compiler Stages

The eventual implementation should follow:

```text
1. parse meter map

2. calculate exact absolute QN

3. parse tempo map

4. apply performance timing

5. integrate to Absolute Master Time

6. construct simultaneous onset groups

7. assign musical weights

8. project onto backend ideal tick coordinates

9. generate legal tick candidates

10. solve local/global quantization

11. detect collisions

12. calculate error metrics

13. apply backend endpoint constraints

14. run geometry-aware timing verification if physical

15. produce timing report
```

---

# 110. Separation of Responsibilities

The timing compiler decides:

```text
WHEN
```

The pitch/instrument solver decides:

```text
WHAT SOUND
```

The physical backend decides:

```text
WHERE AND HOW TO BUILD IT
```

These concerns may exchange constraints but should not be collapsed into one algorithm.

---

# 111. Determinism

Given identical:

```text
Master Score

backend settings

Minecraft profile

solver version
```

BlockScore should generate identical timing output.

Random timing decisions are forbidden unless a future humanization mode explicitly requests them.

---

# 112. Reproducibility

Timing reports should record:

```text
timing_model_version

solver_version

Minecraft_profile

backend

tempo_mode

optimization_settings
```

This allows an old song to be rebuilt even after the compiler evolves.

---

# 113. Calibration Dependencies

The following timing behavior still requires direct Java 26.2 game testing:

```text
CAL-003
Command Rail physical driver behavior

CAL-004
minimum physical endpoint retrigger interval

CAL-005
same-tick multi-endpoint synchronization
```

Until those tests pass:

```text
20 TPS scheduler timing
```

is considered established,

while:

```text
physical endpoint recovery behavior
```

remains provisional.

---

# 114. Research Basis

The BlockScore Java 26.2 timing model is based on the current Minecraft/Paper timing model in which:

```text
game simulation target:
20 ticks per second

game tick:
50 ms

redstone repeater unit:
2 game ticks

redstone repeater minimum delay:
1 redstone tick

redstone repeater maximum single-block delay:
4 redstone ticks

repeating command block:
capable of execution each game tick
```

Java function scheduling also supports delayed execution, but the BlockScore architecture does not require one scheduled function per note.

---

# 115. Governing Timing Rule

> Never trade hidden drift for apparent local simplicity.

Preserve exact musical timing in the Master.

Compile from absolute time.

Distribute unavoidable backend error intentionally.

Keep important simultaneous events simultaneous.

Keep important cycles phase-correct.

And report every timing compromise that could change the music.
