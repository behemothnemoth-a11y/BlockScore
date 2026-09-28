# BlockScore Arrangement Rules

## Shared Musical Rules for All Backends

This document defines how BlockScore transforms a Source Score into a Minecraft Master.

These rules apply before backend compilation.

They govern:

```text
SOURCE SCORE
      ↓
ARRANGEMENT
      ↓
MINECRAFT MASTER
```

The resulting Minecraft Master may then be compiled independently to:

```text
REDSTONE_PHYSICAL

COMMAND_RAIL_PHYSICAL

COMMAND_RAIL_ENHANCED

DIGITAL_PLAYBACK
```

Backend convenience must not determine the arrangement.

---

# 1. Governing Rule

> Preserve musical identity first. Expose every meaningful compromise.

BlockScore is an arranger, not a silent simplifier.

---

# 2. Source Score Is Musical Truth

The Source Score records what the source music actually does.

It may contain:

- pitches
- rhythms
- meter
- tempo
- dynamics
- articulations
- percussion
- voices
- harmony
- note durations
- tuplets
- structural sections
- ornaments
- expression
- phrasing

Minecraft restrictions do not modify the Source Score.

---

# 3. Minecraft Master

The Minecraft Master is the best intended Minecraft arrangement.

It may differ from the Source Score deliberately.

Every meaningful difference must have:

```text
reason

scope

affected events

priority impact

loss classification
```

---

# 4. Backend Neutrality

The Minecraft Master must not be arranged specifically around:

```text
repeater convenience
```

or:

```text
Command Rail endpoint count
```

or:

```text
digital command count
```

unless the user intentionally requests a backend-specific arrangement.

---

# 5. Arrangement before Compilation

Correct order:

```text
SOURCE SCORE

↓ musical decisions

MINECRAFT MASTER

↓ technical decisions

BACKENDS
```

Incorrect:

```text
SOURCE SCORE

↓ redstone limitations

REDSTONE ARRANGEMENT

↓ copied elsewhere

OTHER BACKENDS
```

---

# 6. Arrangement Change

An arrangement change is any deliberate modification to:

```text
pitch

register

instrument

voice assignment

rhythm

duration strategy

dynamic behavior

articulation

doubling

harmony

percussion role
```

---

# 7. Arrangement Change Record

Conceptually:

```yaml
change_id: arrangement-0042

source_event:
  id: horn-00217

change:
  type: TIMBRE_SUBSTITUTION

from:
  voice: horn_2
  pitch: C3

to:
  instrument: didgeridoo
  pitch: C3

reason:
  exact pitch preserved using closest available low timbre

priority:
  P4

status:
  APPROVED
```

---

# 8. Musical Priority

Every important event, voice, pattern, or structural relationship may receive:

```text
P1

P2

P3

P4

P5
```

---

# 9. P5 — Identity Critical

P5 represents material whose loss would materially change recognition or rhythmic identity.

Examples:

- main riff
- principal melody
- meter-defining pulse
- signature accent pattern
- essential bass movement
- defining ostinato
- central thematic attack
- essential rhythmic displacement

P5 material may not be silently deleted.

---

# 10. P4 — Structural

Examples:

- important countermelody
- structural harmony
- major bass reinforcement
- essential percussion
- important dissonance
- large-form transition cue

P4 material requires strong justification for reduction.

---

# 11. P3 — Harmonic Support

Examples:

- inner chord voices
- meaningful doublings
- secondary harmonic motion
- supportive rhythmic material

P3 may be simplified when needed, but changes must remain documented.

---

# 12. P2 — Color

Examples:

- orchestration color
- decorative percussion
- redundant doubling
- secondary texture

P2 is a common reduction candidate.

---

# 13. P1 — Disposable

P1 material may be removed when it contributes little to musical identity.

Deletion still belongs in the loss report.

---

# 14. Priority Is Not Volume

Priority does not mean:

```text
louder
```

A quiet P5 event may be more important than a loud P2 event.

---

# 15. Priority Is Contextual

The same voice may change priority over time.

Example:

```text
Horn 1

measure 4:
P2 doubling

measure 18:
P5 theme
```

Priority belongs to musical function, not instrument name.

---

# 16. Arrangement Order

When resolving a conflict, BlockScore should generally prefer:

```text
1. preserve rhythm

2. preserve identity-critical pitch relationships

3. preserve bass movement

4. preserve principal melody

5. preserve important harmony

6. preserve voice separation

7. preserve timbre

8. preserve decorative detail
```

Specific passages may override this hierarchy.

---

# 17. Rhythm Has Exceptional Weight

For rhythmically defining music, a correct pitch with the wrong rhythm may be less faithful than an approximate timbre with the correct rhythm.

BlockScore should therefore treat rhythmic identity as a first-class arrangement property.

---

# 18. Meter Must Remain Explicit

The Master preserves:

```text
time signature

beat grouping

accent hierarchy
```

separately.

Example:

```text
7/8
```

is incomplete without possible grouping such as:

```text
2 + 2 + 3
```

---

# 19. Additive Meter

Meters such as:

```text
5/8

7/8

9/8

11/8
```

may use additive groupings.

BlockScore must preserve the grouping when it contributes to musical identity.

---

# 20. Five-Four Is Not Automatically Five Equal Beats

A 5/4 measure may function as:

```text
3 + 2

2 + 3

2 + 2 + 1

other accent structure
```

The arrangement must preserve the source grouping rather than merely retaining five quarter-note units.

---

# 21. Riff Cycle Is Separate from Bar

A riff may repeat across barlines.

BlockScore therefore tracks:

```text
BAR

RIFF_CYCLE
```

independently.

---

# 22. Phrase Is Separate from Riff

Likewise:

```text
PHRASE_CYCLE
```

may span several riff cycles or end inside one.

---

# 23. Polyrhythm

Independent rhythmic layers must remain independent in the Master.

Example:

```text
voice A:
3-event cycle

voice B:
4-event cycle
```

BlockScore must not force them into artificial shared bar resets.

---

# 24. Polymeter

If source layers imply different grouping cycles over one absolute timeline, the Master may track those cycles separately.

Backend timing later resolves them to shared absolute time.

---

# 25. Tuplets

Tuplets must remain exact musical relationships in the Master.

Example:

```text
triplet eighth
=
1/3 QN
```

Do not pre-round tuplets to backend ticks during arrangement.

---

# 26. Swing

Swing belongs to the Master or performance-time layer.

It must be represented intentionally.

Example:

```text
swing_ratio:
2:1
```

rather than being approximated accidentally by backend rounding.

---

# 27. Microtiming

Intentional timing feel may use:

```text
micro_offset_ms
```

or equivalent performance metadata.

Examples:

- laid-back snare
- pushed attack
- humanized ensemble timing

Microtiming is distinct from backend quantization error.

---

# 28. No Accidental Groove

Backend timing errors must not be mistaken for expressive groove.

If BlockScore wants a note late:

```text
encode it late in the Master
```

Do not rely on redstone imprecision.

---

# 29. Pitch Preservation

When possible:

```text
source absolute pitch
=
Master absolute pitch
```

---

# 30. Range Conflict

If an intended Minecraft instrument cannot play a source pitch, invoke the range solver.

Never silently clamp the note state.

---

# 31. Range Solver Default Order

Default:

```text
1. same instrument, exact pitch

2. related instrument, exact pitch

3. same instrument, octave displacement

4. split phrase between related instruments

5. merge with another voice

6. deliberate reduction

7. unresolved warning
```

---

# 32. Exact Pitch before Exact Timbre

For many P4/P5 lines, preserving:

```text
actual pitch
```

is normally preferred to preserving:

```text
exact Minecraft timbre choice
```

---

# 33. Timbre before Octave May Sometimes Win

This is not universal.

For material where register is less important but instrument identity is critical, same-timbre octave displacement may be preferable.

The decision must be explicit.

---

# 34. Octave Displacement

Any octave shift must record:

```text
source pitch

Master pitch

direction

octaves shifted

reason
```

---

# 35. Octave Shift Cost

An octave displacement is never treated as zero loss.

Even when pitch class remains correct:

```text
register
```

has changed.

---

# 36. Bass Register Has High Importance

For bass and pedal material, octave displacement can substantially change:

- weight
- harmony
- tension
- voice leading

P5 low material should normally prioritize absolute register.

---

# 37. Melody Register

Principal melody may also require register preservation, especially when octave placement contributes strongly to character.

---

# 38. Inner Harmony Is More Flexible

P2/P3 inner voices are generally more tolerant of:

- octave displacement
- inversion changes
- revoicing

provided harmony and voice-leading remain intelligible.

---

# 39. Instrument Mapping

A source instrument does not map automatically to a same-named Minecraft instrument.

Example:

```text
orchestral trumpet
```

does not automatically require:

```text
Minecraft trumpet
```

---

# 40. Timbre Selection Factors

Choose Minecraft timbre based on:

```text
register

attack

decay

brightness

darkness

percussiveness

musical role

voice separation

available range
```

---

# 41. General MIDI Is a Hint

General MIDI program names may provide useful source metadata.

They are not arrangement authority.

---

# 42. Instrument Roles Are Heuristics

Mappings such as:

```text
didgeridoo → low brass

guitar → rhythmic ostinato

pling → bright keyboard
```

are arrangement heuristics.

They are not Minecraft rules.

---

# 43. Timbre Consistency

BlockScore should avoid unnecessary instrument switching within a phrase.

This property is:

```text
TIMBRE_CONTINUITY
```

---

# 44. Timbre Continuity May Be Broken Deliberately

Reasons include:

- range
- articulation
- register transition
- structural emphasis
- orchestration change
- phrase handoff

---

# 45. Timbre Substitution Cost

Future scoring may estimate:

```text
LOW

MODERATE

HIGH
```

timbre substitution cost.

Initial workflow may use qualitative reporting.

---

# 46. Composite Timbre

Two or more Minecraft instruments may layer at one pitch.

Example:

```text
Guitar E4
+
Bit E4
```

to create a stronger attack.

---

# 47. Layering Is an Arrangement Decision

Layering increases:

```text
event count

physical polyphony

Command Rail endpoint demand

digital command density
```

It should therefore be intentional.

---

# 48. Duplicate Source Doublings

Orchestral scores often contain several instruments doubling the same pitch.

BlockScore does not automatically need one Minecraft attack per original source instrument.

---

# 49. Doubling Merge

If several source voices contribute mostly loudness/color rather than distinct musical information, they may be merged.

Example:

```text
Horn 1 C4
Horn 2 C4
Trumpet C4
```

may become:

```text
Trumpet C4
+
Exposed Trumpet C4
```

or another deliberate composite.

---

# 50. Doubling Merge Must Preserve Function

Do not merge voices that appear identical at one instant but soon diverge in important ways without considering phrase continuity.

---

# 51. Harmonic Reduction

Dense harmony may be reduced when Minecraft clarity or physical practicality requires it.

Default preservation order:

```text
root

bass line

melody note

structural dissonance

third / quality-defining tones

seventh / extension

inner doubling

decorative extensions
```

This is contextual, not absolute.

---

# 52. Root Is Not Always Most Important

Some chords derive identity from:

- pedal tones
- suspensions
- tritones
- altered extensions
- chromatic upper structures

BlockScore must analyze function rather than blindly preserve roots.

---

# 53. Structural Dissonance

Important dissonances should not be "cleaned up" automatically.

If the source intentionally contains:

```text
minor seconds

tritones

clusters

bitonality
```

the Master should preserve them where possible.

---

# 54. Cluster Reduction

If a cluster must be reduced, prioritize:

- outer boundaries
- strongest dissonance
- melodic note
- bass note
- source-defined accents

and report the removed tones.

---

# 55. Voice Leading

When reducing harmony, preserve meaningful movement between successive chords.

A mathematically correct chord with broken voice-leading may sound less faithful.

---

# 56. Voice Identity

The Master retains logical:

```text
voice_id
```

even if several voices use the same Minecraft instrument.

---

# 57. Voice Crossing

Source voice crossing may be preserved.

BlockScore should not automatically reorder voices simply to keep them vertically sorted.

---

# 58. Voice Merge

Two voices may merge only if their musical distinction is not important for the affected passage.

---

# 59. Voice Split

One source voice may be divided between multiple Minecraft instruments.

Typical reason:

```text
range
```

---

# 60. Split Boundary

A split should preferably occur at:

```text
phrase boundary

rest

structural accent

register pivot
```

rather than arbitrarily inside a smooth phrase.

---

# 61. Split Smoothing

If an unavoidable instrument handoff occurs mid-phrase, BlockScore may use:

- overlap
- common-pitch handoff
- layered transition

to reduce abrupt timbre change.

---

# 62. Sustain

Source duration remains part of the Master even though physical note blocks are attack-based.

---

# 63. Sustain Strategy

Each important sustained passage may receive:

```text
NATURAL_DECAY

RETRIGGER

TREMOLO

LAYER

HARMONIC_REDUCTION

DIGITAL_ASSIST
```

---

# 64. Natural Decay

Use when one attack communicates enough of the source event.

Often appropriate for:

- short notes
- accented notes
- naturally decaying material

---

# 65. Retrigger

Repeated attacks may simulate continued energy.

Risk:

```text
unwanted rhythmic pulse
```

---

# 66. Tremolo

If repeated attacks are intended to be heard rhythmically, label:

```text
TREMOLO
```

rather than pretending they are seamless sustain.

---

# 67. Layered Sustain

Different timbres may overlap to imply a broader sustained texture.

This changes orchestration and must be recorded.

---

# 68. Harmonic Sustain Reduction

A long dense chord may be represented by:

```text
attack
+
selected sustained/retriggered tones
```

rather than retriggering every source voice.

---

# 69. Digital Assist

Only:

```text
COMMAND_RAIL_ENHANCED
```

or:

```text
DIGITAL_PLAYBACK
```

may use digital strategies.

`REDSTONE_PHYSICAL` and `COMMAND_RAIL_PHYSICAL` must remain physically honest.

---

# 70. Articulation

Source articulations may include:

```text
staccato

tenuto

accent

marcato

legato
```

Minecraft note blocks cannot reproduce all of these literally.

---

# 71. Articulation Translation

Possible translations:

```text
accent
→ stronger layer / volume / doubled attack

staccato
→ single short-decay attack

tenuto
→ sustain strategy

marcato
→ strong transient + optional layer

legato
→ reduced retrigger emphasis / overlapping strategy
```

---

# 72. Articulation Must Not Invent Rhythm

An articulation strategy may not add clearly audible repeated attacks unless those attacks are musically acceptable.

---

# 73. Dynamics

The Source Score retains dynamics.

The Master may simplify them into meaningful levels.

---

# 74. Dynamic Classes

Initial internal classes may include:

```text
VERY_SOFT

SOFT

MEDIUM_SOFT

MEDIUM

MEDIUM_LOUD

LOUD

VERY_LOUD
```

while retaining original notation.

---

# 75. Physical Dynamics

Physical note blocks do not provide MIDI-style attack velocity.

Physical dynamics may therefore use:

- layering
- orchestration density
- register
- spatial placement
- omission of secondary doublings

---

# 76. Digital Dynamics

Digital Playback may additionally use:

```text
volume
```

but this does not change the Master priority or source dynamic marking.

---

# 77. Accent by Layering

An important accent may temporarily add:

```text
secondary instrument
```

or:

```text
duplicate attack
```

if musically appropriate.

---

# 78. Percussion Function

Percussion is mapped primarily by function.

Canonical roles:

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

---

# 79. Percussion Priority

For rock/metal-style arrangements, default importance often follows:

```text
1. kick rhythm

2. snare placement

3. meter-defining cymbal/hat pulse

4. important tom fills

5. ghost notes

6. decorative cymbals
```

Actual source function may change this order.

---

# 80. Drum Note Numbers Are Not Musical Truth

General MIDI drum note numbers identify source percussion instruments.

They do not dictate Minecraft percussion mapping.

---

# 81. Tuned Percussion State

Minecraft percussion note blocks still support:

```text
note_state 0..24
```

for sample pitch variation.

The Master may use tuned states intentionally.

---

# 82. Timpani

Timpani or pitched drums may require:

- bass
- didgeridoo
- basedrum pitch variation
- layered low instruments

depending on context.

Do not force every timpani line into ordinary kick mapping.

---

# 83. Cymbals

Minecraft's stock note-block palette has limited direct cymbal representation.

Possible approximations may use:

- hat states
- snare states
- metallic instruments
- layered attacks
- expanded digital sounds

Every choice should preserve rhythmic function first.

---

# 84. Drum Fill Simplification

When a fast fill exceeds useful detail, preserve:

```text
entry point

direction

important accents

landing beat
```

before every intermediate ghost note.

---

# 85. Density

Minecraft arrangements can become muddy even when every source note is technically representable.

BlockScore may reduce redundant density deliberately.

---

# 86. Density Reduction Is Not Backend Optimization

Density reduction should occur because of:

```text
musical clarity
```

not simply because a backend has many components.

---

# 87. Masking

Voices that occupy similar:

```text
pitch

timbre

timing
```

may mask each other.

BlockScore may separate them through:

- instrument choice
- register
- selective doubling
- spatial placement

---

# 88. Separation before Deletion

When two important voices collide perceptually, first try:

```text
different timbres
```

before deleting one.

---

# 89. Register Separation

Octave displacement may sometimes be used to separate voices.

Because this changes register, it must be reported.

---

# 90. Accent Separation

Rhythmic distinction may also preserve voice identity even when timbres are similar.

---

# 91. Musical Compression

BlockScore may intentionally represent several source voices using fewer Minecraft voices.

This is:

```text
MUSICAL_COMPRESSION
```

---

# 92. Physical Compression Is Different

Command Rail endpoint reuse is:

```text
PHYSICAL_COMPRESSION
```

not musical compression.

Do not confuse them.

---

# 93. Timing Compression Is Different

If backend quantization collapses two attacks to one tick:

```text
SEQUENCE_COLLAPSE
```

that is timing loss, not arrangement compression.

---

# 94. Loss Categories

Arrangement loss categories include:

```text
PITCH_CHANGE

OCTAVE_SHIFT

TIMBRE_SUBSTITUTION

VOICE_MERGE

VOICE_DROP

HARMONY_REDUCTION

DYNAMIC_REDUCTION

ARTICULATION_APPROXIMATION

SUSTAIN_APPROXIMATION

PERCUSSION_SUBSTITUTION

DENSITY_REDUCTION
```

---

# 95. No Silent Loss

Every nontrivial arrangement loss must be represented in project state.

---

# 96. Automatic Safe Changes

Some transformations may eventually be automatically accepted when confidence is high.

Examples:

```text
exact-pitch instrument substitution with low timbre cost for P1 material

redundant identical P1 doubling merge

format normalization
```

---

# 97. User-Decision Changes

Changes that should normally require review include:

```text
P5 deletion

P5 octave shift

principal melody substitution

major bass-register change

structural rhythm change

important chord-tone deletion

major sustain reinterpretation
```

---

# 98. Unresolved Arrangement

If no acceptable solution exists:

```text
USER_DECISION_REQUIRED
```

is preferable to inventing a hidden compromise.

---

# 99. Candidate Solutions

A conflict report should show alternatives.

Example:

```text
Source:
Horn C3

Candidate A:
Didgeridoo C3
exact pitch
moderate timbre change

Candidate B:
Trumpet C4
same brass family
+1 octave

Candidate C:
merge with low brass
pitch retained elsewhere
voice identity lost
```

---

# 100. Candidate Ranking Data

BlockScore may calculate costs such as:

```text
pitch cost

register cost

timbre cost

rhythm cost

priority impact

density cost
```

These are decision aids.

They must not hide what actually changed.

---

# 101. Deterministic Arrangement

Given identical:

```text
Source Score

arrangement settings

version profile

locked user decisions
```

BlockScore should produce the same Minecraft Master.

---

# 102. Locked Decisions

A user-approved arrangement decision becomes:

```text
LOCKED
```

and automatic passes may not silently reverse it.

---

# 103. Lock Scope

Locks may apply to:

```text
single event

voice

measure range

section

instrument mapping

rhythmic pattern
```

---

# 104. Arrangement Revision

If new evidence makes a locked decision impossible or invalid:

```text
LOCK_CONFLICT
```

must be reported.

Do not silently change the lock.

---

# 105. Section-by-Section Arrangement

Large songs should be arranged in manageable sections.

Each section may move through:

```text
TRANSCRIBED

ANALYZED

ARRANGED

REVIEWED

LOCKED
```

---

# 106. Cross-Section Consistency

Section-by-section work must still maintain:

- instrument identity
- voice identity
- dynamic arc
- recurring riff treatment
- recurring theme treatment

across the song.

---

# 107. Recurring Material

A recurring musical object should receive a stable identifier.

Example:

```text
RIFF_A

OSTINATO_MARS_A

THEME_1
```

---

# 108. Recurring Material Rule

If the same riff returns, BlockScore should normally reuse the same arrangement strategy unless context justifies a change.

---

# 109. Contextual Re-Orchestration

A recurring riff may deliberately change arrangement when source orchestration or dramatic role changes.

Record the variation.

---

# 110. Phrase-Level Analysis

Do not arrange isolated notes without considering their phrase.

Instrument substitution that looks sensible for one pitch may create poor timbre continuity over the whole line.

---

# 111. Pattern-Level Analysis

Repeated rhythmic patterns should be analyzed as patterns rather than independent events.

This is especially important for:

- ostinati
- drum grooves
- arpeggios
- riffs

---

# 112. Harmony-Level Analysis

Chord reductions should be made using harmonic context rather than one simultaneous vertical slice at a time.

---

# 113. Bass-Line Analysis

Bass should be tracked melodically across time, not simply treated as each chord's lowest pitch.

---

# 114. Drum-Groove Analysis

Drums should be treated as recurring groove structures.

Do not make each percussion hit an isolated mapping decision when a pattern-level solution is clearer.

---

# 115. Source Confidence

Transcribed events may carry:

```text
HIGH

MEDIUM

LOW
```

source confidence.

Arrangement should not aggressively optimize uncertain source material without flagging it.

---

# 116. Source Error versus Arrangement Loss

If a source transcription is wrong:

```text
SOURCE_ERROR
```

is not arrangement loss.

Correct the Source Score first.

---

# 117. Import Does Not Equal Truth

MIDI, MusicXML, or other imports are starting data.

They must be audited.

---

# 118. MIDI Velocity

MIDI velocity may suggest:

```text
dynamic

accent

articulation
```

but it is not automatically mapped to Minecraft volume or layering.

---

# 119. MIDI Duration

MIDI note length may represent:

- written duration
- performance articulation
- pedal effects
- transcription quirks

It requires context before sustain strategy is chosen.

---

# 120. Quantization during Import

If imported MIDI is already quantized inaccurately, BlockScore should not blindly preserve those errors as source truth.

---

# 121. Humanized Performance

Small performance deviations may be:

```text
intentional feel
```

or:

```text
incidental performance variation
```

The source-audit stage determines whether they belong in the Master.

---

# 122. Arrangement Presets

Future presets may include:

```text
FAITHFUL

BALANCED

COMPACT

AGGRESSIVE

NOTE_BLOCK_CLASSIC
```

These modify arrangement preferences.

They must not change the underlying Source Score.

---

# 123. Faithful Preset

Prioritizes:

- exact pitch
- complete voices
- source rhythm
- source register
- source dynamics

at the cost of complexity.

---

# 124. Balanced Preset

Allows moderate:

- doubling reduction
- timbre substitution
- density reduction

while protecting P4/P5 identity.

---

# 125. Compact Preset

May reduce P1/P2 material more aggressively.

Still cannot silently change P5 material.

---

# 126. Aggressive Preset

May intentionally layer instruments and emphasize attacks for:

- rock
- metal
- cinematic material

while retaining source structure.

---

# 127. Note-Block-Classic Preset

May prioritize traditional Minecraft note-block aesthetics even when digital backends could do more.

---

# 128. Presets Are Starting Policies

User-approved decisions override presets.

---

# 129. Mars Arrangement Policy

For TEST-001A:

```text
5/4 pulse:
P5

opening ostinato:
P5

meter accents:
P5

primary low pulse:
P5

major thematic statements:
P5
```

---

# 130. Mars Density

The opening should not be made artificially huge simply because Holst's orchestration eventually becomes massive.

Arrange the actual source texture at that moment.

---

# 131. Mars Ostinato

The opening ostinato must preserve:

```text
rhythmic spacing

accent structure

cyclic identity
```

before timbral detail.

---

# 132. Mars Low Material

Low pedal/bass material should prioritize:

```text
absolute pitch

weight

attack placement
```

over exact orchestral instrument names.

---

# 133. Mars Brass

The new trumpet family may be evaluated for brass roles.

Any use dependent on provisional register assumptions retains:

```text
TRUMPET_CALIBRATION_PENDING
```

---

# 134. Mars Percussion

Percussion should preserve:

```text
meter reinforcement

major accents

structural impacts
```

before decorative detail.

---

# 135. Mars Arrangement Passes

Recommended:

```text
PASS 1
rhythm and bass

PASS 2
principal statements

PASS 3
harmony

PASS 4
timbre

PASS 5
percussion detail

PASS 6
density and masking
```

---

# 136. Future Tool-Like Material

For rhythmically complex progressive-metal material, BlockScore should give unusually high weight to:

```text
riff cycle

kick pattern

bass/riff relationship

accent displacement

meter transitions

polyrhythm
```

---

# 137. Guitar Reduction

Dense distorted guitar chords may sound clearer as:

- root/fifth structures
- selected extensions
- layered Guitar + Bit
- register-separated voices

rather than mechanically copying every source guitar track.

---

# 138. Bass and Guitar Unison

When bass and guitar double a riff:

```text
do not automatically merge them
```

The bass register often contributes essential weight.

---

# 139. Drum Complexity

Complex kick patterns are often structurally important in progressive metal and should frequently receive:

```text
P4 or P5
```

rather than being reduced to generic pulse.

---

# 140. Cross-Bar Riffs

A riff that crosses barlines remains a coherent object.

BlockScore must not force its phrase to restart at each bar.

---

# 141. Backend Comparison Must Use Same Master

When comparing:

```text
REDSTONE_PHYSICAL

COMMAND_RAIL_PHYSICAL

DIGITAL_PLAYBACK
```

all should compile from the same locked Minecraft Master.

Otherwise backend comparison is invalid.

---

# 142. Backend-Specific Variant

If a backend genuinely needs a separate arrangement:

```text
BACKEND_VARIANT
```

must be explicit.

Example:

```text
Master:
standard

Redstone variant:
reduced P2 inner harmony
```

---

# 143. Backend Variant Is Not the Master

The canonical Minecraft Master remains preserved.

---

# 144. Arrangement Metrics

A completed section should eventually report:

```text
source event count

Master event count

P5 preserved

P4 preserved

pitch changes

octave shifts

timbre substitutions

voice merges

voice drops

harmony reductions

sustain approximations

percussion substitutions
```

---

# 145. P5 Preservation Metric

Report:

```text
P5 total

P5 unchanged

P5 transformed

P5 unresolved

P5 removed
```

P5 removal should normally be:

```text
0
```

unless explicitly approved.

---

# 146. Master Completeness

Every significant Source event must end as one of:

```text
PRESERVED

TRANSFORMED

MERGED

REMOVED

UNRESOLVED
```

No source material should disappear without classification.

---

# 147. Arrangement QA

Every Master section must check:

```text
SOURCE_EVENTS_ACCOUNTED_FOR

P5_EVENTS_ACCOUNTED_FOR

RHYTHMIC_IDENTITY_PRESERVED

RANGE_VALID

INSTRUMENTS_VALID

VOICE_IDS_VALID

LOSS_RECORDS_COMPLETE

LOCKS_RESPECTED

NO_SILENT_CLAMPING

NO_SILENT_DELETION

NO_BACKEND_CONTAMINATION
```

---

# 148. Backend Contamination

Example failure:

```text
Dropped inner voice because repeater branch was inconvenient
```

This is invalid during Master arrangement.

Correct process:

```text
retain voice in Master

compile redstone

report backend difficulty
```

---

# 149. Arrangement Warning

Use:

```text
ARRANGEMENT_WARNING
```

for compromises that should be reviewed but are not necessarily failures.

---

# 150. Arrangement Failure

Use:

```text
ARRANGEMENT_CONFLICT
```

when no legal Minecraft Master representation has been selected.

---

# 151. Loss Severity

Future loss reporting may use:

```text
INFO

LOW

MODERATE

HIGH

CRITICAL
```

Severity is separate from P1–P5 priority.

---

# 152. Example Loss Record

```yaml
loss_id: loss-0018

category: OCTAVE_SHIFT

source:
  voice: bass_1
  pitch: E1

master:
  instrument: bass
  pitch: E2

priority: P4

severity: HIGH

reason:
  no selected physical timbre supports the original pitch

status:
  USER_REVIEW_REQUIRED
```

---

# 153. Arrangement Notes

Human-readable explanation is encouraged.

The point of loss reporting is not merely machine validation.

It should help the user understand what changed and why.

---

# 154. No Quality Score Yet

BlockScore should not reduce an arrangement to one opaque:

```text
quality = 92%
```

Different kinds of musical loss matter differently.

Expose the components instead.

---

# 155. User Approval

A section becomes user-approved when the user accepts:

```text
Master arrangement

known loss

open calibration dependencies
```

---

# 156. Locking

After approval:

```text
LOCKED
```

means future automated passes preserve the arrangement unless the user reopens it.

---

# 157. Reopening

A locked section may be reopened intentionally.

Revision history should record:

```text
previous version

reason

new decisions
```

---

# 158. Arrangement Version

Each Minecraft Master should eventually include:

```text
arrangement_version
```

for reproducibility.

---

# 159. Versioned Instrument Profile

The Master also records:

```text
minecraft_profile:
java-26.2
```

because legal instrument choices may change between versions.

---

# 160. Profile Migration

Future migration to another Minecraft version must not silently mutate a locked Master.

Run an explicit:

```text
PROFILE_MIGRATION
```

pass.

---

# 161. Calibration Dependencies

A Master may use provisional instrument science.

Such dependencies must be listed.

Example:

```text
CAL-001
Trumpet register
```

---

# 162. Calibration Result Changes Master

If later calibration disproves an assumed legal pitch:

```text
ARRANGEMENT_REVALIDATION_REQUIRED
```

should be triggered.

---

# 163. Master versus Build

The Master describes:

```text
what should be heard
```

The backend describes:

```text
how Minecraft produces it
```

Keep these concepts separate.

---

# 164. Arrangement Output

Future arrangement artifacts may include:

```text
minecraft-master.yaml

voices.yaml

instrument-map.yaml

priority-map.yaml

arrangement-loss.json

locks.json
```

---

# 165. Arrangement Implementation Order

Recommended future implementation:

```text
1. voice model

2. priority model

3. pitch/range solver

4. instrument mapping

5. loss records

6. voice merge/split model

7. harmony reduction support

8. sustain strategy model

9. percussion role mapping

10. lock system

11. deterministic arrangement passes
```

---

# 166. Test Cases

Arrangement tests should include:

```text
out-of-range melody

out-of-range bass

dense chord

important cluster

duplicate doublings

voice split

voice merge

fast drum fill

long sustain

odd meter riff

polyrhythm

cross-bar riff

P5 conflict
```

---

# 167. Arrangement Test Principle

Tests should verify not only that BlockScore produces an answer, but that it:

```text
does not hide what it changed
```

---

# 168. Governing Arrangement Rule

> Minecraft limitations may force compromise, but BlockScore must make the compromise consciously.

Preserve rhythm before convenience.

Preserve identity before completeness for its own sake.

Preserve exact pitch where it matters.

Use timbre intelligently.

Reduce density only for musical reasons.

Never let a backend rewrite the Master in secret.

And never let difficult music become easy by quietly removing what made it difficult.
