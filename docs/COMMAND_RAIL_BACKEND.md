# BlockScore Command Rail Backend

## Minecraft Java Edition 26.2

This document defines the BlockScore Command Rail backend.

Command Rail is a hybrid physical/digital control system:

- the **sound is produced by real physical Minecraft note blocks**
- each note block sits on its correct instrument material
- note blocks are tuned normally
- commands replace most or all traditional repeater-based timing circuitry
- the physical note blocks are reusable throughout the song
- the song is sequenced on Minecraft's game-tick clock

The primary backend identifier is:

```text
COMMAND_RAIL_PHYSICAL
```

An enhanced variant is:

```text
COMMAND_RAIL_ENHANCED
```

---

# 1. Core Concept

A traditional note-block song often builds another physical note block every time a musical note occurs.

Conceptually:

```text
EVENT
  ↓
NOTE BLOCK
  ↓
EVENT
  ↓
ANOTHER NOTE BLOCK
  ↓
EVENT
  ↓
ANOTHER NOTE BLOCK
```

Command Rail instead separates:

```text
INSTRUMENT
```

from:

```text
SEQUENCER
```

A physical note block represents a reusable instrument endpoint.

The command system decides when that endpoint should sound.

Conceptually:

```text
SONG EVENTS
      ↓
COMMAND SEQUENCER
      ↓
ENDPOINT ADDRESS
      ↓
PHYSICAL POWER PULSE
      ↓
REAL NOTE BLOCK
      ↓
SOUND
```

---

# 2. Governing Rule

> Command Rail must use commands to control real note blocks, not merely place decorative note blocks while `/playsound` secretly produces the music.

For:

```text
COMMAND_RAIL_PHYSICAL
```

the actual sound source must be the physical note block.

If Digital Playback supplements the build, the backend becomes:

```text
COMMAND_RAIL_ENHANCED
```

and every assisted event must be explicitly marked.

---

# 3. Why Command Rail Exists

Command Rail is intended to solve several problems with traditional note-block builds:

- massive timing corridors
- huge repeater counts
- difficult revisions
- difficult polyphony routing
- coarse repeater-only timing
- duplicate physical note blocks for repeated pitches
- complicated chord branching
- large songs becoming impractical to maintain

Command Rail keeps the physical Minecraft instrument while moving sequencing into commands.

---

# 4. Command Rail Is Still a Physical Build

Command Rail is not equivalent to a `/playsound` music machine.

Every normal physical endpoint contains:

```text
AIR / REQUIRED CLEARANCE

NOTE BLOCK

INSTRUMENT SUPPORT BLOCK
```

and a command-controlled power mechanism.

The support block remains musically functional.

Example:

```text
AIR
NOTE BLOCK tuned to E4
WHITE WOOL
```

represents:

```text
Guitar E4
```

---

# 5. First-Class Linear Rail Mode

The simplest Command Rail layout is:

```text
LINEAR_RAIL
```

This is the layout originally proposed for BlockScore.

It places physical endpoints in a line.

Example side/top concept:

```text
NOTE BLOCKS

[N][N][N][N][N][N][N][N][N][N]

SUPPORT MATERIALS

[W][W][W][C][C][G][G][I][I][S]
```

where each support block determines the instrument.

Each note block is tuned to its required pitch.

A separate driver cell is positioned beside each endpoint.

---

# 6. Linear Rail Geometry

Default coordinate convention:

```text
X = endpoint progression

Y = vertical level

Z = depth / driver direction
```

For endpoint `i`:

```text
support:
(i, 0, 0)

note block:
(i, 1, 0)

clearance:
(i, 2, 0)

driver:
(i, 1, 1)
```

Conceptually:

```text
TOP VIEW

note rail
N N N N N N N N

driver rail
D D D D D D D D
```

Side view:

```text
     AIR
      |
NOTE BLOCK — DRIVER CELL
      |
SUPPORT BLOCK
```

This coordinate system may later be rotated during schematic generation.

---

# 7. Driver Rail

Each physical note-block endpoint receives one associated:

```text
DRIVER CELL
```

The command controller changes the driver cell in order to create a real redstone power transition at the note block.

The initial candidate driver behavior is:

```text
AIR
 ↓
REDSTONE BLOCK
 ↓
AIR
```

The transition:

```text
AIR → REDSTONE BLOCK
```

is intended to power the note block.

The transition:

```text
REDSTONE BLOCK → AIR
```

resets the endpoint.

Exact behavior must be verified by:

```text
CAL-003
Command Rail physical driver behavior
```

Until that test passes, the driver implementation is:

```text
PROVISIONAL
```

---

# 8. Driver Independence

Driver cells must not unintentionally activate neighboring endpoints.

The default geometry places the driver:

```text
one block behind its own note block
```

rather than between adjacent note blocks.

Conceptually:

```text
N N N N N

D D D D D
```

Each driver is directly adjacent only to its intended note block in the primary rail direction.

The physical QA pass must nevertheless test for:

```text
DIRECT_POWER_COLLISION

NEIGHBOR_UPDATE_COLLISION

QUASI_CONNECTIVITY_COLLISION

UNINTENDED_REDSTONE_CONNECTION
```

where relevant.

---

# 9. Endpoint

A reusable physical instrument unit is called an:

```text
ENDPOINT
```

Example:

```text
guitar_e4_01
```

An endpoint includes:

```yaml
endpoint_id:
instrument:
note_state:
sounding_pitch:
support_block:
note_position:
driver_position:
clearance_position:
pool_index:
bank:
status:
```

Example:

```yaml
endpoint_id: guitar_e4_01
instrument: guitar
note_state: 22
sounding_pitch: E4
support_block: minecraft:white_wool

note_position:
  x: 14
  y: 1
  z: 0

driver_position:
  x: 14
  y: 1
  z: 1

clearance_position:
  x: 14
  y: 2
  z: 0

pool_index: 1
bank: guitar
status: VALID
```

---

# 10. Endpoint Key

The basic reusable endpoint type is identified by:

```text
instrument + note_state
```

or equivalently for pitched instruments:

```text
instrument + sounding_pitch
```

Example:

```text
guitar + E4
```

is different from:

```text
harp + E4
```

even though the musical pitch is identical.

---

# 11. Endpoint Reuse

If a song plays:

```text
Guitar E4
```

100 times, Command Rail does not automatically construct 100 Guitar E4 note blocks.

It constructs a reusable endpoint pool.

Example:

```text
guitar_e4_01
```

may service many attacks over the song.

---

# 12. Endpoint Pool

Each:

```text
instrument + pitch
```

combination receives an:

```text
ENDPOINT POOL
```

Example:

```text
Guitar E4 pool

guitar_e4_01
guitar_e4_02
guitar_e4_03
```

The required pool size depends on:

- simultaneous attacks
- rapid repeated attacks
- reset time
- backend safety margin

---

# 13. Why Multiple Identical Endpoints Exist

Suppose the Minecraft Master requires:

```text
tick 100:
Guitar E4

tick 101:
Guitar E4
```

If one endpoint cannot safely:

```text
power
reset
power
```

within that interval, BlockScore can alternate physical endpoints.

Example:

```text
tick 100:
guitar_e4_01

tick 101:
guitar_e4_02

tick 102:
guitar_e4_01
```

This preserves timing without changing the music.

---

# 14. Simultaneous Duplicate Notes

Suppose three voices simultaneously require:

```text
Exposed Trumpet E4
```

The backend cannot represent three independent physical attacks using one note block.

It must allocate at least:

```text
trumpet_exposed_e4_01
trumpet_exposed_e4_02
trumpet_exposed_e4_03
```

unless the Minecraft Master intentionally merges those voices.

Backend limitations may not silently perform that merge.

---

# 15. Provisional Busy Window

Until direct Java 26.2 testing establishes minimum safe retrigger behavior, the allocator uses:

```text
busy_window_game_ticks = 2
```

This means an endpoint is conservatively considered unavailable for immediate reuse until its power-reset cycle has completed.

Status:

```text
PROVISIONAL
```

Calibration:

```text
CAL-004
Minimum same-endpoint retrigger interval
```

may reduce or alter this value.

---

# 16. Endpoint Allocation Algorithm

For every unique endpoint key:

```text
instrument + pitch
```

BlockScore collects all attack times.

Then it allocates attacks to the minimum endpoint pool that satisfies:

```text
simultaneity

busy window

reset safety
```

Conceptually:

```text
for each attack:
    find free endpoint

    if free endpoint exists:
        assign attack

    otherwise:
        create new endpoint
```

The allocation must be deterministic.

---

# 17. Allocation Priority

The allocator must never solve endpoint shortage by moving a P5 note to another tick unless timing compilation has already explicitly approved that movement.

Preferred solution:

```text
ADD ENDPOINT
```

before:

```text
CHANGE MUSIC
```

---

# 18. Instrument Banks

Endpoints may be grouped into:

```text
BANKS
```

Default banks:

```text
harp

bass

drums

guitar

flute

bell

chime

xylophone

iron_xylophone

cow_bell

didgeridoo

bit

banjo

pling

trumpet

trumpet_exposed

trumpet_weathered

trumpet_oxidized
```

Bank organization simplifies:

- construction
- debugging
- labels
- material counting
- spatial design
- endpoint lookup

---

# 19. Bank Pitch Ordering

Within a pitched instrument bank, endpoints should normally be sorted:

```text
lowest pitch
→
highest pitch
```

Example:

```text
Guitar

F#2
G2
G#2
A2
...
E4
F4
F#4
```

Only pitches actually required by the song need to exist unless the user requests a complete playable instrument bank.

---

# 20. Sparse Bank

Default Command Rail behavior is:

```text
SPARSE_BANK
```

Only required pitches are constructed.

Example:

If the song uses only:

```text
Bass F#1
Bass C#2
Bass E2
Bass B2
```

the bank contains four pitch types rather than all 25 states.

This minimizes physical size.

---

# 21. Full Bank

Optional mode:

```text
FULL_BANK
```

constructs every state:

```text
0 through 24
```

for selected instruments.

This is useful for:

- reusable music installations
- experimentation
- live composition
- generic sequencer builds

It is not the default for song-specific exports.

---

# 22. Literal Single-Line Rail

The user may request:

```text
LAYOUT = SINGLE_LINE
```

All song endpoints are placed into one continuous physical line.

Sorting order:

```text
instrument order
then pitch order
then pool index
```

Example:

```text
Bass F#1
Bass C#2
Bass C#2 copy 2
Guitar A3
Guitar E4
Trumpet E4
...
```

Instrument boundaries may use spacing or signs.

---

# 23. Single-Line Advantages

`SINGLE_LINE` is:

- simple
- easy to inspect
- easy to hand-build
- easy to understand
- easy to schematic
- ideal for early calibration
- ideal for small to medium songs

It should be BlockScore's first Command Rail test layout.

---

# 24. Single-Line Limitations

A long single rail may create:

- excessive listener distance
- large footprint
- inconvenient instrument grouping
- poor stereo balance
- long maintenance walks

Therefore the layout compiler must calculate:

```text
maximum_listener_distance
```

for every endpoint.

---

# 25. Folded Linear Rail

If a rail becomes too long, BlockScore may use:

```text
FOLDED_RAIL
```

Conceptually:

```text
N N N N N N N N
              ↓
N N N N N N N N
↓
N N N N N N N N
```

The physical note bank remains logically linear, but folds into parallel rows.

Command timing is unaffected because endpoint addressing uses coordinates rather than signal propagation.

---

# 26. Parallel Rails

Optional layout:

```text
PARALLEL_RAILS
```

uses one or more rows per instrument family.

Example:

```text
BASS RAIL
N N N N N

GUITAR RAIL
N N N N N N N

BRASS RAIL
N N N N N N

DRUM RAIL
N N N N
```

This is often easier to read and may fit within audible range more effectively.

---

# 27. Orchestra Layout

Future layout mode:

```text
ORCHESTRA_STAGE
```

places instrument families spatially like a performance ensemble.

Potential grouping:

```text
LOW / BASS

GUITARS / RHYTHMIC

BRASS

HIGH METALLIC

PERCUSSION
```

This mode prioritizes:

```text
spatial presentation
```

as well as mechanical function.

It should not be implemented until core Command Rail playback is proven.

---

# 28. Performance Origin

Every physical Command Rail build defines a:

```text
PERFORMANCE_ORIGIN
```

This is the intended primary listener position.

Example:

```yaml
performance_origin:
  x: 0
  y: 2
  z: -8
```

All physical audio-distance checks are calculated from this point.

---

# 29. Audible-Range QA

If a physical endpoint is too distant from the Performance Origin, BlockScore creates:

```text
AUDIBILITY_WARNING
```

Example:

```yaml
endpoint: bell_f7_01
distance: 53.8
priority: P4
warning: AUDIBILITY_WARNING
```

The backend may then suggest:

- fold rail
- move bank
- move listener
- duplicate spatial bank
- use enhanced digital assistance

It may not silently ignore the problem.

---

# 30. Controller Layer

Command Rail separates the physical instrument rail from its controller.

The controller may be:

```text
COMMAND_BLOCK_ONLY
```

or:

```text
COMMAND_BLOCK_DATAPACK
```

Both produce real physical note-block sounds.

---

# 31. Command-Block-Only Controller

`COMMAND_BLOCK_ONLY` requires no datapack.

It may use:

- repeating command block
- scoreboard clock
- chain command blocks
- endpoint trigger commands
- endpoint reset commands

This mode is useful for:

- prototypes
- small songs
- visible redstone/command installations
- calibration fixtures

---

# 32. Command-Block-Only Clock

A conceptual setup uses:

```text
scoreboard objective:
bs_tick

scoreboard holder:
#clock
```

Initialization:

```mcfunction
scoreboard objectives add bs_tick dummy
scoreboard players set #clock bs_tick 0
```

A repeating command block increments the clock while playback is active.

Exact control-state architecture will be specified during implementation.

---

# 33. Event Dispatch

A scheduled attack conceptually becomes:

```mcfunction
execute if score #clock bs_tick matches 127 run setblock <driver> minecraft:redstone_block
```

and its reset:

```mcfunction
execute if score #clock bs_tick matches 128 run setblock <driver> minecraft:air
```

These are implementation templates, not yet game-certified Command Rail commands.

Certification requires:

```text
CAL-003
CAL-004
CAL-005
```

---

# 34. Command Ordering

Within one game tick, controller commands may execute sequentially even though BlockScore treats their musical time as the same tick.

For a same-tick chord:

```text
tick 127
```

all endpoint activation commands belong to one logical onset group.

Command ordering inside that dispatch is not an intentional arpeggio.

---

# 35. Command Block Scaling

Command-block-only mode may require a large number of command blocks for long songs.

Therefore it is not necessarily the preferred production controller.

A complex composition may instead use:

```text
COMMAND_BLOCK_DATAPACK
```

---

# 36. Command-Block + Datapack Controller

In this mode, the physical build can use one or a few command blocks as the in-world controller while generated datapack functions handle the event schedule.

Conceptually:

```text
START BUTTON
    ↓
COMMAND BLOCK
    ↓
BlockScore datapack controller
    ↓
endpoint driver commands
    ↓
physical note blocks
```

This still qualifies as Command Rail because the sound source remains physical note blocks.

---

# 37. Recommended Production Controller

For complex songs, BlockScore's expected production mode is:

```text
COMMAND_BLOCK_DATAPACK
```

because it offers:

- compact control hardware
- easier generated code
- easier revisions
- cleaner pause/reset
- cleaner section seeking
- more scalable event dispatch

The physical instrument rail remains unchanged.

---

# 38. Controller Clock

The canonical generated schedule is:

```text
game_tick → actions
```

Example:

```yaml
127:
  activate:
    - guitar_e4_01
    - bass_c2_01
    - basedrum_04_01

128:
  deactivate:
    - guitar_e4_01
    - bass_c2_01
    - basedrum_04_01

  activate:
    - guitar_g4_01
```

The controller implementation consumes this schedule.

---

# 39. Controller State

Future controller state should include:

```text
STOPPED

PLAYING

PAUSED
```

Optional later states:

```text
SEEKING

LOADING

LOOPING
```

---

# 40. Start

Starting playback should:

```text
reset song clock

reset endpoint drivers

set state PLAYING

begin clock advancement
```

A constant controller preroll is allowed.

Preroll is not musical timing error.

---

# 41. Stop

Stopping playback must:

```text
stop clock advancement

reset all active drivers

return controller to STOPPED
```

No endpoint should remain powered after stop.

---

# 42. Reset

Reset returns:

```text
song_tick = 0
```

and clears:

```text
active endpoint states
```

Reset should be safe from either:

```text
STOPPED
```

or:

```text
PAUSED
```

and eventually from:

```text
PLAYING
```

if implementation permits.

---

# 43. Pause

Pause should stop the song clock.

Physical note samples already triggered may continue their natural decay.

Pause does not retroactively stop sound unless enhanced digital behavior is explicitly used.

---

# 44. Resume

Resume continues from the preserved song tick.

Before resume, the controller must confirm that no stale driver remains active.

---

# 45. Seeking

Future Command Rail should support:

```text
seek to tick

seek to measure

seek to section
```

Because the song schedule uses absolute ticks, seeking does not require replaying previous events.

However, sustained/retrigger states may require reconstruction.

Initial implementations may omit seeking.

---

# 46. Looping

A Command Rail song may define:

```text
loop_start_tick

loop_end_tick
```

At loop end:

```text
clock → loop_start_tick
```

All active drivers must be in a known valid state at the loop boundary.

Loop-seam timing is validated by the timing backend.

---

# 47. Endpoint Trigger Actions

Each physical attack produces at least:

```text
ACTIVATE
```

and:

```text
RESET
```

actions.

Canonical internal form:

```yaml
action:
  type: ACTIVATE_ENDPOINT
  tick: 127
  endpoint: guitar_e4_01
```

and:

```yaml
action:
  type: RESET_ENDPOINT
  tick: 128
  endpoint: guitar_e4_01
```

---

# 48. Physical versus Digital Event Origin

Every Command Rail event must identify:

```text
origin = PHYSICAL
```

or:

```text
origin = DIGITAL_ASSIST
```

For:

```text
COMMAND_RAIL_PHYSICAL
```

all normal musical events must be:

```text
PHYSICAL
```

---

# 49. Enhanced Mode

`COMMAND_RAIL_ENHANCED` allows selective digital supplementation.

Examples:

- impossible sustain
- non-note-block FX
- spatial sound outside bank range
- special ambience
- sound-stop behavior
- rare register problems

Digital assistance must be explicit.

---

# 50. Digital Assist Must Not Replace Physical Playback Silently

If a physical endpoint could not be used and a command sound replaced it, the event must report:

```text
PHYSICAL_FALLBACK_TO_DIGITAL
```

The QA report must include the count and identity of all such events.

---

# 51. Physical Percentage

Enhanced Command Rail should report:

```text
physical_event_percentage
```

Example:

```text
total attacks: 8,420

physical attacks: 8,301

digital assists: 119

physical percentage: 98.59%
```

This lets the user judge how physical the result really is.

---

# 52. Instrument Material Count

Command Rail material reporting should include:

```text
note blocks

support blocks by block type

driver cells

controller command blocks

decorative/label blocks

optional maintenance floor
```

Example:

```text
Note Block × 87

White Wool × 21

Oak Planks × 14

Copper Block × 8

Weathered Copper × 6

Redstone Block:
temporary command-created state,
not necessarily required as placed inventory
```

---

# 53. Command-Created Driver Blocks

If the driver works by `/setblock`:

```text
minecraft:redstone_block
```

the driver blocks are runtime states rather than permanently placed construction materials.

Material reports should distinguish:

```text
PLACED MATERIALS
```

from:

```text
RUNTIME GENERATED BLOCK STATES
```

---

# 54. Endpoint Labels

Optional endpoint labels can show:

```text
instrument

pitch

note state

endpoint pool index
```

Example:

```text
Guitar
E4
22
#2
```

Labels are useful during:

- calibration
- development
- debugging
- manual tuning

Production builds may omit them.

---

# 55. Manual Tuning Mode

For hand-built Command Rails, BlockScore can generate:

```text
TUNING SHEET
```

Example:

| Endpoint | Instrument | Pitch | Clicks |
|---|---|---:|---:|
| guitar_e4_01 | Guitar | E4 | 22 |
| bass_c2_01 | Bass | C2 | 6 |

For schematic builds, the note state should be encoded directly.

---

# 56. Endpoint Determinism

Endpoint naming and placement must be deterministic.

Given identical:

```text
Minecraft Master

profile

Command Rail settings

allocator version
```

BlockScore should create the same:

```text
endpoint IDs

pool sizes

endpoint ordering

coordinates
```

This simplifies revisions and schematic diffs.

---

# 57. Stable Endpoint IDs

If a later song revision adds a new pitch, existing endpoint IDs should remain stable where possible.

Example:

Before:

```text
guitar_a3_01
guitar_e4_01
```

After adding C4:

```text
guitar_a3_01
guitar_c4_01
guitar_e4_01
```

Do not arbitrarily rename existing endpoints.

---

# 58. Physical Bank Revision

When the Master changes, BlockScore should calculate:

```text
ENDPOINT DIFF
```

Example:

```text
ADD:
trumpet_g4_01

REMOVE:
none

POOL GROW:
guitar_e4
1 → 2

UNCHANGED:
82 endpoints
```

This allows a player to modify an existing build rather than rebuild everything.

---

# 59. Song Schedule Revision

Endpoint layout and event schedule are independent.

A musical revision may change:

```text
timing only
```

without changing any physical endpoint.

This is one of Command Rail's largest advantages.

---

# 60. Controller-Only Revision

If the song changes but uses the same:

```text
instrument + pitch
```

set and same pool demand, the physical rail may remain completely unchanged.

Only the controller schedule needs replacement.

---

# 61. Endpoint-Only Revision

A new instrument or pitch may require additional endpoints while most of the controller remains structurally unchanged.

BlockScore should report this explicitly.

---

# 62. Layout Modes

Initial planned layout enum:

```text
SINGLE_LINE

FOLDED_RAIL

PARALLEL_RAILS

CUSTOM
```

Future:

```text
ORCHESTRA_STAGE
```

Default test mode:

```text
SINGLE_LINE
```

---

# 63. Layout Options

A Command Rail project may define:

```yaml
layout:
  type: SINGLE_LINE

  origin:
    x: 0
    y: 0
    z: 0

  direction: EAST

  instrument_gap: 1

  maintenance_aisle: true

  labels: true
```

---

# 64. Instrument Gap

Optional empty positions between banks make rails easier to read.

Example:

```text
Bass endpoints
...
GAP
Guitar endpoints
...
GAP
Trumpet endpoints
```

Default:

```text
1 block
```

for development builds.

Production compact mode may use:

```text
0
```

if safe.

---

# 65. Maintenance Space

A generated rail should permit the player to inspect and modify endpoints.

Development layout should provide a:

```text
MAINTENANCE AISLE
```

unless the user specifically requests maximum compression.

---

# 66. Driver Access

Driver cells must remain accessible to:

```text
commands
```

regardless of whether the player can physically walk beside them.

Player maintenance access and command addressability are separate requirements.

---

# 67. Block Coordinate Registry

Every generated endpoint receives fixed world-relative coordinates.

Example:

```yaml
guitar_e4_01:
  note: [14, 1, 0]
  support: [14, 0, 0]
  driver: [14, 1, 1]
```

Schematic placement may later translate the entire build by an origin offset.

---

# 68. Relative Coordinates

The canonical build plan should store:

```text
relative coordinates
```

rather than absolute world coordinates.

This allows the schematic or structure to be placed anywhere.

---

# 69. World Placement

At installation time:

```text
world_coordinate
=
structure_origin
+
relative_coordinate
```

The controller must use coordinates consistent with actual placement.

A datapack controller may use:

- fixed absolute positions generated at install time
- marker entities
- storage-defined origin
- function macros
- other future addressing strategies

Initial implementation may use fixed coordinates.

---

# 70. Controller Placement

The controller may be:

```text
adjacent

underground

behind the rail

remote
```

because commands do not require physical signal propagation to the endpoints.

The listener should not need to hear or see the controller.

---

# 71. Visual Controller Option

Some users may prefer a visible:

```text
SEQUENCER WALL
```

showing:

- play
- stop
- pause
- reset
- current tick
- current measure
- section

This is a UI layer rather than core playback logic.

---

# 72. Debug Mode

Development Command Rails should support:

```text
DEBUG_MODE
```

Potential debug output:

```text
current tick

current measure

events triggered

endpoint IDs

active drivers

collision warnings
```

Production builds may disable it.

---

# 73. Solo Bank

Debug tooling should eventually support:

```text
SOLO BANK
```

Example:

```text
play only Guitar bank
```

This helps test arrangements.

---

# 74. Mute Bank

Similarly:

```text
MUTE BANK
```

can temporarily suppress an instrument family without changing the Master.

Useful for:

- debugging
- comparison
- listening tests

---

# 75. Endpoint Test

Every endpoint should be individually triggerable in development mode.

Example:

```text
TEST guitar_e4_01
```

This verifies:

- pitch
- support block
- driver
- address
- clearance
- sound

---

# 76. Bank Sweep Test

Each pitched bank should support a test that plays endpoints from low to high.

Example:

```text
F#2
G2
G#2
...
F#4
```

This makes tuning errors easy to detect.

---

# 77. Chord Test

Calibration should include simultaneous endpoint activation.

Example:

```text
guitar_c4_01
guitar_e4_01
guitar_g4_01
```

Purpose:

```text
CAL-005
same-tick synchronization
```

---

# 78. Rapid Retrigger Test

Calibration should test:

```text
same instrument
same pitch
rapid attacks
```

using:

```text
one endpoint
```

and:

```text
alternating endpoint pools
```

This determines actual allocator requirements.

---

# 79. Performance Requirements

Command Rail should target stable operation at:

```text
20 TPS
```

Large event bursts must be measured for command-processing impact.

Future QA may include:

```text
max commands per tick

mean commands per tick

95th percentile commands per tick

maximum simultaneous physical attacks
```

---

# 80. Command Density

A dense chord may require many commands during one game tick.

Example:

```text
activate 20 endpoints
```

followed by:

```text
reset 20 endpoints
```

the next tick.

The backend must report command density rather than assuming unlimited performance.

---

# 81. Command Density Warning

Future configurable threshold:

```text
COMMAND_DENSITY_WARNING
```

Example:

```yaml
tick: 824
actions: 73
warning: COMMAND_DENSITY_WARNING
```

Actual safe thresholds must be benchmarked.

---

# 82. Chunk Loading

A physical endpoint outside loaded simulation range may fail to behave as intended.

Command Rail layouts should normally keep:

```text
controller
instrument rail
listener
```

within an intentionally loaded performance area.

Large distributed layouts require explicit chunk-loading design.

---

# 83. Chunk Boundary Awareness

The layout compiler should record chunk coordinates for:

```text
endpoints

controller

performance origin
```

A small Command Rail should preferably avoid unnecessary spread across many chunks.

This is a build optimization, not a musical requirement.

---

# 84. Physical Safety Rules

A generated rail must not place:

```text
solid block above normal note endpoint

incorrect support material

driver inside note-block clearance

two endpoints in same position

driver in another endpoint's position

controller hardware inside required bank geometry
```

---

# 85. Copper Trumpet Safety

Trumpet-family endpoints require additional checks:

```text
correct oxidation stage

stability policy

CAL-001 status

CAL-002 status
```

Until waxed-copper equivalence is verified, the backend should report:

```text
COPPER_STABILITY_PENDING
```

for production trumpet rails that use unwaxed support blocks.

---

# 86. Range Verification

An endpoint may only be constructed if:

```text
note_state 0..24
```

and the selected pitch mapping is valid for the instrument registry.

A provisional trumpet register may still generate an endpoint if project settings allow provisional science.

It must carry:

```text
TRUMPET_CALIBRATION_PENDING
```

---

# 87. Provisional Science Policy

Command Rail project configuration should eventually allow:

```text
allow_provisional_mechanics: true | false
```

If false:

```text
PROVISIONAL
```

instrument behavior cannot be used in a certified backend.

If true:

the build may be generated with warnings.

---

# 88. Build Certification Levels

Command Rail outputs should use:

```text
DESIGNED

OFFLINE_VALIDATED

GAME_TESTED

USER_APPROVED
```

A generated command schedule is not automatically GAME_TESTED.

---

# 89. Command Rail QA

Every Command Rail build must check:

```text
ENDPOINT_COUNT_VALID

ENDPOINT_IDS_UNIQUE

POSITIONS_UNIQUE

NOTE_STATES_VALID

SUPPORT_BLOCKS_VALID

CLEARANCE_VALID

DRIVER_POSITIONS_VALID

POOL_CAPACITY_VALID

EVENTS_FULLY_ASSIGNED

NO_UNDECLARED_DIGITAL_EVENTS

TIMING_SCHEDULE_VALID

AUDIBILITY_CHECKED

COMMAND_DENSITY_CHECKED

CALIBRATION_DEPENDENCIES_REPORTED
```

---

# 90. Endpoint Assignment QA

Every physical Master attack must map to:

```text
exactly one endpoint
```

unless:

```text
the Master explicitly contains layered duplicate attacks
```

No attack may disappear.

No attack may be assigned twice accidentally.

---

# 91. Pool Capacity QA

For each endpoint pool:

```text
required_concurrency
<=
allocated_pool_size
```

must hold for the entire song.

This includes busy-window overlap, not just exact same-tick simultaneity.

---

# 92. Driver-State Simulation

Offline validation should simulate:

```text
driver state by game tick
```

for every endpoint.

Invalid example:

```text
tick 100:
ACTIVATE

tick 101:
ACTIVATE
```

without an intervening valid reset.

This should fail unless calibration proves such behavior legal.

---

# 93. Schedule Completeness

Every generated endpoint action must correspond to a valid song attack or required reset.

The controller must not generate unexplained note attacks.

---

# 94. Stuck Driver Detection

Simulation should verify:

```text
no driver remains powered
```

after:

```text
song end

stop

reset

loop boundary
```

unless intentionally specified.

---

# 95. Command Rail Loss Report

Command Rail should report:

```text
timing quantization

endpoint duplication

provisional mechanics

digital assists

audibility warnings

command-density warnings

layout compromises
```

Endpoint duplication itself is not musical loss.

It is a build cost.

---

# 96. Command Rail Metrics

A compiled build should eventually report:

```text
unique instrument-pitch combinations

physical endpoint count

maximum pool size

total musical attacks

total activate actions

total reset actions

maximum simultaneous attacks

maximum commands per tick

rail length

bank count

material count

maximum listener distance

physical event percentage
```

---

# 97. Compression Ratio

Command Rail may calculate:

```text
compression_ratio =
total musical attacks
/
physical endpoint count
```

Example:

```text
8,000 musical attacks
80 physical endpoints

compression ratio = 100:1
```

This measures physical reuse.

It is not a quality score.

---

# 98. Comparison with Redstone Physical

For the same Minecraft Master, BlockScore should eventually report:

| Metric | Redstone Physical | Command Rail |
|---|---:|---:|
| note blocks | | |
| repeaters | | |
| command blocks | | |
| unique endpoints | | |
| footprint | | |
| max timing error | | |
| revision difficulty | | |

This lets the user choose the backend based on actual tradeoffs.

---

# 99. Expected Strengths

Command Rail should generally outperform traditional Redstone Physical in:

- compactness
- timing resolution
- revision simplicity
- high polyphony
- odd meter
- tuplets
- rapidly changing patterns
- long compositions
- reusable physical instrumentation

---

# 100. Expected Tradeoffs

Command Rail requires:

- commands enabled
- more backend logic
- controller setup
- coordinate management
- potentially a datapack for large production songs
- careful calibration of physical trigger behavior

It is not intended to replace traditional note-block builds in every context.

---

# 101. Mars TEST-001A Command Rail Target

Mars TEST-001A should compile first to:

```text
LAYOUT:
SINGLE_LINE
```

with:

```text
SPARSE_BANKS
```

and:

```text
COMMAND_RAIL_PHYSICAL
```

No digital assistance should be required for the initial physical test unless explicitly approved.

---

# 102. Mars Test Questions

TEST-001A should answer:

```text
How many unique physical endpoints are required?

How many duplicate endpoint pools are required by the ostinato?

Can the opening rhythm be represented at 20 TPS without unacceptable loss?

Does rapid retriggering require alternating endpoints?

How long is the literal single-line rail?

Does the entire rail remain within practical listening distance?

How many commands occur on the densest tick?

Does Command Rail preserve the 5/4 identity better than Redstone Physical?
```

---

# 103. Mars Acceptance Criteria

Command Rail TEST-001A passes only if:

```text
all P5 attacks preserved

no undeclared digital sounds

all physical pitches legal

all endpoints use correct support blocks

5/4 timing identity preserved

no endpoint pool overflow

no stuck drivers

same-tick chords remain logically simultaneous

timing error report complete

calibration dependencies clearly reported
```

---

# 104. Future Tool Test

Command Rail is expected to be particularly useful for Tool-style material because it can represent:

```text
odd meters

riff cycles across barlines

polyrhythm

rapid repeated attacks

independent bass/drum cycles

large common-reset patterns
```

without encoding every rhythmic relationship as physical repeater distance.

The Master timing model remains authoritative.

---

# 105. Future Live Sequencer Possibility

A full endpoint bank could later support:

```text
interactive composition

live step sequencing

MIDI-to-Command-Rail playback

in-game editing

instrument soloing

pattern looping
```

These are future possibilities.

They are not required for BlockScore's initial song compiler.

---

# 106. Planned Command Rail Output Files

Future compiled song packages may include:

```text
command-rail-plan.json

endpoint-map.json

event-schedule.json

materials.json

warnings.json

build.nbt

build.litematic

datapack/
```

Exact formats will be defined by later schemas.

---

# 107. Canonical Command Rail Plan

Conceptually:

```yaml
profile: java-26.2
backend: COMMAND_RAIL_PHYSICAL

layout:
  type: SINGLE_LINE

performance_origin:
  x: 0
  y: 2
  z: -8

endpoints:
  - endpoint_id: guitar_e4_01
    instrument: guitar
    pitch: E4
    note_state: 22

schedule:
  127:
    activate:
      - guitar_e4_01

  128:
    reset:
      - guitar_e4_01
```

The formal schema will be added later.

---

# 108. Implementation Stages

Recommended implementation order:

```text
1. endpoint model

2. endpoint requirement analysis

3. pool allocator

4. SINGLE_LINE layout

5. coordinate registry

6. schedule compiler

7. offline driver-state simulator

8. command-block controller generator

9. Command Rail QA

10. materials report

11. structure/schematic output

12. datapack controller

13. advanced layouts
```

---

# 109. Calibration Before Optimization

Do not optimize the endpoint allocator aggressively until:

```text
CAL-003
CAL-004
CAL-005
```

have been game-tested.

Correct physical behavior comes before minimum endpoint count.

---

# 110. No Fake Physical Playback Rule

Never report:

```text
physical note block playback verified
```

because commands or `/playsound` were generated successfully.

Physical verification requires actual Minecraft testing.

---

# 111. Governing Command Rail Rule

> Commands control the orchestra. The note blocks are the orchestra.

The controller may become sophisticated.

The physical endpoint bank may become compact.

The layout may eventually become visually elaborate.

But in `COMMAND_RAIL_PHYSICAL`, every normal musical attack must ultimately come from a real, correctly tuned, correctly supported Minecraft note block.
