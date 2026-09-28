# BlockScore Note Block Science

## Minecraft Java Edition 26.2

This document defines the Minecraft note block mechanics BlockScore may rely on when targeting:

```text
Minecraft Java Edition 26.2
```

It is a versioned technical reference.

Future Minecraft versions must receive their own profile rather than silently changing this document.

Related machine-readable data will eventually live in:

```text
data/java-26.2/
```

---

# 1. Verification Policy

BlockScore distinguishes between several confidence levels.

```text
VERIFIED
```

Confirmed by current Minecraft documentation, current 26.2 API data, or otherwise high-confidence version-specific evidence.

```text
ESTABLISHED
```

Long-standing Java note block behavior with consistent documentation and no known 26.2 change.

```text
PROVISIONAL
```

Strong evidence exists, but BlockScore still wants an explicit 26.2 game calibration before treating the value as immutable.

```text
TEST_REQUIRED
```

Behavior must be verified in Minecraft before a compiler implementation may depend on it.

Never silently promote a provisional assumption to verified behavior.

---

# 2. Java 26.2 Instrument Count

Java 26.2 has twenty material-selected note block instrument sounds relevant to normal musical composition:

```text
harp
bass
basedrum
snare
hat
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

The first sixteen are the established modern Java note block set.

Four copper trumpet variants were added in Java 26.1 and remain present in Java 26.2.

The four trumpet sound events are:

```text
minecraft:block.note_block.trumpet

minecraft:block.note_block.trumpet_exposed

minecraft:block.note_block.trumpet_weathered

minecraft:block.note_block.trumpet_oxidized
```

Minecraft 26.2 API data exposes all four as distinct note block instruments.

---

# 3. Note Block State

A Java note block is represented using block state rather than a block entity.

For BlockScore, the important properties are:

```text
instrument

note

powered
```

## note

Valid values:

```text
0 through 24
```

There are therefore 25 tuning positions.

## powered

Valid values:

```text
false
true
```

This records whether the note block is currently powered.

## instrument

The 26.2 instrument property includes normal instruments, the four copper trumpets, mob-head instruments, and custom-head behavior. Current version-specific data includes the trumpet values in the instrument state.

BlockScore must never infer pitch solely from visible block appearance.

Canonical note state is:

```text
note = integer 0..24
```

---

# 4. Basic Activation

A normal note block can play when:

- attacked by a player
- tuned/used by a player
- activated by redstone

For automated BlockScore machines, redstone activation is the relevant physical mechanism.

A note block responds to the transition into its powered state rather than continuously repeating while power remains present.

Conceptually:

```text
OFF
 ↓ rising edge
ON  → PLAY
```

Remaining powered does not create a stream of repeated notes.

Before another normal trigger, the block must return to an unpowered state.

This is fundamental to both the Redstone Physical and Command Rail backends.

---

# 5. Command Rail Consequence

BlockScore must not assume that this command:

```text
setblock ... note_block[powered=true]
```

is equivalent to a genuine redstone activation.

The Command Rail backend should initially produce an actual power transition around the physical note block.

A conceptual endpoint driver is:

```text
COMMAND
   ↓
create power source
   ↓
NOTE BLOCK receives power transition
   ↓
NOTE BLOCK sounds
   ↓
remove power source
```

A likely implementation is an adjacent temporary redstone block or another deterministic command-controlled power source.

Exact driver behavior remains:

```text
TEST_REQUIRED
```

until verified in Java 26.2.

---

# 6. Required Clearance

For normal musical note block playback, the block above the note block must remain unobstructed.

Conceptually:

```text
AIR

NOTE BLOCK

INSTRUMENT MATERIAL
```

A solid block directly above a normal note block prevents normal musical playback.

This has major implications for generated layouts:

- do not place timing circuitry directly above normal note blocks
- do not place decorative ceilings directly against them
- do not stack instrument banks without vertical clearance
- do not use an upper driver position unless the upper block is specifically part of head-sound behavior

Normal generated endpoints should reserve:

```text
Y + 1 = air
Y     = note block
Y - 1 = instrument material
```


---

# 7. Mob Head Exception

Certain heads placed directly above a note block deliberately replace the normal instrument sound with a mob sound.

Supported vanilla categories include:

```text
zombie
skeleton
wither_skeleton
creeper
piglin
dragon
custom_head
```

A mob head therefore represents an exception to the normal "air above" rule.

Conceptually:

```text
MOB HEAD

NOTE BLOCK

support block
```

The head controls the resulting sound.

Minecraft 1.20 introduced this behavior, including `note_block_sound` support for player heads.

BlockScore classifies head modes as:

```text
FX / SOUND EVENT
```

rather than normal pitched instruments.

---

# 8. Head Pitch Rule

For normal BlockScore purposes, mob-head and custom-head playback should not be treated as a 25-note melodic instrument.

The note state may still exist on the block, but the head sound behavior is not mapped through the normal chromatic instrument range.

Therefore:

```text
HEAD SOUND
pitch_role = FX
tonal_range = none
```

unless a future backend deliberately manipulates the underlying sound through commands.

---

# 9. Pitch States

Normal note block tuning contains 25 chromatic positions.

Each increase is one equal-tempered semitone.

The pitch pattern is:

| State | Pitch class |
|---:|---|
| 0 | F♯ |
| 1 | G |
| 2 | G♯ |
| 3 | A |
| 4 | A♯ |
| 5 | B |
| 6 | C |
| 7 | C♯ |
| 8 | D |
| 9 | D♯ |
| 10 | E |
| 11 | F |
| 12 | F♯ |
| 13 | G |
| 14 | G♯ |
| 15 | A |
| 16 | A♯ |
| 17 | B |
| 18 | C |
| 19 | C♯ |
| 20 | D |
| 21 | D♯ |
| 22 | E |
| 23 | F |
| 24 | F♯ |

State 12 is exactly one octave above state 0.

State 24 is exactly two octaves above state 0.

The 25 values contain both endpoints of the two-octave span.

---

# 10. Pitch Multiplier

For normal note-block sound events, the pitch multiplier corresponding to tuning state `n` is:

```text
pitch_multiplier = 2 ^ ((n - 12) / 12)
```

Therefore:

```text
state 0  = 0.5

state 12 = 1.0

state 24 = 2.0
```

The semitone relationship between states is:

```text
ratio = 2 ^ (1 / 12)
```

This is useful for Digital Playback because a note block state can be recreated using the corresponding sound event and pitch multiplier.

---

# 11. Pitch Multiplier Reference

| State | Pitch class | Multiplier |
|---:|---|---:|
| 0 | F♯ | 0.500000 |
| 1 | G | 0.529732 |
| 2 | G♯ | 0.561231 |
| 3 | A | 0.594604 |
| 4 | A♯ | 0.629961 |
| 5 | B | 0.667420 |
| 6 | C | 0.707107 |
| 7 | C♯ | 0.749154 |
| 8 | D | 0.793701 |
| 9 | D♯ | 0.840896 |
| 10 | E | 0.890899 |
| 11 | F | 0.943874 |
| 12 | F♯ | 1.000000 |
| 13 | G | 1.059463 |
| 14 | G♯ | 1.122462 |
| 15 | A | 1.189207 |
| 16 | A♯ | 1.259921 |
| 17 | B | 1.334840 |
| 18 | C | 1.414214 |
| 19 | C♯ | 1.498307 |
| 20 | D | 1.587401 |
| 21 | D♯ | 1.681793 |
| 22 | E | 1.781797 |
| 23 | F | 1.887749 |
| 24 | F♯ | 2.000000 |

BlockScore should calculate these mathematically rather than storing rounded values as authoritative data.

---

# 12. Register versus Note State

An important BlockScore concept is:

```text
NOTE STATE != ABSOLUTE MUSICAL PITCH
```

The state determines semitone position within the sound sample's two-octave playback span.

The instrument determines the sounding register.

For example:

```text
state 0 + bass
```

does not sound at the same absolute pitch as:

```text
state 0 + bell
```

Even though both note blocks use state 0.

The compiler therefore stores both:

```text
note_state

sounding_pitch
```

---

# 13. Established Instrument Ranges

The established Java instrument ranges used by BlockScore are:

| Instrument | Sounding range |
|---|---|
| Bass | F♯1 – F♯3 |
| Guitar | F♯2 – F♯4 |
| Harp | F♯3 – F♯5 |
| Iron Xylophone | F♯3 – F♯5 |
| Bit | F♯3 – F♯5 |
| Banjo | F♯3 – F♯5 |
| Pling | F♯3 – F♯5 |
| Flute | F♯4 – F♯6 |
| Cow Bell | F♯4 – F♯6 |
| Bell | F♯5 – F♯7 |
| Chime | F♯5 – F♯7 |
| Xylophone | F♯5 – F♯7 |
| Didgeridoo | F♯1 – F♯3 |

These register offsets are long-established note block behavior.

---

# 14. Register Offsets

Relative to the standard F♯3–F♯5 range:

```text
Bass             -24 semitones
Didgeridoo       -24

Guitar           -12

Harp               0
Iron Xylophone     0
Bit                 0
Banjo               0
Pling               0

Flute             +12
Cow Bell          +12

Bell              +24
Chime             +24
Xylophone         +24
```

This representation should eventually be used directly by the range solver.

---

# 15. Canonical Support Blocks

Minecraft often classifies multiple materials into the same note-block instrument group.

BlockScore should not rely on the entire category when generating builds.

Instead, every instrument receives a predictable canonical support block.

Default Java 26.2 build materials:

| BlockScore instrument | Canonical block beneath |
|---|---|
| `harp` | `minecraft:dirt` |
| `bass` | `minecraft:oak_planks` |
| `basedrum` | `minecraft:stone` |
| `snare` | `minecraft:sand` |
| `hat` | `minecraft:glass` |
| `guitar` | `minecraft:white_wool` |
| `flute` | `minecraft:clay` |
| `bell` | `minecraft:gold_block` |
| `chime` | `minecraft:packed_ice` |
| `xylophone` | `minecraft:bone_block` |
| `iron_xylophone` | `minecraft:iron_block` |
| `cow_bell` | `minecraft:soul_sand` |
| `didgeridoo` | `minecraft:pumpkin` |
| `bit` | `minecraft:emerald_block` |
| `banjo` | `minecraft:hay_block` |
| `pling` | `minecraft:glowstone` |
| `trumpet` | `minecraft:copper_block` |
| `trumpet_exposed` | `minecraft:exposed_copper` |
| `trumpet_weathered` | `minecraft:weathered_copper` |
| `trumpet_oxidized` | `minecraft:oxidized_copper` |

The classic mappings are established Java behavior, while current 26.2 APIs specifically identify the four corresponding copper oxidation states for the trumpet family.

---

# 16. Why BlockScore Uses Canonical Blocks

Using a single canonical material per instrument improves:

- reproducibility
- schematic generation
- material counting
- debugging
- visual recognition
- cross-build comparison
- automated QA

A generated bass endpoint should therefore normally use:

```text
oak_planks
```

even though many other wood-class blocks could produce bass.

Users may later request aesthetic substitutions.

---

# 17. Harp Fallback

Harp is the fallback instrument for blocks that do not belong to another note-block material category.

BlockScore should nevertheless use an explicit canonical harp material.

Default:

```text
minecraft:dirt
```

Do not generate harp endpoints by relying on accidental fallback behavior from arbitrary decorative materials.

---

# 18. Percussion Instruments

Three classic instruments are primarily percussion voices:

```text
basedrum

snare

hat
```

They still exist on normal note blocks with note states from:

```text
0..24
```

and the underlying sample can be pitch-shifted.

However, BlockScore does not assign them standard melodic note names by default.

Instead:

```yaml
instrument: basedrum
pitch_mode: percussion_index
state: 8
```

is preferred to pretending the event is an orchestral D or another definite-pitch instrument.

Pitch-changing percussion remains available for:

- drum tuning
- tom approximation
- impact variation
- cymbal-height simulation
- sound-design layers

---

# 19. Percussion State Preservation

MIDI drum importers often throw away note-block percussion tuning information.

BlockScore should not.

The canonical event model preserves:

```text
instrument
note_state
percussion_function
```

separately.

Example:

```yaml
instrument: basedrum
note_state: 4
percussion_function: KICK
```

This allows the arrangement to distinguish several kick or tom colors using the same Minecraft instrument.

---

# 20. Trumpet Family

Java 26.1 added trumpet playback when a note block is placed on copper.

The oxidation state changes the sound.

The four BlockScore IDs are:

```text
trumpet

trumpet_exposed

trumpet_weathered

trumpet_oxidized
```

Corresponding support blocks:

```text
copper_block

exposed_copper

weathered_copper

oxidized_copper
```

This is confirmed by Mojang's 26.1 release material and remains exposed in current 26.2 APIs.

---

# 21. Trumpet Timbre Is Not Cosmetic

Copper oxidation is not merely changing the appearance of one underlying instrument.

Each stage has its own sound event:

```text
block.note_block.trumpet

block.note_block.trumpet_exposed

block.note_block.trumpet_weathered

block.note_block.trumpet_oxidized
```

Therefore BlockScore treats them as four independent instruments.

They may be assigned to separate voices.

Example:

```text
TRUMPET
upper brass

EXPOSED TRUMPET
mid brass

WEATHERED TRUMPET
dark brass

OXIDIZED TRUMPET
low/dark color
```

That role assignment is an arrangement heuristic, not a Minecraft rule.

---

# 22. Trumpet Register Calibration

The trumpet family needs more careful handling than the established instruments.

Current Open Note Block Studio development code maps MIDI instrument octave differences as:

```text
Trumpet            0
Exposed Trumpet    0
Weathered Trumpet +1
Oxidized Trumpet  +2
```

Source location:

```text
OpenNBS/NoteBlockStudio
scripts/midi_instruments/midi_instruments.gml
```

Interpreted as sample/register compensation, this strongly suggests the following BlockScore working model:

```text
trumpet
F♯3 – F♯5

trumpet_exposed
F♯3 – F♯5

trumpet_weathered
F♯2 – F♯4

trumpet_oxidized
F♯1 – F♯3
```

Status:

```text
PROVISIONAL
```

Do not mark these sounding ranges `VERIFIED` until the Java 26.2 trumpet calibration fixture has been run in-game.

The existence of the four instruments and their corresponding copper oxidation blocks is verified; the exact musician-facing octave labels are what remain under calibration.

---

# 23. Trumpet Calibration Fixture

BlockScore should eventually generate a tiny calibration build:

```text
row A:
harp state 0
harp state 12
harp state 24

row B:
trumpet state 0
trumpet state 12
trumpet state 24

row C:
exposed trumpet state 0
12
24

row D:
weathered trumpet state 0
12
24

row E:
oxidized trumpet state 0
12
24
```

Each row should be triggered against known reference notes.

The fixture should verify:

```text
absolute sounding octave

pitch-state progression

instrument identity

tuning accuracy

support-block mapping
```

Once game-tested, the results replace the provisional registry values.

---

# 24. Copper Stability

BlockScore-generated trumpet builds must consider copper oxidation.

An unprotected copper support block changing oxidation stage could potentially change the instrument selected for that endpoint.

Therefore production builds require one of two policies:

```text
COPPER_POLICY = STABLE_VERIFIED_WAXED
```

or:

```text
COPPER_POLICY = CONTROLLED_UNWAXED
```

Before automatically substituting waxed copper in generated endpoints, BlockScore must verify that each waxed full-block equivalent produces the same corresponding trumpet instrument in Java 26.2.

Status:

```text
TEST_REQUIRED
```

Until that fixture exists, machine-readable data should distinguish:

```text
canonical_verified_support

stable_build_support
```

rather than assuming they are identical.

---

# 25. Sound Events

The standard digital sound-event naming pattern is:

```text
minecraft:block.note_block.<instrument>
```

Examples:

```text
minecraft:block.note_block.harp

minecraft:block.note_block.bass

minecraft:block.note_block.guitar

minecraft:block.note_block.bell

minecraft:block.note_block.trumpet_weathered
```

Current Paper 26.2 sound registries expose the normal instrument events and all four trumpet events.

The Digital Playback backend should obtain event names from versioned registry data rather than construct them blindly.

---

# 26. Instrument versus Sound Event

BlockScore must distinguish:

```text
physical instrument
```

from:

```text
sound event
```

Example:

```yaml
instrument:
  id: trumpet_weathered
  support_block: minecraft:weathered_copper

sound:
  event: minecraft:block.note_block.trumpet_weathered
```

Physical playback uses the material/instrument system.

Digital playback uses the sound event.

Both compile from the same Minecraft Master.

---

# 27. Physical and Digital Pitch Equivalence

For a normal instrument event:

```text
physical:
note block state = n
```

should correspond musically to:

```text
digital:
/playsound corresponding_event ... pitch_multiplier(n)
```

provided the same underlying instrument sample is being used.

This gives BlockScore a useful cross-backend comparison mechanism.

Example:

```text
physical:
harp note=12

digital:
block.note_block.harp
pitch=1.0
```

---

# 28. `/playsound` Is Not Identical to a Physical Note Block

Even when pitch is mathematically equivalent, Digital Playback and Physical Playback are not assumed to be behaviorally identical.

Potential differences include:

- source position
- volume
- attenuation behavior
- sound category
- command scheduling
- physical block updates
- particle behavior
- interaction with other game mechanics

Therefore:

```text
MUSICAL_EQUIVALENCE
```

does not imply:

```text
MECHANICAL_EQUIVALENCE
```

---

# 29. Audible Distance

Normal note block sounds are documented as audible out to approximately 48 blocks, with volume decreasing over distance.

BlockScore should therefore treat listener distance as a physical-build constraint.

This matters particularly for Command Rail.

A giant note bank hundreds of blocks away from the intended listener is not a valid physical orchestra merely because commands can activate it.

Possible future strategies include:

```text
central compact bank

multiple distributed banks

listener-positioned digital playback

performance chamber design
```

---

# 30. Spatial Sound Is Part of the Instrument

Physical note blocks emit from their actual world positions.

Therefore endpoint placement affects:

- stereo perception
- relative volume
- arrival perception
- physical immersion

BlockScore should eventually support:

```text
MONO_BANK

STEREO_BANK

ORCHESTRA_STAGE

DISTRIBUTED_SPATIAL
```

Command Rail does not automatically mean all note blocks should be compressed into one tiny cube.

---

# 31. Recommended Command Rail Layout Rule

Until spatial synthesis is implemented, Command Rail should prioritize:

```text
compact but audible
```

The listener/performance position should remain within the effective range of all essential P5 instruments.

Peripheral decorative layers may be positioned farther outward only after listening tests.

---

# 32. Support Block Is Functional

The block below each physical note block is not decoration.

It is part of the instrument definition.

Therefore generated schematics must preserve the pair:

```text
NOTE BLOCK

SUPPORT BLOCK
```

as one logical endpoint.

A support block may not be replaced merely for palette aesthetics unless the replacement is known to belong to the same instrument category.

---

# 33. Endpoint Definition

A BlockScore physical endpoint should eventually contain:

```yaml
endpoint_id:

instrument:

note_state:

sounding_pitch:

support_block:

world_position:

driver_position:

clearance:

polyphony_pool:

verification_status:
```

Example:

```yaml
endpoint_id: guitar_e4_01
instrument: guitar
note_state: 10
sounding_pitch: E4
support_block: minecraft:white_wool
clearance:
  above: air
verification_status: VERIFIED
```

---

# 34. Pitch-to-State Conversion

For an instrument with known lowest sounding pitch:

```text
state =
semitone_distance(
    instrument_low_pitch,
    desired_pitch
)
```

Valid only when:

```text
0 <= state <= 24
```

Example:

Guitar range:

```text
F♯2 – F♯4
```

Desired:

```text
E4
```

Distance from F♯2 to E4:

```text
22 semitones
```

Therefore:

```text
note_state = 22
```

---

# 35. Out-of-Range Rule

If calculated state is:

```text
< 0
```

or:

```text
> 24
```

the requested pitch cannot be played by that physical instrument at that octave.

Never do:

```text
state = clamp(state, 0, 24)
```

That silently changes the music.

Instead invoke the BlockScore range solver.

---

# 36. Range Solver Order

Default resolution order:

```text
1. same instrument, exact pitch

2. timbrally related instrument, exact pitch

3. same instrument, octave displacement

4. split phrase across instruments

5. merge with another voice

6. report unresolved range loss
```

Priority may modify this order.

For P5 bass material, preserving pitch may be more important than preserving exact timbre.

---

# 37. Combined Effective Tonal Range

The established non-trumpet instrument palette spans approximately:

```text
F♯1 through F♯7
```

when different instrument families are combined.

That does not mean one consistent timbre can cover six octaves.

Register expansion always involves instrument changes.

This distinction matters for orchestral reduction.

---

# 38. Timbre Continuity Cost

Every automatic range substitution should calculate a qualitative timbre cost.

Example:

```text
Guitar E4 → Guitar E4
cost = 0

Guitar F5 → Harp F5
cost = moderate

Bass C2 → Didgeridoo C2
cost = moderate

Flute F7 → Bell F7
cost = high
```

The exact scoring model is future work.

For now, changes should be reported rather than hidden.

---

# 39. Tuning Interaction

Using a normal note block advances its note state by one semitone.

After state 24, tuning wraps back to state 0.

Conceptually:

```text
0
1
2
...
23
24
0
```

This makes a human-readable tuning-click count equivalent to note state when starting from a freshly reset/default note block.

Therefore:

```text
note_state = tuning_click_count
```

for normal fresh tuning.

BlockScore can generate tuning instructions such as:

```text
Guitar E4
22 clicks
```

when manual construction is desired.

---

# 40. Schematic Preference

Whenever BlockScore generates a schematic or structure, it should encode the final note state directly.

Manual click counts are primarily for:

- survival builds
- debugging
- hand-built prototypes
- calibration fixtures

They should not be necessary for automated schematic placement.

---

# 41. Normal Physical Instrument Registry

The initial BlockScore registry should contain at least:

```yaml
id:
minecraft_instrument:
sound_event:
canonical_support_block:
pitch_mode:
low_pitch:
high_pitch:
register_offset:
verification:
```

Percussion instruments may omit:

```text
low_pitch
high_pitch
```

and instead use:

```text
pitch_mode: percussion_index
```

---

# 42. Suggested Instrument Roles

These are BlockScore arrangement heuristics, not Minecraft rules.

## Bass

Good for:

- bass guitar
- cello/contrabass reduction
- low synth
- low pedal

## Didgeridoo

Good for:

- low brass
- tuba-like weight
- drone
- aggressive low reinforcement

## Guitar

Good for:

- guitar
- rhythmic ostinato
- middle-low plucked lines

## Harp

Good for:

- piano reduction
- neutral harmony
- generic melodic material

## Pling

Good for:

- bright keyboard
- attack reinforcement
- electric-piano-like material

## Bit

Good for:

- synth
- distorted reinforcement
- cutting melody

## Flute

Good for:

- woodwind
- upper sustained melodic approximation

## Bell / Chime / Xylophone

Good for:

- very high material
- metallic accents
- bright doubling

Use carefully when substituting non-metallic orchestral voices.

## Trumpet Family

Good for:

- brass
- horn reduction
- aggressive melodic statements
- differentiated brass choir layers

Exact register assignment remains partially provisional until calibration.

---

# 43. BlockScore Does Not Use GM Mapping as Truth

General MIDI instruments do not correspond directly to Minecraft instruments.

For example:

```text
MIDI trumpet
```

does not imply:

```text
Minecraft trumpet
```

if another Minecraft instrument better preserves:

- register
- attack
- darkness
- articulation
- musical separation

MIDI mappings are import hints only.

---

# 44. Same Pitch, Different Timbre

A core BlockScore arrangement tool is layering multiple instruments at the same pitch.

Example:

```text
Guitar E4
+
Bit E4
```

can create a more aggressive attack than either instrument alone.

Likewise:

```text
Trumpet
+
Exposed Trumpet
```

can create a composite brass color.

Such layering increases:

```text
polyphony demand
endpoint count
physical volume
```

and therefore must be intentional.

---

# 45. Natural Sound Duration

Note blocks do not behave like MIDI note-on/note-off instruments.

Triggering a note starts its sample.

The source score's note duration is not automatically reproduced by simply keeping redstone power applied.

Therefore:

```text
powered duration
```

is not equivalent to:

```text
musical sustain duration
```

BlockScore handles sustain at the arrangement/backend level.

---

# 46. Physical Sustain Consequence

These source events:

```text
C4 whole note
```

and:

```text
C4 eighth note
```

may initially trigger exactly the same physical note-block attack.

Their difference must be represented through one of:

```text
natural decay

retriggering

tremolo

layering

harmonic reduction

digital assistance
```

depending on context.

---

# 47. Note Block Output Is an Attack Event

For BlockScore's internal architecture, physical note-block playback should be modeled as:

```text
ATTACK EVENT
```

rather than:

```text
NOTE WITH CONTROLLABLE GATE LENGTH
```

This prevents MIDI-style duration assumptions from contaminating the physical compiler.

---

# 48. Command Rail Endpoint Reuse

Because physical playback requires power cycling, an endpoint cannot be assumed to retrigger while remaining continuously powered.

The endpoint allocator must track:

```text
activation tick

reset tick

next legal reuse tick
```

Exact single-game-tick reuse behavior must be confirmed by the Command Rail calibration fixture.

Status:

```text
TEST_REQUIRED
```

Until then, the allocator should favor correctness over maximum endpoint compression.

---

# 49. Command Rail Polyphony

If three simultaneous attacks require:

```text
trumpet E4
```

BlockScore cannot assume one physical note block can represent three independent attacks.

Required pool:

```text
trumpet_e4_01

trumpet_e4_02

trumpet_e4_03
```

The bank compiler calculates maximum concurrent demand.

This is separate from repeated-note reuse.

---

# 50. Physical Chords

A physical chord is simply multiple endpoints activated at the same intended time.

Example:

```text
C4
E4
G4
```

requires three note blocks.

The backend must ensure the power branches arrive simultaneously.

Physical spacing must not alter musical timing.

---

# 51. Redstone Does Not Set Musical Tempo

Minecraft provides timing primitives.

It does not understand:

```text
BPM
quarter note
triplet
5/4
7/8
```

Those concepts belong to BlockScore.

The backend translates musical time into game/redstone time.

Detailed timing mathematics belongs in:

```text
docs/TIMING_MODEL.md
```

---

# 52. Physical Note Block QA

Every generated physical endpoint must pass:

```text
NOTE_STATE_VALID

INSTRUMENT_VALID

SUPPORT_BLOCK_VALID

TOP_CLEARANCE_VALID

DRIVER_CLEARANCE_VALID

POWER_ISOLATION_VALID

POSITION_VALID
```

Trumpet endpoints additionally receive:

```text
COPPER_STAGE_VALID

COPPER_STABILITY_VALID
```

---

# 53. Instrument Verification Matrix

Current BlockScore status:

| Instrument family | 26.2 existence | support mapping | established register |
|---|---|---|---|
| Classic 16 | VERIFIED | VERIFIED/ESTABLISHED | VERIFIED/ESTABLISHED |
| Trumpet | VERIFIED | VERIFIED | PROVISIONAL register calibration |
| Exposed Trumpet | VERIFIED | VERIFIED | PROVISIONAL register calibration |
| Weathered Trumpet | VERIFIED | VERIFIED | PROVISIONAL register calibration |
| Oxidized Trumpet | VERIFIED | VERIFIED | PROVISIONAL register calibration |
| Mob heads | VERIFIED | VERIFIED | FX, no normal tonal range |
| Custom head | VERIFIED | special | FX / custom |

---

# 54. Mars Implications

For TEST-001A, BlockScore may safely rely on:

```text
25-state chromatic tuning

standard established instrument ranges

support-block instrument selection

physical power-trigger behavior

normal top clearance

real physical polyphony

20 material-selected instruments existing in Java 26.2
```

The first Mars pass should preferentially use fully established instruments plus standard/exposed trumpet where appropriate.

Weathered and oxidized trumpet can still be evaluated as arrangement candidates, but any range-dependent use should carry:

```text
TRUMPET_CALIBRATION_PENDING
```

until the fixture is game-tested.

---

# 55. Calibration Tests Still Needed

Before BlockScore v1.0 implementation is considered fully verified, create these in-game fixtures:

```text
CAL-001
Trumpet sounding-register calibration

CAL-002
Waxed copper trumpet equivalence

CAL-003
Command Rail physical driver behavior

CAL-004
Minimum same-endpoint retrigger interval

CAL-005
Multi-endpoint same-tick chord synchronization

CAL-006
Note bank audible-distance practical test

CAL-007
Structure/Litematica preservation of note/instrument states
```

These tests do not block Source Score or Minecraft Master arrangement work.

They constrain backend certification.

---

# 56. Research Basis

This Java 26.2 profile was prepared using:

- Mojang Java 26.1 release and snapshot notes
- current Paper 26.2 instrument and sound registries
- established Java Note Block documentation
- current Minecraft asset sound-event data
- Open Note Block Studio development support for the four Java 26.1 trumpets

The Minecraft 26.1 release explicitly added the copper trumpet instrument and four separate sound events, while Paper's 26.2 API confirms the four instruments remain independently exposed in the target version.

---

# 57. Governing Technical Rule

> Never convert an uncertain Minecraft behavior into a silent compiler assumption.

If the science is verified:

```text
encode it
```

If it is provisional:

```text
label it
```

If it requires testing:

```text
create a fixture
```

That rule is especially important because BlockScore is intended to survive future Minecraft version changes without corrupting existing songs.
