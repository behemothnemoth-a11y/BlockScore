# BlockScore Instrument Registry

## Purpose

This document defines how BlockScore stores and uses versioned Minecraft note-block instrument data.

The canonical Java 26.2 aggregate registry is:

```text
data/java-26.2/instruments.json
```

Related lookup views are:

```text
data/java-26.2/pitch-ranges.json
data/java-26.2/support-blocks.json
data/java-26.2/sound-events.json
```

The aggregate registry is authoritative. The smaller lookup files must remain consistent with it.

---

# 1. Versioned Profiles

Instrument mechanics are version-sensitive.

Every registry belongs to a profile such as:

```text
java-26.2
```

Future versions receive their own profile rather than silently mutating historical song data.

---

# 2. Instrument Identity

Each normal instrument has a stable BlockScore ID.

Java 26.2 normal material-selected IDs are:

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

---

# 3. Registry Entry

A pitched instrument entry contains fields conceptually similar to:

```yaml
id: guitar
index: 5
minecraft_instrument: guitar
sound_event: minecraft:block.note_block.guitar
class: pitched
family: plucked
canonical_support_block: minecraft:white_wool
note_state_min: 0
note_state_max: 24
low_pitch: F#2
high_pitch: F#4
register_offset_semitones: -12
pitch_mode: chromatic
verification:
  existence: VERIFIED
  support_mapping: ESTABLISHED
  register: ESTABLISHED
```

Percussion entries use:

```text
pitch_mode = percussion_index
```

and do not require musician-facing absolute low/high pitches.

---

# 4. Note State

Normal note-block tuning uses:

```text
0..24
```

with one semitone per state.

The common multiplier formula is:

```text
2^((note_state-12)/12)
```

---

# 5. Absolute Pitch

BlockScore stores absolute sounding pitch separately from note state.

The same note state can sound in a different octave for different instrument samples.

Therefore:

```text
note_state != absolute_pitch
```

---

# 6. Pitch Modes

Initial modes:

```text
chromatic
percussion_index
none
custom_sound_event
```

`chromatic` uses musician-facing absolute pitch plus note state.

`percussion_index` preserves sample tuning state while the musical role is described separately.

---

# 7. Canonical Support Block

Every physical normal instrument has one predictable canonical support block.

This improves:

- reproducibility
- schematic generation
- QA
- material counting
- debugging

The canonical block is a build default, not necessarily the only vanilla block capable of selecting that instrument.

---

# 8. Stable Support Block

`stable_support_block` is separate from `canonical_support_block` when long-term build stability requires verification.

The copper trumpet family currently keeps:

```text
stable_support_block = null
```

until `CAL-002` verifies waxed-copper behavior for Java 26.2.

---

# 9. Trumpet Family

Java 26.2 contains four copper trumpet instruments:

```text
trumpet
trumpet_exposed
trumpet_weathered
trumpet_oxidized
```

Their existence and support-block mapping are verified.

Their musician-facing octave labels remain provisional until `CAL-001`.

Current BlockScore working model:

```text
trumpet            F#3-F#5
trumpet_exposed    F#3-F#5
trumpet_weathered  F#2-F#4
trumpet_oxidized   F#2-F#4
```

---

# 10. Verification Levels

The registry uses:

```text
VERIFIED
ESTABLISHED
PROVISIONAL
TEST_REQUIRED
NOT_APPLICABLE
```

Never silently upgrade a provisional value.

---

# 11. Sound Events

Digital Playback uses the `sound_event` field from the versioned registry.

Do not reconstruct names blindly when the registry already contains the authoritative mapping.

---

# 12. Support Mapping

Physical backends use the support mapping from the versioned registry.

Backend code should not maintain a second independent instrument-material table.

---

# 13. Range Lookup

`pitch-ranges.json` is a derived lookup view for range solvers and validation.

Until automatic generation exists, edits to range information must update both:

```text
instruments.json
pitch-ranges.json
```

in the same repository change.

---

# 14. Support Lookup

`support-blocks.json` is a derived lookup view for physical layout and QA.

Until automatic generation exists, support-block edits must remain synchronized with `instruments.json`.

---

# 15. Sound Lookup

`sound-events.json` is a derived lookup view for digital compilation.

It must use the same instrument IDs and sound events as `instruments.json`.

---

# 16. Head Instruments

Mob-head and custom-head sounds are categorized separately from the twenty normal material-selected instruments.

BlockScore treats them as:

```text
FX / SOUND EVENT
```

rather than normal two-octave melodic instruments unless a future explicit extension says otherwise.

---

# 17. General MIDI

General MIDI mappings are import hints only.

They are not registry truth.

A MIDI trumpet does not automatically imply Minecraft `trumpet` if another timbre or register better preserves the arrangement.

---

# 18. Range Validation

For a chromatic instrument, a requested physical pitch is legal only when it maps to:

```text
0 <= note_state <= 24
```

Never clamp an illegal state.

Invoke the range solver instead.

---

# 19. Percussion Validation

Percussion instruments still preserve note state.

Example:

```yaml
instrument: basedrum
note_state: 4
percussion_function: KICK
```

Do not replace note state with a fake absolute orchestral pitch.

---

# 20. Registry Consumers

The registry is consumed by:

```text
Source/Master validation
range solver
arrangement system
Command Rail endpoint compiler
Physical Redstone note-cell compiler
Digital Playback sound lookup
material reports
schematic exporters
QA
```

---

# 21. Schema

Individual normal instrument entries are validated by:

```text
specs/instrument.schema.json
```

The current aggregate `instruments.json` remains a versioned data file containing multiple entries plus profile metadata.

---

# 22. Calibration Dependencies

Current instrument-specific dependencies:

```text
CAL-001  Trumpet sounding-register calibration
CAL-002  Waxed copper trumpet equivalence
```

Backends may add additional mechanical calibration dependencies without changing basic instrument identity.

---

# 23. Migration

When targeting another Minecraft version:

1. create a new profile
2. compare instrument existence
3. compare support mappings
4. compare sound events
5. compare pitch behavior
6. rerun required calibration fixtures
7. migrate song data explicitly

Do not silently reinterpret a locked Java 26.2 song using a later profile.

---

# 24. Governing Registry Rule

> Versioned registry data is the technical source of truth for Minecraft instrument mechanics; arrangement heuristics belong elsewhere.

Keep mechanics, musical decisions, and backend layout logic separate.
