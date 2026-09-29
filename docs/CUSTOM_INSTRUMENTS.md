# BlockScore Custom Instruments

## Purpose

BlockScore custom instruments extend the physical note-block vocabulary without replacing the existing BlockScore timing, arrangement, Command Rail, or backend models.

The first target is guitar articulation.

The immediate benchmark is **natural guitar harmonics**, because a vanilla note-block timbre can preserve pitch and rhythm while still failing the musical identity of a harmonic-heavy guitar passage.

Custom instruments are therefore a **timbre/articulation extension**, not a new playback backend.

---

# 1. Governing Rule

> Keep the proven BlockScore playback architecture. Replace only the physical instrument used by an event when a custom articulation is available.

A custom instrument must remain compatible with the existing Command Rail concept:

```text
SOURCE EVENT
    ↓
Minecraft Master
    ↓
instrument + note_state
    ↓
Command Rail endpoint allocation
    ↓
physical block endpoint
    ↓
redstone rising edge
```

The Command Rail scheduler must not care whether an endpoint is:

```text
minecraft:note_block
```

or:

```text
blockscore:guitar_natural_harmonic_note_block
```

Endpoint identity remains conceptually:

```text
instrument_id + note_state + physical_voice_index
```

---

# 2. Registry Layers

The vanilla Java 26.2 registry remains authoritative for vanilla instruments:

```text
data/java-26.2/instruments.json
```

BlockScore-provided custom instruments live in a separate overlay:

```text
data/java-26.2/custom-instruments.json
```

Source-articulation routing lives in:

```text
data/java-26.2/articulation-map.json
```

The custom overlay must never silently mutate the meaning of a vanilla instrument ID.

---

# 3. Mod Identity

Provider/mod identifier:

```text
blockscore-instruments
```

Minecraft namespace:

```text
blockscore
```

The mod is intentionally small.

Its first responsibility is to add physical note-block-compatible instrument blocks for articulations that vanilla Minecraft cannot represent convincingly.

It is not responsible for song scheduling, source parsing, arrangement, or Command Rail dispatch.

---

# 4. Physical Contract

Every pitched BlockScore custom note block in the first implementation exposes:

```text
note = 0..24
powered = true|false
```

Required behavior:

1. A rising redstone edge plays the block's current `note` state.
2. Remaining powered does not continuously retrigger the sound.
3. A falling edge only resets the powered state.
4. A later rising edge can retrigger the same note.
5. Right-click tuning advances `note` by one semitone and wraps after 24.
6. The block can be placed directly into a Command Rail endpoint bank.
7. No block entity is required for the basic instrument.
8. The block produces a physical in-world sound. Command Rail must not substitute `/playsound` for the physical endpoint.
9. The block remains addressable with ordinary block-state commands and ordinary redstone.

The implementation should remain as close to vanilla note-block interaction behavior as practical.

---

# 5. First Instrument — Guitar Natural Harmonic

Canonical BlockScore instrument ID:

```text
guitar_natural_harmonic
```

Minecraft block:

```text
blockscore:guitar_natural_harmonic_note_block
```

Canonical sound event:

```text
blockscore:block.note_block.guitar_natural_harmonic
```

Initial sounding register:

```text
F#3 .. F#5
```

Initial note-state model:

```text
0 .. 24
```

This register is an implementation starting point, not a claim that all real guitar natural harmonics fit inside a two-octave span.

BlockScore's existing range/loss rules still apply when a source pitch falls outside the physical custom instrument register.

---

# 6. Multisample Strategy

Do not build the instrument from one sample stretched over two octaves.

Version 0.1 uses seven sample roots:

```text
0
4
8
12
16
20
24
```

That keeps the nearest-root pitch shift to at most two semitones.

Asset names:

```text
assets/blockscore/sounds/note_block/guitar_natural_harmonic/n00.ogg
assets/blockscore/sounds/note_block/guitar_natural_harmonic/n04.ogg
assets/blockscore/sounds/note_block/guitar_natural_harmonic/n08.ogg
assets/blockscore/sounds/note_block/guitar_natural_harmonic/n12.ogg
assets/blockscore/sounds/note_block/guitar_natural_harmonic/n16.ogg
assets/blockscore/sounds/note_block/guitar_natural_harmonic/n20.ogg
assets/blockscore/sounds/note_block/guitar_natural_harmonic/n24.ogg
```

The mod chooses the nearest sample root for the requested note state and applies only the remaining small pitch ratio.

---

# 7. Prototype Audio

Batch 02 includes procedurally generated prototype harmonic samples.

They exist only to prove the complete physical path:

```text
custom block → multisample selection → redstone edge → audible sound
```

They contain no third-party sampled audio.

Once the block mechanics are verified, these OGG files can be replaced one-for-one with better recorded guitar harmonic samples without changing the block code or BlockScore registry contract.

---

# 8. Articulation Routing

Example:

```text
source instrument: acoustic guitar
source articulation: natural_harmonic
source sounding pitch: E5
```

With the custom-instrument mod available:

```text
minecraft.instrument = guitar_natural_harmonic
minecraft.origin = PHYSICAL
```

Without the mod, BlockScore may use the declared vanilla fallback and must report the substitution.

Current fallback:

```text
pling
```

This is a perceptual fallback only. It is not articulation-faithful.

---

# 9. Guitar Pro Mapping

Guitar Pro natural harmonics should route to the custom instrument only when the source parser positively identifies the articulation:

```text
Guitar Pro NaturalHarmonic
    ↓
canonical articulation: natural_harmonic
    ↓
guitar_natural_harmonic
```

Do not infer a natural harmonic only because a note is high or bell-like.

---

# 10. Planned Guitar Articulations

After natural harmonics:

```text
guitar_palm_mute
guitar_dead_note
guitar_tapped_harmonic
guitar_artificial_harmonic
guitar_pinch_harmonic
guitar_acoustic_body_hit
guitar_clean
guitar_distorted
```

These are planned identifiers, not implemented instruments.

---

# 11. Command Rail Compatibility

Custom instruments do not change the proven Command Rail scheduler.

For a custom pitched endpoint, the build compiler needs:

```text
instrument_id
minecraft_block
note_state
physical_voice_index
```

Polyphony allocation remains based on simultaneous demand for:

```text
instrument_id + note_state
```

If the same harmonic pitch requires three simultaneous attacks, allocate three physical custom blocks.

---

# 12. Vanilla Compatibility

Recommended compile modes:

```text
VANILLA_ONLY
CUSTOM_IF_AVAILABLE
CUSTOM_REQUIRED
```

- `VANILLA_ONLY` — use declared vanilla fallbacks.
- `CUSTOM_IF_AVAILABLE` — use custom instruments when available; otherwise report and fall back.
- `CUSTOM_REQUIRED` — fail if a required custom articulation is unavailable.

No fallback may occur silently.

---

# 13. NBS Interoperability

A later export layer may generate Note Block Studio custom-instrument definitions from the same registry.

The BlockScore registry remains authoritative.

NBS metadata is an export target, not the source of truth.

---

# 14. Acceptance Test — Crow

The first musical acceptance test is the harmonic-heavy **Crow** arrangement that previously sounded poor with vanilla timbres.

Compare:

```text
A. vanilla articulation fallback
B. guitar_natural_harmonic custom block
```

Pass criteria:

- harmonic attacks remain rhythmically identical
- no attacks are silently removed
- harmonic passages are recognizably distinct from ordinary guitar notes
- repeated harmonics retrigger reliably under Command Rail
- chords allocate enough endpoints
- the custom block does not require `/playsound`
- disabling the mod path still produces an explicit fallback report

---

# 15. Version 0.1 Boundary

Version 0.1 proves only:

```text
source articulation
    ↓
custom instrument selection
    ↓
physical custom block
    ↓
existing Command Rail driver
    ↓
multisampled sound
```

Do not expand the first implementation into a general synthesizer, DAW, or replacement scheduling engine.
