# BlockScore

**Chat-native Minecraft note block composition, arrangement, timing, and build compiler.**

BlockScore is a workflow and future toolchain for turning real music into high-quality Minecraft Java note block arrangements without reducing the problem to simple MIDI conversion.

The project treats musical transcription, Minecraft arrangement, timing, physical construction, and export as separate stages.

The chat workflow is currently the authoritative development environment.

---

## Project Status

**Current stage:** Specification + repository-owned compiler/validation foundation
**Minecraft target:** Java Edition 26.2  
**Primary benchmark:** Gustav Holst — *Mars, the Bringer of War*  
**First test:** TEST-001A — opening measures

BlockScore now includes a Python compiler core that consumes the existing Minecraft Master event format and emits validated physical Command Rail datapacks. The repository also executes a growing subset of its YAML contracts in CI instead of treating them as documentation only.

Source import/transcription remains upstream of the compiler. Minecraft installation and in-game testing remain user-side. See `docs/COMPILER_CORE.md` for the compiler boundary and validation commands.

---

# Core Idea

Most note block conversion workflows effectively do this:

```text
MIDI
  ↓
quantize
  ↓
map instruments
  ↓
Minecraft song
```

BlockScore instead separates the problem into several layers:

```text
SOURCE MUSIC
      ↓
SOURCE SCORE
      ↓
MINECRAFT MASTER
      ↓
┌───────────────┬──────────────────┬──────────────────┐
│               │                  │                  │
▼               ▼                  ▼                  ▼
REDSTONE     COMMAND RAIL      DIGITAL PLAYBACK    EXPORT DATA
BUILD        BUILD             / DATAPACK          NBS / MIDI
```

The **Minecraft Master** is the authoritative musical arrangement.

Physical limitations are applied only when compiling that master into a particular playback system.

This prevents redstone constraints from silently damaging the music during transcription.

---

# Design Goals

BlockScore should:

- preserve the musical identity of difficult music
- support odd and changing meters
- support additive meter
- support tuplets and polyrhythms
- support independent rhythmic cycles
- preserve important bass and percussion patterns
- handle dense harmony and simultaneous voices
- understand actual Minecraft note block ranges
- understand instrument support-block requirements
- support the Java 26.2 instrument set
- explicitly handle the four copper trumpet timbres
- distinguish source timing from Minecraft timing
- report every meaningful musical compromise
- generate conventional redstone note block machines
- generate compact command-controlled physical note block banks
- generate command/datapack playback
- eventually generate NBS, MIDI, structures, and Litematica-compatible builds
- remain usable entirely through chat during arrangement and design

---

# Non-Goals

BlockScore is not intended to be:

- a blind MIDI-to-note-block converter
- a system that silently octave-shifts everything into range
- a system that silently deletes difficult voices
- a system that assumes every song is 4/4
- a system that forces every song onto one timing grid
- a substitute for musical arrangement decisions
- dependent on Note Block Studio or another editor to maintain project state

External tools may be useful import/export targets, but they are not the source of truth.

---

# Canonical Score Layers

## 1. Source Score

The Source Score represents what the original music actually does.

It preserves:

- pitch
- rhythm
- meter
- tempo
- voices
- harmony
- percussion
- dynamics
- articulations
- note duration
- structural sections
- tuplets
- phrase boundaries

Minecraft limitations do not apply at this level.

---

## 2. Minecraft Master

The Minecraft Master is the best musical arrangement possible using Minecraft note block language.

It may deliberately:

- re-orchestrate voices
- substitute Minecraft timbres
- redistribute chords
- octave-shift individual material
- simulate sustain
- reinforce attacks
- reduce redundant doublings
- separate otherwise muddy voices

Every meaningful deviation from the Source Score is tracked.

The Minecraft Master is **not** constrained to repeater timing.

---

## 3. Backend Compilation

The Master can then be compiled into different playback systems.

Each backend has different capabilities and different kinds of loss.

BlockScore currently defines three primary backends.

---

# Backend 1 — Physical Redstone

`REDSTONE_PHYSICAL`

A conventional Minecraft note block machine.

Timing is encoded physically using vanilla redstone circuitry.

Typical components include:

- note blocks
- instrument support blocks
- redstone dust
- repeaters
- branching circuits
- synchronization paths
- start/reset controls

This mode is intended for builds where the playback mechanism itself is part of the attraction.

### Strengths

- entirely physical
- understandable in-world
- no command dependency
- classic note block engineering
- useful for survival-compatible designs where resources permit

### Limitations

- coarse timing compared with musical notation
- potentially huge physical footprint
- complex polyphony requires substantial routing
- repeated notes require careful pulse separation
- revisions can require physical redesign

The physical backend must never silently alter the Master simply to make routing easier.

---

# Backend 2 — Command Rail

`COMMAND_RAIL_PHYSICAL`

Command Rail uses **real Minecraft note blocks** as physical instruments while replacing large repeater timing networks with command-controlled sequencing.

This is expected to become one of BlockScore's most important playback modes for complex music.

A Command Rail build contains a reusable physical **instrument bank**.

Example:

```text
BASS
[F#][G][G#][A][A#][B][C]...

GUITAR
[F#][G][G#][A][A#][B][C]...

TRUMPET
[F#][G][G#][A][A#][B][C]...

WEATHERED TRUMPET
[F#][G][G#][A][A#][B][C]...

PERCUSSION
[KICK][SNARE][HAT]...
```

Each note block:

- is physically present
- is tuned correctly
- sits on the correct instrument material
- remains reusable throughout the song

The controller activates endpoints according to the compiled event sequence.

The same physical note therefore does not need to be rebuilt every time that pitch occurs.

---

## Command Rail Voice Allocation

If one pitch must sound more than once simultaneously, BlockScore allocates additional physical endpoints.

Example:

```text
TRUMPET_E4_1
TRUMPET_E4_2
TRUMPET_E4_3
```

This behaves similarly to polyphony allocation in a synthesizer.

The compiler calculates the maximum simultaneous demand for each:

```text
instrument + pitch
```

and provisions only the number of physical voices required.

---

## Command Rail Advantages

Compared with a traditional redstone machine, Command Rail can provide:

- much smaller builds
- easier revision
- reusable note blocks
- straightforward large chords
- cleaner polyphony
- better synchronization
- game-tick sequencing
- compact instrument rooms
- visible physical instrumentation without enormous timing corridors

A Command Rail build is still intended to sound through actual physical note blocks rather than merely placing decorative blocks while `/playsound` does all of the work.

---

# Backend 3 — Digital Playback

`DIGITAL_PLAYBACK`

This backend uses Minecraft commands or datapacks to play sound events directly.

It does not require a physical note block for every musical event.

This mode may support capabilities unavailable to physical note blocks, including:

- more direct volume shaping
- spatial placement
- sound-category routing
- additional sound effects
- enhanced sustain strategies
- command-level sound stopping
- expanded pitch handling where supported

Digital Playback is useful for:

- cinematics
- maps
- extremely complex compositions
- testing
- reference playback
- hybrid installations

---

# Hybrid Playback

BlockScore may also generate:

`COMMAND_RAIL_ENHANCED`

This combines the physical Command Rail note bank with selective digital assistance.

Every event must identify its origin:

```text
PHYSICAL
```

or

```text
DIGITAL_ASSIST
```

BlockScore must never pretend a digitally generated sound originated from a physical note block.

---

# Java 26.2 Instrument Profile

BlockScore currently targets the Java 26.2 note block system.

The registry includes the established note block timbres plus the copper trumpet family introduced in the 26.x generation.

The canonical registry lives at:

```text
data/java-26.2/instruments.json
```

Instrument information includes:

- BlockScore ID
- Minecraft instrument identifier
- sound event
- support block or block family
- pitched/percussive classification
- playable range
- pitch-state mapping
- register behavior
- recommended musical roles
- verification status

Instrument behavior should come from the versioned registry rather than being hard-coded throughout the compiler.

---

# Timing Model

BlockScore never stores difficult rhythms only as rounded milliseconds.

Musical positions should retain exact musical relationships wherever possible.

Example:

```text
measure: 12
beat: 3
subdivision: 2/3
```

instead of immediately converting the event to:

```text
12.363636 seconds
```

Timing is resolved in stages:

```text
SOURCE_TIME
    ↓
MASTER_TIME
    ↓
BACKEND_TIME
```

Each backend performs its own timing compilation.

---

# Absolute-Time Quantization

Timing errors must not accumulate from event to event.

Incorrect:

```text
event 1 rounded
    ↓
event 2 calculated from rounded event 1
    ↓
event 3 calculated from rounded event 2
    ↓
drift
```

Correct:

```text
SOURCE TIMELINE
      │
      ├── event 1 → nearest valid backend time
      ├── event 2 → nearest valid backend time
      ├── event 3 → nearest valid backend time
      └── event N → nearest valid backend time
```

Every event remains anchored to the same absolute musical timeline.

This is especially important for:

- polyrhythms
- Tool-style rhythmic cycles
- tuplets
- odd meter
- repeating ostinati
- very long songs

---

# Independent Rhythmic Structures

BlockScore does not assume that musical structure is identical to bar structure.

It can separately track:

```text
PULSE
BAR
RIFF_CYCLE
PHRASE_CYCLE
POLYRHYTHM_CYCLE
```

For example, a riff can repeat across barlines without being artificially reset at each measure.

This is essential for progressive metal and other rhythmically complex music.

---

# Priority System

Every musical event or voice can receive an importance class.

## P5 — Identity Critical

Examples:

- main riff
- main melody
- signature rhythm
- critical bass movement
- meter-defining pattern

A P5 event may not be removed automatically.

## P4 — Structural

Examples:

- important countermelody
- major harmony
- structural percussion
- important dissonance

## P3 — Harmonic Support

Examples:

- inner chord voices
- meaningful doubling
- secondary harmonic movement

## P2 — Color

Examples:

- orchestration detail
- decorative percussion
- redundant reinforcement

## P1 — Disposable

Material that can be removed with minimal effect on musical identity.

---

# Loss Reporting

BlockScore must never hide compromises.

Example:

```text
RANGE WARNING

Measure: 18
Voice: Horn 3
Source pitch: C#3
Requested Minecraft instrument: Exposed Trumpet

Problem:
Requested pitch is outside the selected physical register.

Candidates:
A. Raise one octave and retain timbre.
B. Retain pitch and change timbre.
C. Merge with LOW_BRASS voice.

Status:
USER_DECISION_REQUIRED
```

Timing example:

```text
TIMING WARNING

Measure: 23
Voice: OSTINATO_A
Priority: P5

Ideal backend time:
117.5 redstone ticks

Candidate physical times:
117
118

Quantization changes a meter-defining pattern.

Status:
RHYTHM_SOLVER_REQUIRED
```

---

# Canonical Event Model

Every note or percussion event will eventually use the BlockScore event schema.

Conceptually:

```yaml
id: event-000124

source:
  measure: 12
  beat: 3
  subdivision: 2/3
  voice: horn_1
  pitch: E4
  duration: 1/8

musical:
  priority: P4
  articulation: marcato
  dynamic: f

minecraft:
  instrument: trumpet_exposed
  pitch: E4
  note_state: 10

backend:
  physical_lane: null
  command_endpoint: null

status: VALID
```

The formal schema will live at:

```text
specs/event.schema.json
```

---

# Arrangement Philosophy

BlockScore optimizes in this order:

1. preserve musical identity
2. preserve rhythm
3. preserve important pitch relationships
4. preserve bass movement
5. preserve major harmonic structure
6. preserve instrumental separation
7. preserve orchestration detail
8. minimize physical complexity

A smaller build is not automatically a better arrangement.

Correctness comes before compression.

---

# Sustain

A note block is fundamentally an attack-based instrument.

BlockScore therefore does not pretend a sustained orchestral note automatically behaves like a sustained Minecraft note.

Possible strategies include:

- natural decay
- controlled retriggering
- tremolo
- layered attacks
- harmonic reduction
- overlapping timbres
- digital assistance

Each sustained passage should have an explicit strategy.

---

# Percussion

Percussion should be mapped by **musical function**, not simply MIDI note number.

Functions include:

```text
KICK
SNARE
CLOSED_HAT
OPEN_HAT
TOM_LOW
TOM_HIGH
CYMBAL
RIDE
METALLIC
WOOD
TIMPANI
IMPACT
OTHER
```

For complex rock and metal arrangements, the default preservation order is:

1. kick pattern
2. snare placement
3. meter-defining cymbal or hat pulse
4. tom fills
5. ghost notes
6. decorative cymbals

---

# Source Ingestion

Preferred source hierarchy:

1. MIDI
2. MusicXML
3. digital notation
4. printed/scanned score
5. stems
6. mixed audio
7. manual transcription

Imported data is never trusted automatically.

Every source must be audited for:

- tempo
- meter
- pickup measures
- track names
- channel assignments
- octave errors
- percussion mapping
- duplicate tracks
- note duration
- tempo changes
- silent lead-in
- transcription mistakes

---

# TEST-001 — Mars

The first BlockScore benchmark is:

**Gustav Holst — Mars, the Bringer of War**

The test is intentionally difficult.

Mars provides:

- 5/4 meter
- repeating ostinati
- strong accent hierarchy
- extreme register separation
- dissonant harmony
- large brass writing
- percussion
- rapidly increasing density
- substantial polyphony

BlockScore should prove itself on difficult material rather than appearing successful only because the first test is easy.

---

## TEST-001A

The first executable section is the opening measures of Mars.

It will be compiled into at least:

```text
MARS_MASTER
MARS_REDSTONE_PHYSICAL
MARS_COMMAND_RAIL_PHYSICAL
```

Later:

```text
MARS_DIGITAL_PLAYBACK
```

### P5 Requirements

The following are considered identity-critical:

- 5/4 pulse
- opening ostinato
- meter-defining accents
- primary bass/pedal movement
- major thematic statements

These may not be silently simplified.

---

# Repository Layout

Planned structure:

```text
BlockScore/
│
├── README.md
├── CHANGELOG.md
├── ROADMAP.md
│
├── docs/
│   ├── WORKFLOW.md
│   ├── NOTE_BLOCK_SCIENCE.md
│   ├── TIMING_MODEL.md
│   ├── INSTRUMENT_REGISTRY.md
│   ├── ARRANGEMENT_RULES.md
│   ├── PHYSICAL_REDSTONE_BACKEND.md
│   ├── COMMAND_RAIL_BACKEND.md
│   ├── DIGITAL_PLAYBACK_BACKEND.md
│   └── QA_AND_LOSS_REPORTING.md
│
├── specs/
│   ├── song-state.schema.json
│   ├── event.schema.json
│   ├── instrument.schema.json
│   ├── voice.schema.json
│   ├── timing.schema.json
│   └── build-plan.schema.json
│
├── data/
│   └── java-26.2/
│       ├── instruments.json
│       ├── pitch-ranges.json
│       ├── support-blocks.json
│       ├── sound-events.json
│       └── timing.json
│
├── fixtures/
│   └── mars/
│       ├── README.md
│       └── test-001a.yaml
│
├── tests/
│   ├── timing/
│   ├── pitch/
│   ├── polyphony/
│   ├── mixed-meter/
│   └── command-rail/
│
├── songs/
│   └── README.md
│
└── src/
    └── README.md
```

---

# Development Strategy

BlockScore is intentionally **spec-first**.

Before large-scale implementation, the repository should define:

- musical event model
- versioned Minecraft mechanics
- instrument registry
- pitch solver
- timing model
- quantization rules
- polyphony model
- backend interfaces
- Command Rail architecture
- loss reporting
- QA requirements
- benchmark fixtures

Once these behaviors are stable, implementation can be delegated in small, explicit tasks.

Example future implementation task:

```text
Implement the absolute timing quantizer described in
docs/TIMING_MODEL.md.

Do not modify the documented behavior.

All tests in tests/timing must pass.
```

This keeps coding effort focused on implementation rather than repeatedly rediscovering project architecture.

---

# Current Workflow

Until the implementation is mature, BlockScore development can be performed entirely in chat.

The chat can:

- research Minecraft mechanics
- transcribe source sections
- build canonical event lists
- make arrangement decisions
- classify voices
- assign Minecraft timbres
- detect range problems
- calculate tuning states
- calculate timing
- compile Command Rail endpoint requirements
- design physical lane layouts
- generate paste-ready repository files
- prepare implementation specifications
- prepare tests
- prepare handoffs for coding tools

No external application is required to continue musical work.

---

# Project Principle

> **Never hide musical loss just because Minecraft made the original difficult.**

Every compromise should be visible.

Every important rhythm should remain intentional.

Every backend should compile from the same musical truth.

And the physical build should serve the music rather than defining it.
