# BlockScore Physical Redstone Backend

## Minecraft Java Edition 26.2

This document defines the traditional physical redstone backend for BlockScore.

Backend identifier:

```text
REDSTONE_PHYSICAL
```

This backend uses:

- real note blocks
- real instrument support blocks
- redstone dust
- repeaters
- physical timing paths
- physical chord branches
- physical start/reset controls

Normal playback must not depend on:

- command blocks
- datapacks
- `/playsound`
- externally scheduled commands

The build itself contains the song timing.

---

# 1. Core Concept

The Minecraft Master contains the music.

The timing compiler converts that music into legal redstone-tick positions.

The Physical Redstone backend then realizes those positions as actual redstone circuitry.

Pipeline:

```text
MINECRAFT MASTER
        ↓
REDSTONE TIMING COMPILER
        ↓
LOGICAL ONSET TICKS
        ↓
PHYSICAL CIRCUIT LAYOUT
        ↓
GEOMETRY-AWARE TIMING CHECK
        ↓
REAL NOTE BLOCK BUILD
```

---

# 2. Governing Rule

> The circuit must reproduce the compiled timing. The music must not be rewritten merely because a convenient redstone path is easier to build.

Layout serves timing.

Timing serves the Minecraft Master.

---

# 3. Timing Authority

The Physical Redstone backend does not invent musical timing.

Timing comes from:

```text
docs/TIMING_MODEL.md
```

The backend receives events already compiled to:

```text
integer redstone ticks
```

Example:

```yaml
onset_group: onset-0142
compiled_redstone_tick: 87
```

The physical circuit's job is to make that onset occur at redstone tick 87.

---

# 4. Standard Redstone Grid

The default Physical Redstone backend uses:

```text
1 redstone tick
=
2 game ticks
=
0.1 seconds
```

The basic physical timing resolution is therefore:

```text
10 timing positions per second
```

Advanced sub-redstone-tick techniques are outside the standard backend.

---

# 5. Repeater Delay

A repeater can contribute:

```text
1 redstone tick

2 redstone ticks

3 redstone ticks

4 redstone ticks
```

BlockScore records repeater setting directly as:

```text
delay_rt
```

Example:

```yaml
block: repeater
delay_rt: 3
```

---

# 6. Delay Decomposition

A required delay may be represented by several repeaters.

Example:

```text
required delay:
11 redstone ticks
```

One valid decomposition is:

```text
4 + 4 + 3
```

BlockScore should generally prefer fewer repeaters when all other constraints are equal.

---

# 7. Delay Decomposition Is Not the Whole Circuit

Repeaters may also be required for:

- signal restoration
- directional isolation
- branch control
- geometry
- preventing unwanted backflow

Every such repeater also contributes real timing delay.

The layout compiler must include it.

---

# 8. Logical Timing versus Physical Timing

BlockScore distinguishes:

```text
LOGICAL_TIMING
```

from:

```text
PHYSICAL_TIMING
```

Logical timing says:

```text
this chord occurs at redstone tick 87
```

Physical timing asks:

```text
how many actual redstone ticks elapse from the start pulse to every note block in that chord?
```

These must agree.

---

# 9. Geometry-Aware Verification

After physical routing, BlockScore recalculates every path.

For each note event:

```text
physical_arrival_tick
```

must equal:

```text
compiled_redstone_tick
```

unless an explicitly approved warning exists.

---

# 10. Event-Per-Occurrence Default

Traditional Physical Redstone defaults to:

```text
EVENT_PER_OCCURRENCE
```

A musical attack normally receives its own physical note block.

If Guitar E4 occurs 80 times:

```text
80 physical Guitar E4 events
```

may exist along the song track.

This differs fundamentally from Command Rail, which reuses endpoint banks.

---

# 11. Why Event-Per-Occurrence Is Default

Event-per-occurrence simplifies:

- timing
- routing
- debugging
- schematic generation
- physical inspection
- survival construction
- deterministic playback

The tradeoff is physical size.

---

# 12. Optional Note Reuse

Future advanced layouts may support:

```text
REUSABLE_NOTE_MODULE
```

where multiple timing paths trigger the same physical note block.

This is not part of the initial backend.

The standard backend prioritizes understandable deterministic circuitry.

---

# 13. Physical Event

A normal pitched physical event requires:

```text
NOTE BLOCK

SUPPORT BLOCK

CLEARANCE

TRIGGER CONNECTION
```

Example:

```text
AIR

NOTE BLOCK
   ← trigger

WHITE WOOL
```

This represents one Guitar note event.

---

# 14. Event Object

A physical event should eventually contain:

```yaml
event_id:
source_event_id:
onset_group:
compiled_tick:
instrument:
pitch:
note_state:
support_block:
note_position:
support_position:
trigger_position:
route_id:
physical_arrival_tick:
status:
```

---

# 15. Onset Group

Events that must occur simultaneously share an:

```text
ONSET_GROUP
```

Example:

```text
tick 120

Bass C2
Guitar E3
Guitar G3
Trumpet C4
Kick
```

All five notes belong to the same onset group.

---

# 16. Chord Fan-Out

A timing trunk may branch to several note blocks.

Conceptually:

```text
TIMING TRUNK
      |
      +------ Bass C2
      |
      +------ Guitar E3
      |
      +------ Guitar G3
      |
      +------ Trumpet C4
      |
      +------ Kick
```

Every branch must reach its note block on the same intended tick.

---

# 17. Branch Delay Equality

For a simultaneous onset:

```text
arrival_A
=
arrival_B
=
arrival_C
```

If geometry produces:

```text
branch A = 2 RT

branch B = 4 RT

branch C = 3 RT
```

BlockScore must add compensation or redesign the branches.

---

# 18. Compensation

The previous example may become:

```text
A:
2 + 2 compensation = 4

B:
4 = 4

C:
3 + 1 compensation = 4
```

All notes then arrive together.

---

# 19. Zero Musical Spread Default

A chord's allowed intentional spread is:

```text
0 redstone ticks
```

unless the Minecraft Master explicitly describes an arpeggio or spread chord.

Physical routing may not create accidental arpeggiation.

---

# 20. Timing Trunk

The central redstone path that encodes song progression is the:

```text
TIMING TRUNK
```

It carries the play pulse through time.

Onset groups branch from this trunk.

---

# 21. Timing Node

Each unique compiled onset position becomes a:

```text
TIMING NODE
```

Example:

```yaml
node_id: time-0087
absolute_tick: 87
events:
  - event-120
  - event-121
  - event-122
```

The physical trunk reaches that node at redstone tick 87.

---

# 22. Timing Delta

The time between consecutive timing nodes is:

```text
delta_rt
```

Example:

```text
node A:
tick 40

node B:
tick 44

delta:
4 RT
```

---

# 23. Timing Node Construction

A logical sequence:

```text
0
3
8
12
20
```

creates trunk deltas:

```text
3
5
4
8
```

The physical layout constructs those delays.

---

# 24. Never Chain Musical Rounding

The backend must never do:

```text
round duration
build it
round next duration
build it
```

It receives already compiled absolute onset positions.

Then it derives deltas.

This prevents accumulated timing drift.

---

# 25. Song Start

The build has a clear:

```text
START INPUT
```

Default trigger may be:

- button
- lever pulse
- pressure plate
- external redstone pulse

The input creates one clean playback pulse.

---

# 26. Start Pulse

The start mechanism should produce a pulse suitable for entering the timing trunk.

BlockScore should not assume a permanently powered input.

The actual pulse-shaping circuit may vary by layout.

---

# 27. Playback State

A normal linear redstone song behaves more like a physical pulse traveling through a circuit than a software state machine.

Minimum conceptual states:

```text
READY

PLAYING

RESETTING
```

---

# 28. Stop Behavior

A purely physical linear build may not support immediate arbitrary stop after the pulse has entered all active circuit regions.

Optional stop circuitry may:

- cut trunk power
- block repeater propagation
- reset latches
- disable output branches

Initial BlockScore builds may omit sophisticated emergency stop behavior.

---

# 29. Reset

A simple one-shot physical song should return naturally to:

```text
READY
```

after all redstone power decays.

No note block should remain permanently powered.

---

# 30. Looping

Looping requires explicitly returning the ending pulse to the start or loop point.

A loop must satisfy:

```text
compiled loop period
=
physical loop period
```

The return path delay counts toward loop timing.

---

# 31. Loop Return Path

If the musical loop needs:

```text
80 RT
```

and the main sequence consumes:

```text
74 RT
```

the loop return path may require:

```text
6 RT
```

of additional delay before the next iteration begins.

---

# 32. Loop QA

Loop validation must inspect:

- loop period
- end-to-start interval
- stuck power
- overlapping old/new pulses
- repeater state
- note retrigger safety

---

# 33. Linear Track Layout

Initial layout mode:

```text
LINEAR_TRACK
```

A timing path progresses primarily in one direction.

Example:

```text
START → R → R → R → R → R → ...
               |       |
               N       N
```

This is simple but physically long.

---

# 34. Serpentine Track

A more practical layout is:

```text
SERPENTINE_TRACK
```

The timing trunk folds back and forth.

Top-view concept:

```text
→ → → → → → →
              ↓
← ← ← ← ← ← ←
↓
→ → → → → → →
```

This reduces footprint while maintaining logical sequence.

---

# 35. Track Turn

A serpentine turn must preserve timing.

If the turn geometry introduces:

```text
1 additional repeater
```

that delay becomes part of the timing path.

The compiler must account for it.

---

# 36. Turn Compensation

Turns should ideally be designed with known fixed timing cost.

Example:

```text
TURN_MODULE_A
cost = 2 RT
```

The timing layout can then include that cost deterministically.

---

# 37. Track Row

A serpentine layout consists of:

```text
TRACK_ROWS
```

Configuration may include:

```yaml
notes_per_row:
row_spacing:
turn_module:
```

---

# 38. Notes per Row

Example:

```text
notes_per_row = 24
```

does not necessarily mean exactly 24 musical attacks.

It means a maximum number of logical event/timing cells before folding.

Dense chords may consume additional side space.

---

# 39. Parallel Voice Tracks

Optional layout:

```text
PARALLEL_VOICE_TRACKS
```

Different musical voices receive separate physical tracks.

Example:

```text
BASS TRACK

GUITAR TRACK

BRASS TRACK

PERCUSSION TRACK
```

A master timing bus synchronizes them.

---

# 40. Advantages of Parallel Voice Tracks

This can simplify:

- debugging
- visual comprehension
- solo construction
- instrument maintenance
- dense polyphony

But synchronization becomes more complex.

---

# 41. Voice Track Synchronization

Every parallel track must begin from the same timing reference.

If separate tracks contain different repeater/restoration costs, BlockScore must verify absolute arrival times independently.

---

# 42. Layered Track Layout

Optional future layout:

```text
STACKED_TRACKS
```

places separate tracks on different vertical levels.

This can reduce horizontal footprint but increases:

- vertical routing complexity
- clearance risk
- maintenance difficulty

It is not the initial default.

---

# 43. Initial Default Layout

For early BlockScore testing:

```text
layout:
SERPENTINE_TRACK
```

is preferred.

It balances:

- understandable circuitry
- manageable footprint
- direct visual inspection

---

# 44. Circuit Cell

The backend may represent physical construction as reusable:

```text
CIRCUIT CELLS
```

Examples:

```text
DELAY_CELL

ONSET_CELL

TURN_CELL

BRANCH_CELL

NOTE_CELL

RESTORATION_CELL

START_CELL

LOOP_CELL
```

---

# 45. Delay Cell

A Delay Cell contains repeaters whose total delay equals a known value.

Example:

```yaml
cell_type: DELAY
delay_rt: 7
decomposition:
  - 4
  - 3
```

---

# 46. Onset Cell

An Onset Cell exposes the timing pulse to one or more note branches.

Example:

```text
TRUNK → ONSET → TRUNK
          |
          +→ NOTE BRANCH
```

---

# 47. Branch Cell

A Branch Cell distributes the onset pulse.

It must not change timing unpredictably.

Each output path receives an explicitly modeled delay.

---

# 48. Note Cell

A Note Cell contains:

```text
note block

support material

clearance

trigger wiring
```

It should be generated as one logical module.

---

# 49. Restoration Cell

Redstone dust loses signal strength over distance.

Where a signal must travel farther than an uninterrupted dust path safely permits, the backend may insert a repeater to restore signal.

That repeater contributes timing delay.

---

# 50. Restoration Is Not Free

The backend must never insert a repeater only for power restoration and forget its timing cost.

Every repeater is part of the path-delay calculation.

---

# 51. Directional Isolation

Repeaters may also prevent unwanted redstone backflow.

Such repeaters are also timing-bearing components.

The layout planner should distinguish:

```text
TIMING_REPEATER

RESTORATION_REPEATER

ISOLATION_REPEATER

COMPENSATION_REPEATER
```

even though all are physical repeaters.

---

# 52. Repeater Role Metadata

Example:

```yaml
repeater:
  delay_rt: 1
  role: COMPENSATION
```

This improves debugging and optimization.

---

# 53. Signal Strength

Physical routes must maintain valid signal strength all the way to the intended target.

A path that mathematically has correct repeaters but electrically fails to power the note block is invalid.

---

# 54. Signal Simulation

Offline QA should simulate at minimum:

```text
power path connectivity

repeater direction

repeater delay

branch arrival

signal restoration

target activation
```

A future full redstone simulator may go further.

---

# 55. Power Isolation

One note branch must not accidentally trigger:

- another onset
- another timing node
- another note block
- reverse trunk propagation

Isolation is a primary layout constraint.

---

# 56. Adjacent Note Blocks

Dense note layouts must consider direct and indirect power interactions.

The backend should not place note blocks merely as close together as possible without power-isolation analysis.

---

# 57. Instrument Support

Every physical note event uses support material from:

```text
data/java-26.2/instruments.json
```

The backend must not hard-code instrument blocks separately.

---

# 58. Pitch

Every pitched event must contain:

```text
note_state 0..24
```

The backend places that exact state.

No tuning changes occur during normal playback.

---

# 59. Percussion

Percussion note blocks also retain their configured:

```text
note_state
```

even though BlockScore models their musical role through:

```text
percussion_function
```

Example:

```yaml
instrument: basedrum
note_state: 4
percussion_function: KICK
```

---

# 60. Top Clearance

Normal physical note blocks require their playback clearance preserved.

The layout generator must reserve the appropriate space above each note block according to the version profile.

---

# 61. Vertical Wiring

Do not route solid timing circuitry through required note-block clearance.

Vertical layouts must keep note cells acoustically valid.

---

# 62. Trumpet Support

Copper trumpet-family events use support blocks defined by the Java 26.2 registry.

Until copper-stability calibration is complete, trumpet events may carry:

```text
COPPER_STABILITY_PENDING
```

---

# 63. Copper Oxidation Risk

A long-lived physical build using unwaxed copper may change instrument timbre if its support blocks oxidize.

This is a genuine backend-maintenance issue.

The backend must not ignore it.

---

# 64. Physical Build Modes

The backend should eventually support:

```text
CREATIVE_BUILD

SURVIVAL_BUILD
```

Both reproduce the same music.

They differ in construction optimization.

---

# 65. Creative Build

Creative mode may prioritize:

- compactness
- schematic placement
- rare blocks
- easier circuit geometry

Material cost is secondary.

---

# 66. Survival Build

Survival mode may prioritize:

- common materials
- fewer expensive support blocks
- accessible tuning
- maintenance paths
- straightforward construction order

Musical correctness still remains first.

---

# 67. Canonical Construction Palette

Circuitry should initially use a predictable palette.

Example:

```text
structure block:
stone / smooth stone

redstone dust:
minecraft:redstone_wire

repeater:
minecraft:repeater

note block:
minecraft:note_block
```

The exact structural palette can later be customized.

---

# 68. Functional versus Decorative Blocks

BlockScore distinguishes:

```text
FUNCTIONAL BLOCKS
```

from:

```text
DECORATIVE BLOCKS
```

A decorative pass may not alter functional redstone behavior.

---

# 69. Maintenance Aisle

Large physical builds should normally include access paths.

Maintenance access allows:

- tuning verification
- repeater inspection
- branch debugging
- manual repair

---

# 70. Compact Mode

Optional:

```text
COMPACT_MODE
```

reduces maintenance spacing.

This may make the build harder to inspect.

It should not alter timing.

---

# 71. Listener Position

Physical note blocks emit sound from world positions.

The backend defines a:

```text
PERFORMANCE_ORIGIN
```

used for audibility analysis.

---

# 72. Audible Range

The backend should use the current Minecraft profile's audible-distance assumptions rather than hard-code them independently.

If important endpoints fall outside practical range:

```text
AUDIBILITY_WARNING
```

must be emitted.

---

# 73. Distributed Track Problem

A traditional redstone machine may become extremely long.

Even if electrically valid, distant note blocks may become poor physical playback sources for one listener.

The layout compiler therefore must consider:

```text
timing footprint
```

and:

```text
audio footprint
```

separately.

---

# 74. Track Folding for Audio

Serpentine layout is useful not only for compact construction but also for keeping note events closer to the listener.

---

# 75. Multiple Performance Origins

Future large installations may support:

```text
MULTI_LISTENER
```

or multiple performance areas.

Initial backend assumes one primary Performance Origin.

---

# 76. Physical Footprint

The backend should calculate:

```text
min_x
max_x

min_y
max_y

min_z
max_z
```

and report:

```text
width
height
length
volume
```

---

# 77. Chunk Footprint

Also report:

```text
chunks_touched
```

Large builds spanning many chunks may have runtime-loading implications.

---

# 78. Chunk Boundary Awareness

The layout engine should not assume all redstone remains active regardless of simulation/loading state.

Initial generated performance builds should aim to remain in a deliberately loaded area.

---

# 79. Event Density

Dense onsets increase side-branch space.

For each timing node, calculate:

```text
polyphony_count
```

Example:

```text
tick 120:
12 simultaneous attacks
```

---

# 80. Maximum Physical Polyphony

Traditional redstone can support large chords by branching to many note blocks.

The limiting factors are practical:

- footprint
- routing
- power isolation
- signal restoration
- listener audibility

BlockScore must not impose an arbitrary low software polyphony limit.

---

# 81. Branch Packing

For a dense chord, note branches may be arranged:

```text
LEFT

RIGHT

MULTIROW

VERTICAL
```

depending on layout mode.

Every branch must preserve timing.

---

# 82. Symmetric Fan-Out

Where practical, dense chords should use approximately symmetric branch geometry.

This can reduce required compensation.

Example:

```text
      N N N
       \|/
TRUNK--O--TRUNK
       /|\
      N N N
```

---

# 83. Asymmetric Fan-Out

Asymmetric placement is allowed if:

```text
effective branch delay
```

is equalized.

A visually symmetric build is not required.

A timing-symmetric build is.

---

# 84. Fast Repeated Notes

Repeated notes occurring close together generally use separate event note blocks in the standard backend.

Example:

```text
tick 20:
Guitar E4 block A

tick 21:
Guitar E4 block B

tick 22:
Guitar E4 block C
```

This avoids physical endpoint-reset constraints.

---

# 85. Event Block Duplication Is Expected

Traditional note-block songs may contain many copies of identical pitches.

BlockScore does not treat this as waste or failure.

It is part of the backend's physical architecture.

---

# 86. Repetition Compression

Future advanced physical layouts may reuse note modules.

Standard backend does not require this optimization.

---

# 87. Timing Optimization Modes

The Physical Redstone backend can request:

```text
SOURCE_TEMPO

REDSTONE_OPTIMIZED

DUAL
```

from the timing compiler.

It does not implement these rules itself.

---

# 88. DUAL Mode

For difficult music, BlockScore should usually generate:

```text
SOURCE TEMPO candidate
```

and:

```text
REDSTONE-OPTIMIZED candidate
```

for comparison.

The optimized candidate may not silently replace the source-tempo candidate.

---

# 89. Layout Does Not Requantize

After a timing candidate is selected, physical layout may not decide:

```text
this delay would be easier if this note moved one tick
```

without invoking an explicit new timing revision.

Geometry does not have authority to silently requantize music.

---

# 90. Geometry Failure

If the layout cannot realize the selected timing:

```text
LAYOUT_TIMING_CONFLICT
```

is emitted.

Possible resolution:

- alter geometry
- use different branch structure
- use additional compensation
- change layout mode
- return to timing solver

---

# 91. Layout Retry

A compiler may automatically try multiple geometries.

Example:

```text
attempt 1:
simple branch

attempt 2:
mirrored branch

attempt 3:
multirow chord module
```

But musical timing remains fixed during retries.

---

# 92. Material Report

Every compiled build should report counts for:

```text
note blocks

support materials by type

redstone dust

repeaters

structural blocks

buttons/levers

signs/labels

maintenance floor

optional decoration
```

---

# 93. Repeater Settings Report

Material count alone is insufficient.

The backend should also report:

```text
1-tick repeaters

2-tick repeaters

3-tick repeaters

4-tick repeaters
```

This helps manual building.

---

# 94. Tuning Report

For each note event or grouped identical note type:

```text
instrument

pitch

note_state

manual click count
```

should be available.

---

# 95. Build Order

A human construction guide may recommend:

```text
1. structural floor

2. timing trunk

3. repeaters

4. onset branches

5. instrument support blocks

6. note blocks

7. tuning

8. start controls

9. labels

10. QA test
```

---

# 96. Schematic Output

Automated structure output should place:

- support materials
- note block states
- repeater states
- redstone dust
- structural blocks
- controls

exactly as compiled.

---

# 97. Litematica Output

Future Litematica-compatible output should preserve:

```text
note state

instrument support material

repeater delay

repeater facing

wire placement

control placement
```

The exported schematic must not require manual retuning unless explicitly requested.

---

# 98. Structure Origin

The canonical build plan uses:

```text
relative coordinates
```

A placement origin translates the entire structure into world coordinates.

---

# 99. Orientation

Supported orientations should eventually include:

```text
NORTH

SOUTH

EAST

WEST
```

Rotating a build must correctly rotate:

- repeaters
- directional components
- track turns
- control interfaces

---

# 100. Mirroring

Future:

```text
MIRROR_X

MIRROR_Z
```

may be supported.

Directional redstone state must transform correctly.

---

# 101. Offline Timing Simulation

Before export, BlockScore should traverse every physical trigger path.

For each event:

```text
start
→ path components
→ total delay
→ note block
```

Then verify the total.

---

# 102. Simulation Record

Example:

```yaml
event_id: event-0281
compiled_tick: 120

path:
  - repeater: 4
  - repeater: 4
  - repeater: 3
  - compensation: 1

physical_arrival_tick: 120

status: PASS
```

---

# 103. Circuit Connectivity QA

Every musical event must have:

```text
one valid path from song start
```

to its intended note block.

Disconnected notes fail compilation.

---

# 104. Unexpected Connectivity QA

No timing node should accidentally reach an event that does not belong to it.

This produces:

```text
CROSS_TRIGGER_FAILURE
```

---

# 105. Duplicate Trigger QA

A physical note event should receive exactly one intended activation for its onset.

Multiple unintended power paths to the same block produce:

```text
DUPLICATE_TRIGGER_RISK
```

---

# 106. Stuck Power QA

After the song completes:

```text
all timing paths
```

must return to an unpowered stable state.

Any permanently powered note or circuit section is a failure unless explicitly designed.

---

# 107. Circuit Loop QA

Unintended redstone loops are invalid.

A deliberate musical loop must be specifically marked.

---

# 108. Repeater Locking

Layouts should avoid accidental repeater locking unless a module explicitly requires it.

Unexpected repeater locking can break timing.

---

# 109. Torch Logic

Redstone torches may be used in advanced modules.

Initial standard layouts should minimize logic inversion where simpler repeater/dust routing works.

Every torch-based module must have known timing behavior.

---

# 110. Piston Timing

Pistons are excluded from standard musical timing modules unless explicitly specified.

Their behavior is unnecessary for initial BlockScore physical playback.

---

# 111. Observer Timing

Observers are similarly excluded from the basic timing vocabulary.

Future advanced modules may use them after separate specification and testing.

---

# 112. Standard Component Set

Initial backend component vocabulary should remain mostly:

```text
redstone dust

repeaters

solid blocks

note blocks

instrument support blocks

buttons/levers

optional redstone torches
```

This keeps the first compiler manageable and reliable.

---

# 113. Advanced Redstone Backend

Future backend:

```text
REDSTONE_ADVANCED
```

may include:

- observers
- pistons
- comparator logic
- hopper clocks
- specialized pulse circuits
- game-tick timing modules

It is separate from:

```text
REDSTONE_PHYSICAL
```

---

# 114. No Zero-Tick Dependency

The standard backend must not rely on:

```text
zero-tick behavior

update suppression

version-fragile exploits
```

for normal operation.

---

# 115. Build Readability

Development builds should favor:

```text
readable
```

over:

```text
minimum theoretical volume
```

The user should be able to look at the machine and understand its major sections.

---

# 116. Module Labeling

Optional signs may mark:

```text
measure

section

instrument

timing tick

track row
```

This is especially useful during early testing.

---

# 117. Measure Markers

A physical layout may include visual markers at measure boundaries.

These markers do not affect redstone timing.

Example:

```text
M01
M02
M03
```

They help compare the physical machine to the score.

---

# 118. Section Markers

Large songs should visually distinguish:

```text
INTRO

A

B

BUILD

CLIMAX

OUTRO
```

where practical.

---

# 119. Timing Debug Markers

During development, timing nodes may display:

```text
T087

T092

T100
```

representing absolute redstone ticks.

These can be removed from production builds.

---

# 120. Manual Section Test

A development build may optionally expose test inputs at section boundaries.

This allows testing later portions without replaying the entire song.

Such inputs must not alter normal playback circuitry.

---

# 121. Section Start Module

Future development mode may insert:

```text
SECTION_INJECTOR
```

at selected anchor points.

Normal exported production mode can omit these.

---

# 122. Physical Test Sequence

Before declaring GAME_TESTED:

```text
1. start circuit

2. listen for missed notes

3. inspect simultaneous chords

4. inspect rapid repeats

5. inspect turns

6. inspect section boundaries

7. inspect final reset

8. inspect loop if present
```

---

# 123. Timing Calibration Test

A generated timing test may use audible or visual markers to confirm:

```text
1 RT

2 RT

3 RT

4 RT
```

delay modules behave as modeled.

---

# 124. Game-Test Status

The backend may be:

```text
DESIGNED

COMPILED

OFFLINE_VALIDATED

GAME_TESTED

USER_APPROVED
```

Do not conflate these states.

---

# 125. Physical Redstone QA Checklist

Every build must check:

```text
TIMING_PATH_COMPLETE

COMPILED_TICKS_MATCH

BRANCH_DELAYS_EQUALIZED

NOTE_STATES_VALID

SUPPORT_BLOCKS_VALID

CLEARANCE_VALID

REPEATER_STATES_VALID

REPEATER_DIRECTIONS_VALID

SIGNAL_STRENGTH_VALID

NO_CROSS_TRIGGER

NO_DUPLICATE_TRIGGER

NO_STUCK_POWER

NO_UNINTENDED_LOOP

AUDIBILITY_CHECKED

FOOTPRINT_REPORTED

MATERIALS_REPORTED
```

---

# 126. Timing Failure Classes

Use:

```text
PHYSICAL_EARLY

PHYSICAL_LATE

BRANCH_DESYNC

TURN_DELAY_MISMATCH

RESTORATION_DELAY_MISMATCH

LOOP_PERIOD_MISMATCH
```

---

# 127. Electrical Failure Classes

Use:

```text
NO_POWER_PATH

SIGNAL_DECAY_FAILURE

WRONG_REPEATER_DIRECTION

ACCIDENTAL_REPEATER_LOCK

POWER_LEAK

CROSS_TRIGGER

STUCK_POWER
```

---

# 128. Geometry Failure Classes

Use:

```text
BLOCK_COLLISION

CLEARANCE_COLLISION

SUPPORT_COLLISION

MAINTENANCE_COLLISION

CHUNK_LAYOUT_WARNING

AUDIBILITY_WARNING
```

---

# 129. Musical Loss Report

The Physical Redstone backend reports musical differences inherited from timing compilation:

```text
quantized attacks

timing errors

sequence collapses

tempo optimization

groove changes
```

Physical layout itself should introduce:

```text
zero additional musical loss
```

after timing compilation.

---

# 130. Build Cost Report

Physical complexity should be reported separately from musical loss.

Example:

```text
musical:
max timing error = 42 ms

physical:
note blocks = 2,842
repeaters = 1,206
redstone dust = 4,833
footprint = 91 × 8 × 63
```

A large build is not automatically a bad musical result.

---

# 131. Compression Metrics

Traditional Physical Redstone generally has a much lower reuse ratio than Command Rail.

A useful metric is:

```text
physical_note_blocks
/
musical_attacks
```

For event-per-occurrence builds this may approach:

```text
1.0
```

for many voices.

---

# 132. Backend Comparison

For a song compiled to both backends, report:

```text
REDSTONE_PHYSICAL

versus

COMMAND_RAIL_PHYSICAL
```

including:

- timing accuracy
- note-block count
- repeater count
- command count
- footprint
- materials
- maintenance complexity
- revision cost

---

# 133. Revision Behavior

Changing one note in Physical Redstone may require:

- note retuning
- support-block replacement
- branch rerouting
- timing reconstruction
- schematic replacement

This is expected.

---

# 134. Timing-Only Revision

A timing change can affect all later physical circuit positions if the layout is sequential.

Therefore Physical Redstone revisions may be expensive compared with Command Rail.

BlockScore should make that cost visible.

---

# 135. Section Modularity

To reduce revision cost, large builds should be divided into physical:

```text
SECTION MODULES
```

Example:

```text
INTRO MODULE

SECTION A MODULE

SECTION B MODULE
```

connected by defined timing interfaces.

---

# 136. Section Interface

A module should expose:

```text
INPUT PULSE

OUTPUT PULSE
```

with known total duration.

This lets sections be regenerated independently.

---

# 137. Module Duration

For each section:

```text
module_duration_rt
```

must equal the compiled section duration.

---

# 138. Modular Revision Advantage

If Section B changes while Section A does not:

```text
replace Section B module
```

should be preferable to rebuilding the entire machine when possible.

---

# 139. Mars TEST-001A Layout

Mars TEST-001A should initially use:

```text
backend:
REDSTONE_PHYSICAL

layout:
SERPENTINE_TRACK

timing_mode:
DUAL
```

The two timing candidates are:

```text
SOURCE_TEMPO

REDSTONE_OPTIMIZED
```

---

# 140. Mars Physical Priorities

P5 timing includes:

```text
5/4 identity

opening ostinato

meter-defining accents

primary low pulse

major thematic attacks
```

The physical layout must preserve the selected compiled version exactly.

---

# 141. Mars Test Questions

TEST-001A should answer:

```text
How many note blocks does the traditional build require?

How many repeaters?

What is the footprint?

What is the longest branch?

How much chord compensation is required?

Does source-tempo quantization damage the ostinato?

Does a small tempo optimization materially improve the build?

Can all P5 attacks remain distinct?

Does the build remain practically audible from one performance point?
```

---

# 142. Mars Acceptance Criteria

Physical TEST-001A passes only if:

```text
all compiled events physically exist

all paths are connected

all event arrival ticks match

all chords are synchronized

all note states are legal

all support blocks are correct

all note blocks have required clearance

no cross-trigger exists

no stuck power exists

timing warnings are documented

P5 rhythmic identity survives
```

---

# 143. Tool-Like Material

For future Tool-style rhythm, Physical Redstone may become very large.

That is acceptable.

The backend should reveal where:

```text
odd-meter structure

tuplets

polyrhythm

rapid repeated attacks
```

are difficult on the 10 Hz grid.

It must not simplify them silently.

---

# 144. Backend Recommendation Is Not Automatic

BlockScore should not automatically replace Physical Redstone with Command Rail simply because Command Rail is more compact.

The user may deliberately want:

```text
a giant physical music machine
```

That is a legitimate output target.

---

# 145. Planned Output Files

Future compiled Physical Redstone packages may contain:

```text
redstone-plan.json

timing-nodes.json

physical-events.json

materials.json

warnings.json

build.nbt

build.litematic
```

---

# 146. Canonical Plan Example

Conceptually:

```yaml
profile: java-26.2
backend: REDSTONE_PHYSICAL

timing_mode: SOURCE_TEMPO

layout:
  type: SERPENTINE_TRACK
  notes_per_row: 24

timing_nodes:
  - id: time-0000
    tick: 0

  - id: time-0003
    tick: 3

events:
  - id: event-001
    timing_node: time-0003
    instrument: guitar
    pitch: E4
    note_state: 22
```

---

# 147. Physical Route Example

Conceptually:

```yaml
route:
  event: event-001

  source:
    timing_node: time-0003

  components:
    - type: repeater
      delay_rt: 2

    - type: repeater
      delay_rt: 1

  arrival_tick: 3
```

---

# 148. Implementation Order

Recommended implementation:

```text
1. physical event model

2. timing-node model

3. repeater-delay decomposition

4. simple linear timing trunk

5. note branches

6. chord fan-out

7. branch compensation

8. signal-strength validation

9. serpentine turns

10. geometry-aware timing simulation

11. material counting

12. structure export

13. Litematica export

14. modular section generation

15. advanced layouts
```

---

# 149. Test-First Requirement

Before adding clever compact layouts, establish tests for:

```text
simple delay

long delay

two-note chord

large chord

rapid repeated notes

turn modules

signal restoration

multiple rows

loop return

section interface
```

---

# 150. No Fake Validation Rule

Do not claim:

```text
this redstone machine works in Minecraft
```

because:

```text
the mathematical path delay is correct
```

Offline validation is not game testing.

Both statuses matter.

---

# 151. Governing Physical Redstone Rule

> The redstone machine is the score made physical.

Every delay must be intentional.

Every branch must be synchronized.

Every note block must be correctly tuned and supported.

Every physical routing decision must preserve the compiled music.

And no convenience of circuit design may silently rewrite the song.
