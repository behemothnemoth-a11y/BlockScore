# BlockScore Workflow

## Purpose

This document defines the canonical BlockScore workflow for turning source music into Minecraft Java note block arrangements.

BlockScore is designed to work entirely in chat during planning, transcription, arrangement, validation, and test preparation.

The workflow is intentionally split into distinct musical and technical stages so Minecraft limitations do not corrupt the source transcription.

---

# 1. Core Workflow

Every BlockScore project moves through this pipeline:

```text
SOURCE MATERIAL
    ↓
SOURCE AUDIT
    ↓
SOURCE SCORE
    ↓
VOICE ANALYSIS
    ↓
MINECRAFT MASTER
    ↓
BACKEND COMPILATION
    ↓
QA
    ↓
USER REVIEW
    ↓
LOCKED SECTION
```

Backend compilation may produce one or more of:

```text
REDSTONE_PHYSICAL

COMMAND_RAIL_PHYSICAL

COMMAND_RAIL_ENHANCED

DIGITAL_PLAYBACK

NBS_EXPORT

MIDI_EXPORT

STRUCTURE_EXPORT

LITEMATICA_EXPORT
```

The Minecraft Master remains the authoritative arrangement.

---

# 2. Project State

Every active song must maintain a SONG STATE.

Minimum fields:

```yaml
song_id:
title:
composer:
arranger:
source:
source_rights:
minecraft_version:
workflow_version:
target_backends:

source_tempo_map:
source_meter_map:
working_tempo_map:

current_section:
completed_sections:
locked_sections:

voices:
instrument_map:
priority_map:

range_warnings:
timing_warnings:
polyphony_warnings:
build_warnings:

open_decisions:
revision_log:
```

The SONG STATE is persistent project memory.

A section may not be treated as complete merely because a backend file exists.

---

# 3. Status Vocabulary

BlockScore uses explicit status terms.

## DESIGNED

The behavior or arrangement has been planned.

## TRANSCRIBED

Source musical information has been entered.

## ARRANGED

The Minecraft Master has been created.

## COMPILED

A backend representation has been generated from the Master.

## OFFLINE_VALIDATED

The representation has passed BlockScore's non-game checks.

## GAME_TESTED

The result has actually been tested inside Minecraft.

## USER_APPROVED

The user has explicitly approved the result.

## LOCKED

The section should not be changed without deliberate revision.

These statuses are not interchangeable.

Never claim GAME_TESTED unless the build was actually run in Minecraft.

---

# 4. Source Selection

BlockScore can start from:

1. MIDI
2. MusicXML
3. digital score
4. scanned score
5. multitrack stems
6. mixed audio
7. manual transcription
8. an original composition created directly in BlockScore

Preferred source hierarchy is based on how much musical truth can be recovered reliably.

A clean MusicXML or notation source may be preferable to a poorly authored MIDI.

---

# 5. Source Rights

Every project should record source-rights status.

Recommended values:

```text
PUBLIC_DOMAIN

USER_OWNED

USER_PROVIDED_LICENSED_SOURCE

ORIGINAL_COMPOSITION

REFERENCE_ONLY

UNKNOWN
```

The rights field exists so BlockScore knows what source material may be reproduced directly in project fixtures and documentation.

The musical compiler itself does not depend on the rights category.

---

# 6. Source Audit

Before transcription begins, inspect the source for:

- tempo
- tempo changes
- meter
- meter changes
- pickup measures
- repeats
- codas
- fermatas
- tuplets
- swing
- rubato
- instrumentation
- octave-transposing instruments
- percussion notation
- duplicate parts
- divisi
- cue notes
- written versus sounding pitch
- silent lead-in
- editorial markings
- source inconsistencies

The source audit should answer:

```text
What is the actual musical structure?

What timing information is explicit?

What timing information must be inferred?

What instruments are transposing?

What information is unreliable?
```

Do not begin Minecraft adaptation until these questions are sufficiently resolved.

---

# 7. Sectioning

Large songs must be divided into structural sections.

Possible labels:

```text
INTRO
VERSE
PRECHORUS
CHORUS
BRIDGE
BREAKDOWN
SOLO
INTERLUDE
BUILD
CLIMAX
OUTRO
A
B
C
D
TRANSITION
CUSTOM
```

Sections may then be divided into bar groups.

Example:

```text
SECTION_A
bars 1-8

SECTION_B
bars 9-16

SECTION_C
bars 17-24
```

Complex songs should usually be processed in groups of 4-16 bars.

Do not attempt to compile a difficult full song as a single pass.

---

# 8. Pass 1 — Source Truth

The first pass records what the source actually contains.

No Minecraft decisions are allowed during this pass.

Capture:

- notes
- rests
- rhythms
- meter
- tempo
- voices
- note duration
- articulations
- dynamics
- accents
- percussion
- phrase structure
- repeating figures
- pedal tones
- harmonic changes

Example:

```yaml
measure: 12
beat: 3
subdivision: 1/2
voice: horn_1
pitch: E4
duration: 1/8
dynamic: f
articulation: marcato
```

Do not replace E4 with E5 merely because a Minecraft instrument cannot play E4.

That problem belongs to later passes.

---

# 9. Pass 2 — Voice Analysis

Source instrumentation and Minecraft musical voices are not always the same thing.

Identify functional voices such as:

```text
MAIN_MELODY

RIFF_A

RIFF_B

BASS_MAIN

BASS_PEDAL

LOW_BRASS

MID_BRASS

HIGH_BRASS

INNER_HARMONY

COUNTERMELODY

OSTINATO_A

OSTINATO_B

KICK

SNARE

HAT

TOMS

CYMBAL_ACCENT

AMBIENT_LAYER
```

A single source instrument may contain multiple BlockScore voices.

Several source instruments may also collapse into one BlockScore voice if they are redundant doublings.

---

# 10. Pass 3 — Priority Assignment

Assign each voice or event a priority.

## P5 — Identity Critical

Never automatically remove.

Examples:

- signature riff
- primary melody
- defining bass line
- meter-defining ostinato
- crucial rhythmic accents

## P4 — Structural

Examples:

- important countermelody
- structural dissonance
- major percussion accent
- chord tone required for identity

## P3 — Harmonic Support

Examples:

- inner chord tone
- important doubling
- texture-supporting voice

## P2 — Color

Examples:

- orchestration color
- decorative line
- secondary cymbal
- redundant register reinforcement

## P1 — Disposable

Safe reduction candidate if necessary.

Priority assignment must happen before backend constraints begin removing density.

---

# 11. Pass 4 — Minecraft Timbre Mapping

Each voice is mapped to one or more candidate Minecraft timbres.

Do not map instruments solely by literal name.

Consider:

- register
- attack
- brightness
- decay
- harmonic function
- separation from neighboring voices
- texture density

Example:

```text
source: distorted electric guitar

candidate Minecraft mapping:

Guitar
+
Bit reinforcement

or

Guitar
+
Pling attack layer
```

Another example:

```text
source: low orchestral brass

candidate mapping:

Weathered Trumpet

Oxidized Trumpet

Didgeridoo

layered combination
```

The best mapping is whichever preserves the musical role most effectively.

---

# 12. Pass 5 — Range Solving

For every pitched event:

1. check desired instrument at source pitch
2. check octave-equivalent placement
3. check alternate instrument
4. check phrase-level redistribution
5. check voice merging
6. report unresolved loss

Never silently clamp pitches to legal note-block values.

Never silently transpose an entire song because one instrument is out of range.

Prefer local, intentional fixes.

---

# 13. Range Resolution Record

When a pitch cannot be represented directly, create a resolution record.

Example:

```yaml
type: RANGE_WARNING
measure: 18
voice: LOW_BRASS
source_pitch: C#3
requested_instrument: trumpet_exposed

candidates:
  - action: octave_shift
    semitones: 12

  - action: instrument_change
    instrument: didgeridoo

  - action: merge_voice
    target: BASS_MAIN

decision: unresolved
```

The final decision should be stored in the revision history.

---

# 14. Pass 6 — Minecraft Master

The Minecraft Master is the best Minecraft arrangement without backend-specific physical constraints.

It contains:

- Minecraft instruments
- Minecraft-compatible pitch choices
- Minecraft voice structure
- arrangement dynamics
- sustain strategy
- percussion mapping
- final priority
- exact musical timing

The Master may use timing that cannot yet be represented by redstone.

That is intentional.

---

# 15. Sustain Strategy

Each sustained voice should explicitly choose a sustain strategy.

Available values:

```text
ATTACK_ONLY

NATURAL_DECAY

RETRIGGER

TREMOLO

LAYER

HARMONIC_REDUCTION

DIGITAL_ASSIST
```

Example:

```yaml
voice: LOW_STRINGS
strategy: RETRIGGER
interval: 1/2
velocity_curve: decreasing
```

Do not fill long notes with repeated attacks automatically.

Sustain strategy is an arrangement decision.

---

# 16. Dynamics Strategy

Physical note blocks do not reproduce orchestral dynamics directly.

BlockScore may simulate dynamics using:

- fewer or more active voices
- register changes
- octave doubling
- timbre brightness
- percussion reinforcement
- chord width
- rhythmic density
- temporary layer removal
- digital velocity where available

Example:

```text
pp:
single voice

mp:
main voice + light support

f:
main voice + octave reinforcement

ff:
full harmonic stack + percussion reinforcement
```

This should remain musical rather than mechanically proportional.

---

# 17. Percussion Analysis

Percussion should be classified by function.

Canonical functional roles:

```text
KICK

SNARE

CLOSED_HAT

OPEN_HAT

RIDE

CRASH

TOM_LOW

TOM_MID

TOM_HIGH

TIMPANI

METALLIC

WOOD

IMPACT

OTHER
```

For rock and metal, default priority is:

```text
1. kick pattern
2. snare pattern
3. meter-defining cymbal or hat pulse
4. tom fills
5. ghost notes
6. decorative cymbals
```

A complicated kick pattern must not be reduced merely because another melodic voice occurs simultaneously.

---

# 18. Pass 7 — Backend Selection

After the Minecraft Master exists, choose one or more backend targets.

## REDSTONE_PHYSICAL

Traditional physical machine.

## COMMAND_RAIL_PHYSICAL

Reusable physical note-bank with command-controlled triggering.

## COMMAND_RAIL_ENHANCED

Physical note bank plus explicitly labeled digital assistance.

## DIGITAL_PLAYBACK

Command/datapack sound playback.

A song may target multiple backends simultaneously.

---

# 19. Backend Independence

Backends must compile independently.

Incorrect:

```text
MASTER
  ↓
REDSTONE BUILD
  ↓
convert redstone build to Command Rail
```

Correct:

```text
                 ┌→ REDSTONE_PHYSICAL
MASTER ──────────┼→ COMMAND_RAIL_PHYSICAL
                 ├→ COMMAND_RAIL_ENHANCED
                 └→ DIGITAL_PLAYBACK
```

No backend should inherit another backend's compromises unless explicitly requested.

---

# 20. Timing Compilation

Every backend starts from absolute Master timing.

The timing compiler must not calculate event N from the rounded position of event N-1.

For each event:

```text
SOURCE_POSITION
      ↓
MASTER_ABSOLUTE_TIME
      ↓
BACKEND_IDEAL_TIME
      ↓
BACKEND_LEGAL_TIME
      ↓
TIMING_ERROR
```

Store both ideal and compiled timing.

---

# 21. Timing Error

For each backend event, calculate:

```text
signed_error

absolute_error
```

Section-level metrics:

```text
MAX_EVENT_ERROR

MEAN_EVENT_ERROR

RMS_EVENT_ERROR

BARLINE_DRIFT

PHRASE_END_DRIFT

COLLISION_COUNT
```

Barline drift should normally remain zero because the system quantizes against absolute time.

---

# 22. Rhythm Priority

Timing errors must consider musical role.

Two events with the same numeric timing error may have very different musical consequences.

Example:

```text
P1 background doubling:
+50 ms

possibly acceptable
```

versus:

```text
P5 kick accent defining a 7/8 grouping:
+50 ms

possibly unacceptable
```

Timing QA therefore uses:

```text
timing_error
+
priority
+
rhythmic_function
```

not timing error alone.

---

# 23. Mixed Meter

Meter changes are stored explicitly.

Example:

```yaml
meter_map:
  - measure: 1
    meter: 5/4

  - measure: 17
    meter: 3/4

  - measure: 18
    meter: 7/8
    grouping: [2, 2, 3]
```

Do not treat:

```text
7/8 grouped 2+2+3
```

as musically identical to:

```text
7/8 grouped 3+2+2
```

Accent grouping matters.

---

# 24. Polymeter and Riff Cycles

BlockScore separately tracks:

```text
PULSE

BAR

RIFF_CYCLE

PHRASE_CYCLE
```

Example:

```text
meter:
4/4

guitar riff:
cycle length 7 eighth notes

drums:
4/4 backbeat

common reset:
after multiple bars
```

Do not force the riff to restart at barlines.

---

# 25. Tuplets

Tuplets remain exact in Source Score and Minecraft Master.

Example:

```text
triplet subdivision = 1/3 beat
```

Do not initially approximate this as:

```text
0.33 beat
```

Backend compilation decides how accurately the tuplet can be represented.

---

# 26. Chord Compilation

Each simultaneous chord event becomes a logical chord object.

Example:

```yaml
chord_id: chord-021
time: 14.2
notes:
  - C4
  - E4
  - G4
  - B4
```

Backend compilation determines:

- number of physical lanes
- endpoint allocation
- command fan-out
- redstone branch lengths
- simultaneous trigger timing

Physical distance must not introduce unintended chord spread.

---

# 27. Command Rail Compilation

Command Rail compiles the Master into a reusable instrument bank.

Steps:

1. list every required instrument/pitch pair
2. calculate maximum simultaneous demand
3. allocate physical endpoint count
4. assign endpoint IDs
5. construct event-to-endpoint schedule
6. generate trigger timing
7. verify reset time
8. verify same-tick reuse safety
9. generate physical bank layout
10. generate command controller plan

Example endpoint:

```yaml
endpoint_id: guitar_e4_02
instrument: guitar
pitch: E4
note_state: 10
support_block: wool
voice_pool: 2
```

---

# 28. Command Rail Polyphony

For each:

```text
instrument + pitch
```

calculate:

```text
max simultaneous attacks
```

Example:

```text
Exposed Trumpet E4

maximum simultaneous demand:
3
```

Generate:

```text
trumpet_exposed_e4_01

trumpet_exposed_e4_02

trumpet_exposed_e4_03
```

Endpoints may be reused once their trigger/reset requirements permit.

---

# 29. Command Rail Trigger Rule

A Command Rail physical event should trigger the actual note block.

The default architecture must not use `/playsound` while pretending the physical note block produced the sound.

Digital assistance must be explicitly marked:

```text
DIGITAL_ASSIST
```

Physical events must be marked:

```text
PHYSICAL
```

---

# 30. Command Rail Bank Layout

Default logical bank organization:

```text
BANK
├── bass
├── guitar
├── harp
├── flute
├── bells
├── copper_trumpets
├── other_melodic
└── percussion
```

Actual build layout may differ.

Possible physical arrangements:

```text
linear wall

parallel rows

semicircle

orchestra room

stacked racks

compact service corridor
```

Musical correctness takes priority over aesthetics until the functional layout passes QA.

---

# 31. Physical Redstone Compilation

For traditional Redstone Physical:

1. convert Master times to redstone-compatible timing
2. identify simultaneous events
3. create timing trunk
4. create note branches
5. equalize branch delays
6. assign support blocks
7. place note blocks
8. validate clearance
9. verify power isolation
10. add start/reset behavior
11. calculate footprint
12. generate material count

The physical layout compiler should favor deterministic behavior over clever redstone tricks.

---

# 32. Redstone Timing Mode

Traditional Redstone Physical should support at least:

```text
SOURCE_TEMPO

REDSTONE_OPTIMIZED_TEMPO

DUAL
```

## SOURCE_TEMPO

Keep original tempo and accept necessary quantization.

## REDSTONE_OPTIMIZED_TEMPO

Permit small tempo adjustment to improve legal rhythmic spacing.

## DUAL

Maintain both and compare.

Default for difficult benchmark songs:

```text
DUAL
```

---

# 33. Digital Playback Compilation

Digital Playback may use command/datapack sound events.

This backend can preserve:

- greater timing control
- direct sound events
- volume
- panning/spatial position
- additional sound sources
- sound stopping where supported

It should still compile from the same Minecraft Master.

Do not create an unrelated digital arrangement unless explicitly requested.

---

# 34. Arrangement Loss Rules

When density must be reduced:

Reduction order should usually be:

```text
1. redundant P1 doubling

2. decorative P2 material

3. redundant P3 reinforcement

4. alternate timbre

5. octave redistribution

6. harmonic redistribution

7. rhythmic approximation
```

P4 and P5 deletion requires explicit warning.

---

# 35. Collision Resolution

A collision occurs when backend constraints prevent two desired events from being represented independently.

Types include:

```text
TIMING_COLLISION

PITCH_ENDPOINT_COLLISION

REDSTONE_POWER_COLLISION

VOICE_REUSE_COLLISION

COMMAND_LIMIT_COLLISION

PHYSICAL_SPACE_COLLISION
```

Never silently resolve a collision by deleting an event.

Record the collision and selected resolution.

---

# 36. QA Pass

Every completed section must run:

## Musical QA

Check:

- meter
- notes
- bass
- melody
- riff cycle
- harmony
- percussion
- dynamics
- phrase structure
- articulations

## Minecraft QA

Check:

- legal note states
- legal instruments
- valid support blocks
- range compliance
- unobstructed note blocks
- backend compatibility

## Timing QA

Check:

- max error
- mean error
- phrase drift
- meter accents
- tuplets
- collision count

## Backend QA

Check backend-specific rules.

---

# 37. QA Status

Use:

```text
PASS

PASS_WITH_WARNINGS

REVISION_REQUIRED
```

A warning should explain whether it affects:

```text
IDENTITY

RHYTHM

PITCH

HARMONY

TIMBRE

DYNAMICS

BUILD_ONLY
```

---

# 38. User Review

After QA, present the section in a reviewable form.

Possible views:

```text
SHOW SCORE

SHOW EVENTS

SHOW VOICES

SHOW TIMING

SHOW WARNINGS

SHOW RANGE

SHOW COMMAND_RAIL

SHOW REDSTONE

SHOW MATERIALS

SHOW DIFF
```

User feedback may be natural language.

Example:

```text
"The bass doesn't hit hard enough."
```

Convert this into explicit arrangement revisions.

---

# 39. Revision Log

Every meaningful approved change should create an entry.

Example:

```yaml
revision: 14
section: A
change:
  changed LOW_BRASS from exposed trumpet to weathered trumpet
reason:
  user requested darker tone
impact:
  no pitch changes
status:
  approved
```

---

# 40. Section Lock

A section is LOCKED when:

- source truth is accepted
- Minecraft Master is accepted
- required backend has compiled
- QA has passed or warnings are knowingly accepted
- user approves

Locked material should not be changed casually.

Later changes must create a new revision.

---

# 41. Test-Driven Workflow

Before implementation, new compiler behavior should have fixture expectations.

Example:

```text
tests/timing/triplet-redstone.yaml
```

should define:

- source positions
- expected ideal times
- expected legal times
- maximum allowed error
- expected warnings

Implementation should satisfy the fixture rather than redefining the behavior.

---

# 42. Benchmark Philosophy

BlockScore benchmarks should intentionally include difficult music.

Test categories should eventually include:

```text
simple melody

dense chords

fast repeated notes

triplets

5/4

7/8

mixed meter

polyrhythm

long sustained harmony

high polyphony

extreme register

rapid percussion

tempo changes
```

Mars is the first integrated benchmark.

---

# 43. Mars Workflow

For TEST-001A:

```text
STEP 1
source audit

STEP 2
transcribe opening measures

STEP 3
identify ostinato and pedal voices

STEP 4
assign P5 priorities

STEP 5
create Minecraft timbre candidates

STEP 6
solve ranges

STEP 7
create Minecraft Master

STEP 8
compile Command Rail

STEP 9
compile Redstone Physical

STEP 10
compare loss

STEP 11
review

STEP 12
lock or revise
```

---

# 44. Chat Commands

During chat-native development, the following phrases may be used as workflow controls.

## SHOW STATE

Display current SONG STATE.

## SHOW SOURCE

Display source transcription.

## SHOW MASTER

Display Minecraft Master.

## SHOW VOICES

Display voice assignments.

## SHOW WARNINGS

Display unresolved warnings.

## SHOW TIMING

Display timing compilation.

## SHOW RANGE

Display range substitutions.

## SHOW COMMAND RAIL

Display Command Rail endpoint bank and event plan.

## SHOW REDSTONE

Display traditional redstone build plan.

## SHOW MATERIALS

Display block/material requirements.

## SHOW DIFF

Display changes since previous revision.

## LOCK SECTION

Mark current section locked after approval.

## REOPEN SECTION

Allow a locked section to be revised.

---

# 45. No Fake Execution Rule

BlockScore must always distinguish:

```text
planned

calculated

generated

validated

game-tested
```

Do not say:

```text
"the build works"
```

when it has only been designed.

Do not say:

```text
"the timing sounds correct"
```

when it has only passed mathematical analysis.

Do not say:

```text
"the schematic loaded successfully"
```

unless it was actually loaded.

---

# 46. Default Decision Policy

When several valid musical solutions exist:

Do not choose solely based on easiest implementation.

Prefer, in order:

```text
1. musical identity

2. rhythmic identity

3. bass integrity

4. harmonic identity

5. phrase clarity

6. timbral separation

7. physical simplicity
```

If two options remain meaningfully different, preserve both as candidates until reviewed.

---

# 47. Versioned Minecraft Profiles

Minecraft mechanics must remain versioned.

Example:

```text
data/java-26.2/
```

Future versions should use separate profiles:

```text
data/java-26.3/

data/java-27.1/
```

Never overwrite historical behavior merely because Minecraft changes later.

A song should record which profile it targets.

---

# 48. Future Automation

When implementation exists, the full pipeline should eventually support:

```text
import source

analyze source

create event graph

classify voices

assign priorities

solve Minecraft ranges

compile Master

compile backend

run QA

generate report

export
```

Human musical review remains part of the workflow.

BlockScore should automate repetitive translation, not eliminate intentional arrangement decisions.

---

# 49. Governing Rule

The governing BlockScore rule is:

> Preserve the music first, then solve Minecraft.

If a backend cannot reproduce the Master exactly, the backend must report the difference.

The Master should never become less accurate merely to hide backend limitations.
