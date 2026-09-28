# BlockScore Digital Playback Backend

## Minecraft Java Edition 26.2

This document defines the BlockScore pure digital playback backend.

Backend identifier:

```text
DIGITAL_PLAYBACK
```

Digital Playback uses Minecraft commands and/or a generated data pack to play sound events directly.

It does not require a physical note block for each musical event.

The Minecraft Master remains the musical source of truth.

---

# 1. Core Concept

Digital Playback compiles:

```text
MINECRAFT MASTER
        ↓
DIGITAL TIMING
        ↓
SOUND EVENTS
        ↓
GAME-TICK SCHEDULE
        ↓
COMMANDS / FUNCTIONS
        ↓
MINECRAFT AUDIO
```

No physical note-block machine is required.

---

# 2. Governing Rule

> Digital Playback may remove physical construction constraints, but it may not silently rewrite the Minecraft Master.

The digital backend has more freedom than physical backends.

That freedom must be used to preserve music, not obscure changes.

---

# 3. Backend Identity

Digital Playback is distinct from:

```text
REDSTONE_PHYSICAL
```

and:

```text
COMMAND_RAIL_PHYSICAL
```

because the final sound originates from command-triggered sound events.

---

# 4. Relationship to Command Rail Enhanced

`COMMAND_RAIL_ENHANCED` may use Digital Playback for selected events.

Those events are labeled:

```text
DIGITAL_ASSIST
```

Pure `DIGITAL_PLAYBACK` does not need that label because digital sound is the expected playback method.

---

# 5. Digital Playback Modes

Initial digital modes:

```text
NOTE_BLOCK_FAITHFUL

EXPANDED_DIGITAL
```

---

# 6. Note-Block-Faithful Mode

`NOTE_BLOCK_FAITHFUL` attempts to reproduce the Minecraft Master using the same note-block sound events used by the physical instrument system.

Example:

```text
minecraft:block.note_block.guitar
```

with the appropriate pitch multiplier.

This mode is the preferred reference backend for comparing physical output.

---

# 7. Expanded Digital Mode

`EXPANDED_DIGITAL` may use additional Minecraft sound events where explicitly arranged.

Possible uses:

- stronger percussion
- ambience
- effects
- special impacts
- extended orchestration
- non-note-block sounds

Such substitutions belong to the Minecraft Master or an explicitly approved digital arrangement layer.

---

# 8. Physical Instruments Are Still Relevant

Even though no support block is required for digital playback, BlockScore still stores:

```text
instrument
```

because the Minecraft Master may specify:

```text
guitar

bass

trumpet

pling
```

The backend then looks up the corresponding sound event.

---

# 9. Registry Authority

Digital Playback obtains note-block sound events from:

```text
data/java-26.2/instruments.json
```

It should not duplicate instrument-to-sound mappings in backend code.

---

# 10. Basic Java Playsound Model

Current Java syntax supports:

```text
playsound <sound> [<source>] [<targets>] [<pos>] [<volume>] [<pitch>] [<minVolume>]
```

BlockScore should normally emit explicit values rather than depend on optional defaults.

---

# 11. Canonical Note-Block Command Shape

Conceptually:

```mcfunction
playsound minecraft:block.note_block.guitar block @a 0 64 0 1 1 0
```

Fields:

```text
sound:
minecraft:block.note_block.guitar

source:
block

targets:
@a

position:
0 64 0

volume:
1

pitch:
1

minimum volume:
0
```

---

# 12. Mixer Source

Java sound sources include categories such as:

```text
master
music
record
weather
block
hostile
neutral
player
ambient
voice
ui
```

For note-block-faithful playback, BlockScore default is:

```text
block
```

---

# 13. Configurable Mixer Source

Projects may override:

```yaml
digital:
  mixer_source: block
```

Possible reasons:

- dedicated volume control
- map design
- cinematic playback
- separation from environmental block sounds

Changing mixer source does not change musical pitch.

---

# 14. Target Players

The command must identify who hears the event.

Typical targets:

```text
@a
```

or a selected player/group.

The target strategy belongs to project configuration.

---

# 15. Single-Listener Mode

Mode:

```text
SINGLE_LISTENER
```

targets one intended listener.

Useful for:

- testing
- solo worlds
- reference playback
- arrangement work

---

# 16. Audience Mode

Mode:

```text
AUDIENCE
```

targets multiple players.

Spatial and attenuation behavior must remain meaningful for every targeted player.

---

# 17. Digital Event

A canonical digital event should eventually contain:

```yaml
event_id:
source_event_id:
game_tick:
sound_event:
mixer_source:
targets:
position_mode:
position:
volume:
pitch_multiplier:
minimum_volume:
priority:
spatial_group:
stop_policy:
status:
```

---

# 18. Example Digital Event

```yaml
event_id: digital-00124
source_event_id: event-00124

game_tick: 127

sound_event: minecraft:block.note_block.guitar
mixer_source: block

targets: "@a"

position_mode: WORLD_FIXED

position:
  x: 0
  y: 64
  z: 0

volume: 1.0
pitch_multiplier: 1.781797
minimum_volume: 0.0

priority: P4
status: VALID
```

---

# 19. Note-State Pitch Formula

For normal note-block events:

```text
pitch_multiplier =
2 ^ ((note_state - 12) / 12)
```

---

# 20. Note-State Range

Valid normal note states:

```text
0..24
```

produce multipliers:

```text
0.5..2.0
```

This fits the effective normal Java `/playsound` note-block pitch span.

---

# 21. Reference States

```text
state 0  = 0.5

state 12 = 1.0

state 24 = 2.0
```

---

# 22. Digital Pitch Equivalence

For a normal note-block instrument:

```text
PHYSICAL:
instrument + note_state
```

should correspond musically to:

```text
DIGITAL:
instrument sound_event + pitch_multiplier
```

assuming the same underlying sound event.

---

# 23. Digital Pitch Is Not Arbitrary Absolute Pitch

A pitch multiplier of:

```text
1.0
```

does not mean the same musical note for every sound event.

The sample's original register matters.

Therefore BlockScore must not derive absolute pitch from multiplier alone.

---

# 24. Note-Block Register Model

Absolute note names remain determined by:

```text
instrument register
+
note state
```

according to the versioned instrument profile.

---

# 25. Non-Note-Block Sounds

For arbitrary Minecraft sounds:

```text
pitch_multiplier
```

does not automatically map to BlockScore note-block register rules.

Those sounds require explicit arrangement metadata.

---

# 26. Pitch and Playback Speed

Changing `/playsound` pitch also changes playback speed and therefore apparent sample duration.

This matters for:

- sustain
- percussion tails
- high notes
- low notes
- layered attacks

Digital Playback must not assume pitch shifting changes frequency while preserving sample duration.

---

# 27. Sound Event Randomness

Some Minecraft sound events may select among multiple underlying samples.

Therefore:

```text
sound_event
```

does not always imply one deterministic audio file.

Normal note-block events should be treated according to their actual registered behavior.

Arbitrary expanded-digital sounds require review.

---

# 28. Dynamics

Digital Playback may represent dynamics using:

```text
volume
```

but BlockScore must distinguish:

```text
musical loudness
```

from:

```text
audible range
```

because Minecraft's volume argument affects both behavior and attenuation.

---

# 29. Volume Below One

Values below:

```text
1.0
```

can reduce perceived loudness.

This is useful for musical dynamics.

---

# 30. Volume Above One

Values greater than:

```text
1.0
```

should not be interpreted as ordinary musical amplification.

In Java command playback, values above one primarily expand audible range rather than indefinitely increasing source loudness.

---

# 31. Dynamics Range

For normal musical dynamics, BlockScore should initially prefer:

```text
0.0 < volume <= 1.0
```

unless range extension is intentionally required.

---

# 32. Dynamic Mapping

Source dynamics such as:

```text
pp
p
mp
mf
f
ff
```

should eventually map through a configurable response curve.

Do not assume a linear conversion.

---

# 33. Initial Dynamic Policy

Until listening tests define a preferred curve:

```text
dynamic volume mapping
=
PROVISIONAL
```

The Master should preserve the original dynamic marking separately.

---

# 34. Velocity-Like Accent

An accented attack may use a higher digital volume than surrounding notes.

Example:

```text
normal:
0.72

accent:
0.90
```

Exact values remain arrangement parameters.

---

# 35. Minimum Volume

Java `/playsound` supports a minimum-volume parameter for listeners outside the normal audible region.

BlockScore should treat this as:

```text
SPATIAL / ACCESSIBILITY CONTROL
```

rather than ordinary dynamics.

---

# 36. Minimum Volume Default

Default:

```text
minimum_volume = 0
```

for spatially faithful playback.

---

# 37. Forced Audibility

A project may request:

```text
FORCED_AUDIBILITY
```

where minimum volume is greater than zero.

This reduces the significance of true source distance.

It must therefore be explicit.

---

# 38. Digital Position

Every event has a sound-source position.

BlockScore supports multiple positioning strategies.

---

# 39. World Fixed

```text
WORLD_FIXED
```

uses explicit world coordinates.

Example:

```yaml
position:
  x: 120
  y: 72
  z: -40
```

Useful for:

- map installations
- stages
- environmental music
- fixed performances

---

# 40. Stage Relative

```text
STAGE_RELATIVE
```

stores a position relative to a performance origin.

Example:

```yaml
relative_position:
  x: -4
  y: 1
  z: 3
```

At installation time this becomes a world position.

---

# 41. Listener Centered

```text
LISTENER_CENTERED
```

plays the sound at or near each listener.

This minimizes distance attenuation.

It sacrifices world-fixed spatial placement.

---

# 42. Listener Relative

```text
LISTENER_RELATIVE
```

positions a sound at an offset relative to each listener.

This can simulate headphones-like stereo staging.

Example:

```text
guitar:
left

brass:
right

bass:
center
```

---

# 43. Mono Digital Reference

The simplest reference mode is:

```text
MONO_REFERENCE
```

All events originate from one common point.

This is useful for comparing:

- timing
- harmony
- arrangement

without spatial variables.

---

# 44. Stereo Digital Stage

Mode:

```text
STEREO_STAGE
```

places instrument families at different horizontal positions.

Possible layout:

```text
LEFT
guitar / upper percussion

CENTER
bass / core rhythm

RIGHT
brass / secondary voices
```

Exact placement is an arrangement choice.

---

# 45. Orchestra Stage

Future mode:

```text
ORCHESTRA_STAGE
```

can map Minecraft instruments to a wider spatial ensemble.

It should use the same spatial metadata as Command Rail's future orchestra layout where practical.

---

# 46. Spatial Group

Events may belong to:

```text
spatial_group
```

Example:

```yaml
spatial_group: brass_left
```

A spatial group maps to a configured position.

---

# 47. Spatial Position Is Not Pitch

Spatial layout must not alter:

```text
pitch
```

or:

```text
timing
```

unless an explicit effect is intended.

---

# 48. Digital Timing Grid

Default Digital Playback timing grid:

```text
20 game ticks per second
```

under normal 20 TPS simulation.

One game tick is nominally:

```text
50 ms
```

---

# 49. Timing Authority

All timing math comes from:

```text
docs/TIMING_MODEL.md
```

The Digital backend consumes compiled:

```text
game_tick
```

positions.

---

# 50. Absolute Timing

Events are quantized from absolute Master time.

Never compute:

```text
next tick
=
previous rounded tick
+
rounded duration
```

---

# 51. Same-Tick Chords

Every event in one digital onset group receives the same:

```text
game_tick
```

---

# 52. Logical Simultaneity

Commands within one function execute sequentially.

BlockScore still treats commands emitted during the same game tick as:

```text
LOGICALLY_SIMULTANEOUS
```

unless future testing identifies audible command-order problems.

---

# 53. Same-Tick Ordering

Within one onset, command generation should use deterministic ordering.

Default ordering may be:

```text
priority
instrument
pitch
event_id
```

This is for reproducibility, not musical arpeggiation.

---

# 54. Timing Controller

Recommended production controller:

```text
DATAPACK_TICK_CONTROLLER
```

It uses a persistent song tick.

---

# 55. Song Tick

Conceptual scoreboard state:

```text
bs_song_tick
```

increments once per active game tick.

---

# 56. Tick Dispatch

Conceptually:

```text
song tick 127
→ run events assigned to tick 127

song tick 128
→ run events assigned to tick 128
```

---

# 57. Persistent Tick Controller

Dense songs should prefer a persistent tick controller rather than scheduling every individual note as a separate future task.

Advantages:

- deterministic timeline
- easier pause
- easier stop
- easier seek
- easier loop
- simpler state tracking

---

# 58. Schedule Command

Java provides function scheduling mechanisms.

BlockScore may use them for:

- coarse startup
- deferred cleanup
- non-dense utility behavior

They are not the preferred per-note engine for complex music.

---

# 59. Command-Block Digital Mode

Small tests may use:

```text
COMMAND_BLOCK_DIGITAL
```

with repeating and chain command blocks.

This is useful for:

- quick prototypes
- calibration
- small songs

---

# 60. Datapack Digital Mode

Production default:

```text
DATAPACK_DIGITAL
```

The in-world structure may contain only:

- start control
- optional stop/pause controls
- optional display

The event schedule lives in generated functions.

---

# 61. Controller State

Digital playback should support:

```text
STOPPED

PLAYING

PAUSED
```

Future:

```text
SEEKING

LOOPING
```

---

# 62. Start

Starting should:

```text
reset song tick

clear stale controller state

set PLAYING

begin dispatch
```

---

# 63. Stop

Stopping should:

```text
stop tick advancement

set STOPPED

optionally stop managed sounds
```

The sound-stop policy must be explicit.

---

# 64. Pause

Pause stops future event dispatch.

Already-started samples may continue naturally.

---

# 65. Pause Is Not Audio Freeze

Digital Pause does not mean:

```text
freeze every currently playing audio sample in place
```

Minecraft's normal sound commands do not provide arbitrary sample freeze/resume semantics.

---

# 66. Resume

Resume continues dispatch from the saved song tick.

Naturally decayed sounds are not reconstructed automatically unless a future sustain-state system explicitly does so.

---

# 67. Reset

Reset returns:

```text
song_tick = 0
```

and clears playback state.

Optional stop commands may clear managed sound categories/events.

---

# 68. Seeking

Digital Playback can more easily support:

```text
seek to tick

seek to measure

seek to section
```

than physical backends.

However sustained state may need reconstruction.

---

# 69. Seek Policy

Initial seek may use:

```text
ATTACK_ONLY_SEEK
```

meaning playback begins with attacks occurring at or after the destination.

Future:

```text
STATEFUL_SEEK
```

may reconstruct sustained textures.

---

# 70. Looping

Digital loops define:

```text
loop_start_tick

loop_end_tick
```

When the controller reaches the end:

```text
song_tick → loop_start_tick
```

---

# 71. Loop Seam

Timing QA must evaluate:

```text
last attack before loop end
→
first attack after loop start
```

using the same IOI rules defined by the timing model.

---

# 72. Natural Sound Duration

`/playsound` triggers a sound sample.

It is not a general MIDI note gate.

BlockScore must distinguish:

```text
ATTACK TIME
```

from:

```text
SOURCE NOTE DURATION
```

---

# 73. Digital Sustain

Possible strategies:

```text
NATURAL_DECAY

RETRIGGER

TREMOLO

LAYER

ALTERNATE_SOUND

CUSTOM_RESOURCE_SOUND

DIGITAL_REDUCTION
```

---

# 74. Natural Decay

Short source notes may simply trigger the sound once.

This is closest to physical note-block behavior.

---

# 75. Retrigger Sustain

A long tone may be approximated with repeated attacks.

This must be arranged musically because retriggering can sound rhythmic.

---

# 76. Tremolo Sustain

Repeated fast attacks may intentionally represent:

```text
TREMOLO
```

rather than pretending to be seamless sustain.

---

# 77. Layered Sustain

Multiple timbres may overlap to create a longer apparent texture.

This increases event count and sound density.

---

# 78. Stop Sound Command

Java provides:

```text
stopsound <targets> [<source>] [<sound>]
```

This is useful for stopping managed sound categories/events.

---

# 79. Stopsound Limitation

BlockScore must not treat `/stopsound` as a unique MIDI-style note-off for one specific playback instance.

If several voices are using the same:

```text
sound event
+
mixer source
```

a stop command may affect more than the intended musical note.

---

# 80. Default Note-Off Policy

For normal note-block sound events:

```text
NO_EXPLICIT_NOTE_OFF
```

is the initial default.

Samples decay naturally.

---

# 81. Managed Stop Policy

Explicit `/stopsound` should be reserved for cases where stopping every matching managed sound is acceptable.

Example:

```text
stop an ambient layer
```

---

# 82. Precise Per-Voice Stop

True per-voice stop isolation may require:

- distinct sound events
- custom resource-pack events
- other future sound-channel strategies

This is not assumed by the initial backend.

---

# 83. Custom Sounds

A resource pack can define custom sound events.

A data pack alone does not create new client-side audio assets.

Therefore custom audio belongs to an optional:

```text
RESOURCE_PACK_EXTENSION
```

---

# 84. Vanilla-Only Default

Initial Digital Playback should support:

```text
VANILLA_SOUNDS_ONLY
```

without requiring a resource pack.

---

# 85. Custom Resource Mode

Future:

```text
CUSTOM_RESOURCE_MODE
```

may allow:

- custom samples
- longer sustained samples
- isolated per-voice events
- custom instruments

This changes the scope of BlockScore significantly and is not required for the core note-block compiler.

---

# 86. Digital Percussion

Percussion can use note-block percussion events with explicit pitch state.

Example:

```text
minecraft:block.note_block.basedrum
```

with the state-derived multiplier.

---

# 87. Percussion Function

The Minecraft Master still stores:

```text
percussion_function
```

such as:

```text
KICK

SNARE

CLOSED_HAT
```

Digital Playback does not infer percussion role from sound-event name alone.

---

# 88. Expanded Percussion

Expanded mode may substitute or layer other vanilla sound events.

Every such choice must be documented as an arrangement decision.

---

# 89. Layering

Digital Playback makes same-tick layering inexpensive.

Example:

```text
Guitar E4
+
Bit E4
```

requires two commands rather than two physical endpoints.

---

# 90. Duplicate Same-Sound Events

Multiple identical `/playsound` commands may be emitted intentionally to represent layered voices.

BlockScore should preserve source voice identity even when the commands are otherwise identical.

---

# 91. Voice Identity

Digital event metadata should retain:

```text
voice_id
```

even if:

```text
sound_event
pitch
position
volume
```

match another event.

This improves loss reporting and debugging.

---

# 92. Priority

Every digital event retains:

```text
P1..P5
```

priority from the Master.

Priority influences:

- diagnostics
- overload handling
- arrangement review

It does not automatically authorize event deletion.

---

# 93. Command Density

Digital Playback can generate large numbers of commands on one tick.

The backend must calculate:

```text
commands_per_tick
```

---

# 94. Maximum Command Density

Report:

```text
max_commands_per_tick
```

plus the corresponding tick/onset.

---

# 95. Command Density Is a Runtime Concern

A musically valid event schedule can still be operationally expensive.

Digital QA therefore distinguishes:

```text
MUSICAL_VALIDITY
```

from:

```text
RUNTIME_LOAD
```

---

# 96. Runtime Benchmarking

Safe command density should be measured in Minecraft rather than assumed.

Status:

```text
TEST_REQUIRED
```

---

# 97. Runtime TPS

BlockScore timing assumes:

```text
20 TPS
```

as the intended simulation rate.

---

# 98. Simulation Time versus Wall Time

If the game is running below 20 TPS:

```text
compiled tick relationships
```

may remain correct while:

```text
real-world playback speed
```

slows down.

BlockScore must distinguish these concepts.

---

# 99. Runtime Metrics

Future game tests should record:

```text
TPS

MSPT

max commands per tick

mean commands per tick

simultaneous sounds

listener count
```

---

# 100. Multiple Listeners

A command targeting:

```text
@a
```

may cause all selected players to receive the sound.

Runtime cost and perception may differ from single-listener testing.

---

# 101. Per-Listener Rendering

For listener-relative spatialization, BlockScore may need to execute events separately for each listener.

This should be treated as a more expensive playback mode.

---

# 102. World Stage Rendering

World-fixed stage events can target multiple listeners with one logical command per sound event.

This is the simpler multiplayer architecture.

---

# 103. Listener Movement

If a listener moves during world-fixed playback, perceived spatial balance changes naturally.

That is intentional for a physical-stage-like mode.

---

# 104. Listener-Centered Movement

Listener-centered playback follows the listener through command execution context.

This behaves less like an in-world orchestra.

---

# 105. Sound Range Calibration

Digital `/playsound` attenuation does not automatically equal physical note-block attenuation.

Therefore BlockScore must not assume:

```text
digital volume 1
=
physical note block loudness/range
```

without testing.

---

# 106. Digital Range Calibration

Add calibration:

```text
CAL-008
Digital versus physical note-block attenuation
```

The test should compare:

- source loudness
- audible radius
- falloff
- instrument behavior
- multiple pitches

---

# 107. Range Profile

Future configuration:

```text
DIGITAL_NATIVE

PHYSICAL_APPROXIMATION

CUSTOM
```

---

# 108. Digital Native

`DIGITAL_NATIVE` uses straightforward command values optimized for digital playback.

---

# 109. Physical Approximation

`PHYSICAL_APPROXIMATION` attempts to make digital note-block playback resemble a physical note-block installation.

This requires CAL-008 data.

---

# 110. Position Precision

Digital sound positions may use coordinates more precisely than block centers.

BlockScore should allow fractional spatial positions in digital build plans.

---

# 111. Spatial Automation

Future expanded mode may move a sound source across time.

Example:

```text
left → center → right
```

This is not required for the core backend.

---

# 112. Pan Is Spatial, Not a Direct Parameter

BlockScore should model left/right balance through source position rather than invent a nonexistent generic pan field for normal `/playsound`.

---

# 113. Distance and Priority

A P5 event should not become inaudible because of casual spatial placement.

Spatial QA must consider priority.

---

# 114. Digital Audibility Warning

Emit:

```text
DIGITAL_AUDIBILITY_WARNING
```

when configured position/range makes an important event unlikely to be heard by the intended listener.

---

# 115. Event Validation

Each note-block-faithful digital event must pass:

```text
SOUND_EVENT_VALID

PITCH_MULTIPLIER_VALID

TARGET_VALID

POSITION_VALID

VOLUME_VALID

MINIMUM_VOLUME_VALID

GAME_TICK_VALID
```

---

# 116. Note-State Validation

For note-block-faithful events:

```text
0 <= note_state <= 24
```

must hold.

---

# 117. Sound Registry Validation

A requested sound event should exist in the target Minecraft profile or be explicitly supplied by an approved resource pack.

---

# 118. No Silent Missing Sounds

If a sound is unavailable:

```text
MISSING_SOUND_EVENT
```

must be reported.

Do not silently drop the attack.

---

# 119. No Silent Pitch Clamping

If an expanded digital event requests an unsupported pitch multiplier:

```text
DIGITAL_PITCH_RANGE_ERROR
```

must be reported.

Do not silently clamp it.

---

# 120. Note-Block Events Avoid Pitch Clamp

Normal note-block states naturally produce:

```text
0.5..2.0
```

so the standard state range fits the intended command pitch window.

---

# 121. Event Schedule

Canonical schedule:

```yaml
127:
  - event: digital-001
  - event: digital-002
  - event: digital-003

128:
  - event: digital-004
```

---

# 122. Function Grouping

A generated datapack may group all events for one game tick into one function.

Conceptually:

```text
tick_000127
tick_000128
tick_000129
```

Exact implementation may choose more compact dispatch structures.

---

# 123. Sparse Tick Optimization

Ticks containing no musical events should not require large empty event functions.

The controller can use:

- conditional dispatch
- section dispatch
- lookup structures
- generated branching

Implementation is future work.

---

# 124. Section Functions

Long songs should be divisible into sections.

Example:

```text
intro

section_a

section_b

climax

outro
```

This improves:

- debugging
- regeneration
- seeking
- maintainability

---

# 125. Section Anchors

Each section retains:

```text
start_game_tick

end_game_tick

start_measure

end_measure
```

---

# 126. Determinism

Given identical:

```text
Minecraft Master

version profile

backend settings

compiler version
```

Digital Playback must generate the same:

```text
event schedule

pitch values

positions

function ordering
```

---

# 127. Numerical Precision

Pitch multipliers should be calculated mathematically.

Generated command text may round to a documented precision.

The canonical internal value should not be based on repeatedly rounded command output.

---

# 128. Pitch Precision Policy

Initial command generation may use:

```text
6 decimal places
```

for note-block multipliers.

Example:

```text
state 10
=
0.890899
```

Internal computation retains higher precision.

---

# 129. Volume Precision

Volume may similarly use a documented command-output precision.

Do not allow formatting changes to alter Master dynamics silently.

---

# 130. Digital Loss Report

Digital Playback must report:

```text
timing quantization

source-duration approximation

dynamic approximation

instrument substitution

sound-event substitution

spatial compromises

stop-policy compromises

runtime warnings
```

---

# 131. Digital Timing Loss

The backend inherits timing error from the 20 TPS compiler.

Metrics include:

```text
max onset error

mean onset error

RMS onset error

IOI distortion

sequence collapses

anchor error
```

---

# 132. Digital Timbre Loss

In Note-Block-Faithful mode:

```text
timbre
```

should match the Minecraft Master instrument event directly.

In Expanded Digital mode, substitutions must be logged.

---

# 133. Digital Sustain Loss

Long source durations that cannot be represented naturally receive explicit sustain-strategy reporting.

Example:

```yaml
voice: horn_1
source_duration: 2.5s
strategy: RETRIGGER
status: APPROXIMATED
```

---

# 134. Digital Advantages

Compared with physical backends, Digital Playback offers:

- no note-block footprint
- no support-block requirements
- no redstone routing
- easier large chords
- easier section seeking
- easier spatialization
- easier revisions
- 20 TPS rather than standard 10 Hz repeater timing
- no physical endpoint retrigger constraint

---

# 135. Digital Limitations

It still has:

- 20 TPS timing quantization
- runtime command cost
- Minecraft sound-engine behavior
- sample-duration limitations
- pitch-speed coupling
- broad `/stopsound` control
- listener-dependent attenuation
- no physical instrument spectacle

---

# 136. Reference Backend Role

Because it avoids physical layout constraints, Digital Playback is useful as a:

```text
REFERENCE BACKEND
```

for evaluating the Minecraft Master.

---

# 137. Reference Comparison

A workflow may compare:

```text
DIGITAL_PLAYBACK
```

against:

```text
COMMAND_RAIL_PHYSICAL
```

to isolate:

```text
physical endpoint / driver effects
```

---

# 138. Digital versus Redstone

Comparing:

```text
DIGITAL_PLAYBACK
```

with:

```text
REDSTONE_PHYSICAL
```

helps isolate effects caused by:

```text
10 Hz redstone timing
```

versus:

```text
20 TPS command timing
```

---

# 139. Mars TEST-001A Digital Mode

Mars should eventually compile to:

```text
DIGITAL_PLAYBACK
```

after the physical tests are established.

Recommended mode:

```text
NOTE_BLOCK_FAITHFUL
```

---

# 140. Mars Timing Mode

Mars Digital should use:

```text
SOURCE_TEMPO
```

with 20 TPS game-tick compilation.

---

# 141. Mars P5 Requirements

Digital output must preserve:

```text
5/4 identity

opening ostinato

meter accents

low pulse

major thematic attacks
```

---

# 142. Mars Digital Questions

TEST-001A should answer:

```text
How much timing loss remains at 20 TPS?

Are any attacks collapsed onto the same game tick?

Does the ostinato retain its feel?

How many commands occur on the densest tick?

How does Digital compare with Command Rail timing?

How does Digital compare with Redstone Physical timing?

Does spatialization improve or obscure the arrangement?
```

---

# 143. Mars Acceptance Criteria

Digital TEST-001A passes only if:

```text
all Master attacks represented

all sound events valid

all pitch multipliers valid

P5 events preserved

timing report complete

no hidden instrument substitution

no hidden dropped events

command-density report complete
```

---

# 144. Tool-Like Stress Test

Digital Playback should eventually serve as an important stress-test backend for rhythmically complex material involving:

```text
odd meter

polymeter

polyrhythm

fast repeated notes

dense percussion

cross-bar riff cycles
```

Its 20 TPS grid still requires honest loss reporting.

---

# 145. Digital Does Not Mean Unlimited Timing

Commands do not make Minecraft an arbitrary-resolution audio workstation.

Normal generated playback remains constrained by the game simulation clock.

BlockScore must not imply otherwise.

---

# 146. Audio Engine Is Not a DAW

Digital Playback should not promise:

- sample-accurate scheduling
- arbitrary note-off control
- unlimited simultaneous sounds
- studio-quality mixing
- perfect sustain

It remains Minecraft playback.

---

# 147. Runtime Calibration

Add:

```text
CAL-009
Digital playback runtime stress test
```

This should test:

```text
dense same-tick commands

long songs

multiple listeners

high polyphony

stable 20 TPS behavior
```

---

# 148. Calibration Status

Before full certification:

```text
CAL-008
attenuation comparison

CAL-009
runtime stress
```

should be completed.

Neither blocks arrangement work.

---

# 149. Debug Mode

Digital Playback should eventually support:

```text
DEBUG_MODE
```

with optional reporting of:

```text
song tick

measure

event count

sound event

voice

pitch

volume

position
```

---

# 150. Tick Display

Development mode may show current:

```text
GAME TICK

MEASURE

SECTION
```

using in-game UI.

This is not part of musical output.

---

# 151. Solo Voice

Digital controller tooling may support:

```text
SOLO
```

by voice or instrument.

Useful for arrangement review.

---

# 152. Mute Voice

Similarly:

```text
MUTE
```

may suppress selected voices during debugging.

This must not mutate the Minecraft Master.

---

# 153. Instrument Sweep

A generated test function may play all required states for one instrument.

This helps compare:

- tuning
- register
- volume
- digital/physical equivalence

---

# 154. Cross-Backend Calibration

A useful test should trigger:

```text
PHYSICAL NOTE BLOCK
```

followed by:

```text
DIGITAL EQUIVALENT
```

for the same:

```text
instrument
note state
```

This supports CAL-008.

---

# 155. Command Preview

Before generating a full datapack, BlockScore should be able to show representative compiled commands.

Example:

```mcfunction
playsound minecraft:block.note_block.guitar block @a ~ ~ ~ 0.8 1.781797 0
```

---

# 156. Generated Package

Future Digital Playback output may contain:

```text
digital-plan.json

event-schedule.json

spatial-map.json

warnings.json

metrics.json

datapack/
```

---

# 157. Optional Resource Package

Expanded custom-audio mode may additionally produce:

```text
resourcepack/
```

This is separate from the core vanilla backend.

---

# 158. Canonical Digital Plan

Conceptually:

```yaml
profile: java-26.2
backend: DIGITAL_PLAYBACK
mode: NOTE_BLOCK_FAITHFUL

controller:
  type: DATAPACK_TICK_CONTROLLER

mixer_source: block

positioning:
  mode: MONO_REFERENCE

events:
  - id: digital-001
    game_tick: 127
    instrument: guitar
    note_state: 22
    sound_event: minecraft:block.note_block.guitar
    pitch_multiplier: 1.781797
    volume: 0.85
```

---

# 159. Planned Implementation Order

Recommended implementation:

```text
1. digital event model

2. instrument-to-sound lookup

3. note-state pitch calculation

4. game-tick event schedule

5. command renderer

6. simple scoreboard/tick controller

7. datapack generation

8. start/stop/pause/reset

9. metrics

10. runtime QA

11. spatial groups

12. stereo/stage modes

13. sustain strategies

14. seeking

15. custom resource extension
```

---

# 160. Initial Test Suite

Create tests for:

```text
state 0 pitch

state 12 pitch

state 24 pitch

same-tick chord

rapid repetition

silent tick gap

odd-meter timing

triplet quantization

multi-voice duplicate pitch

volume mapping

world positioning

listener positioning

loop seam

pause/resume

stop policy
```

---

# 161. Digital QA Checklist

Every compiled package must check:

```text
EVENT_COUNT_VALID

ALL_MASTER_ATTACKS_MAPPED

SOUND_EVENTS_VALID

PITCH_VALUES_VALID

VOLUMES_VALID

POSITIONS_VALID

TARGETS_VALID

GAME_TICKS_VALID

ONSET_GROUPS_PRESERVED

NO_UNDECLARED_DROPS

NO_UNDECLARED_SUBSTITUTIONS

COMMAND_DENSITY_REPORTED

TIMING_METRICS_REPORTED

RUNTIME_DEPENDENCIES_REPORTED
```

---

# 162. Status States

Digital output may progress through:

```text
DESIGNED

COMPILED

OFFLINE_VALIDATED

GAME_TESTED

USER_APPROVED

LOCKED
```

---

# 163. Offline Validation

Offline validation can prove:

- event completeness
- valid pitch calculations
- valid schedule structure
- deterministic command generation

It cannot prove:

- subjective mix quality
- in-game attenuation quality
- runtime performance
- perceived simultaneity

---

# 164. Game Testing

Game testing should confirm:

```text
commands execute

sounds are audible

pitch mapping sounds correct

timing is stable

dense ticks do not cause unacceptable performance

spatial layout behaves as expected
```

---

# 165. No Fake Execution Rule

Do not claim Digital Playback has been heard or validated in Minecraft unless it has actually been run in Minecraft.

Generated commands are not listening tests.

---

# 166. Research Basis

This backend specification is based on current Java Edition command behavior including:

- `/playsound`
- `/stopsound`
- `/execute`
- function execution
- data-pack tick functions
- scoreboard state
- current Java note-block sound events

Version-sensitive command behavior must remain tied to the Java 26.2 profile.

---

# 167. Governing Digital Playback Rule

> Removing the redstone machine does not remove the obligation to preserve the music.

Digital Playback should be the cleanest expression of the Minecraft Master available inside Minecraft's sound engine.

Every attack must be intentional.

Every pitch must be derived correctly.

Every compromise must be reported.

And digital convenience must never become an excuse to hide musical loss.
