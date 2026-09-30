# Third-Party Audio

## SpeedY — Nylon Guitar Single notes

Source pack:

- Creator: SpeedY
- Pack: `Nylon Guitar Single notes`
- Freesound pack ID: 469
- License: Creative Commons Zero (CC0 1.0)

The source ZIP used for Batch 03 contains the following CC0 recordings used by BlockScore Instruments:

### Harmonic bodies

- `8395__speedy__clean_e_harm.wav` — Freesound 8395
- `8381__speedy__clean_a_harm.wav` — Freesound 8381
- `8387__speedy__clean_d_harm.wav` — Freesound 8387
- `8400__speedy__clean_g_harm.wav` — Freesound 8400
- `8384__speedy__clean_b_harm.wav` — Freesound 8384
- `8392__speedy__clean_e1st_harm.wav` — Freesound 8392

### Picked-string transients

- `8396__speedy__clean_e_str_pick.wav` — Freesound 8396
- `8382__speedy__clean_a_str_pick.wav` — Freesound 8382
- `8388__speedy__clean_d_str_pick.wav` — Freesound 8388
- `8402__speedy__clean_g_str_pick.wav` — Freesound 8402
- `8385__speedy__clean_b_str_pick.wav` — Freesound 8385
- `8393__speedy__clean_e1st_str_pick.wav` — Freesound 8393

## Processing

BlockScore's distributed OGG files are derived works.

Processing includes:

- attack trimming
- mono normalization
- root tuning / small pitch correction
- fade-out and decay shaping
- OGG Vorbis conversion

Tapped harmonics additionally mix a short filtered picked-string transient into the harmonic body.

Dead/muted string samples use short heavily damped picked-string transients.

No commercial or restricted sample-library material is included.


## v0.3 dead/muted-string redesign

Crow acceptance testing showed that the v0.2 dead-note bank was still too tonal.

v0.3 keeps the same CC0 SpeedY source pack but changes the dead-note derivation:

- low register variants: low E and A picked-string recordings
- middle register variants: D and G picked-string recordings
- high register variants: B and high-E picked-string recordings
- only the recorded attack/string-contact region is retained
- stable periodic body is aggressively high-passed/differentiated
- a short shaped broadband component is mixed into the real transient
- no runtime pitch shifting is applied
- two variants per register are exposed through `sounds.json`

The result is intentionally **fret/string percussion**, not a short chromatic guitar note.


## v0.4 clean nylon-guitar bank

The clean nylon-guitar multisample bank uses the same SpeedY / Freesound CC0
`Nylon Guitar Single notes` source pack already documented above.

Roots:
- MIDI 40 E2: clean low-E string pluck
- MIDI 45 A2: clean A string pluck
- MIDI 50 D3: clean D string pluck
- MIDI 55 G3: clean G string pluck
- MIDI 59 B3: clean B string pluck
- MIDI 64 E4: clean high-E string pluck
- MIDI 69 A4: clean high-E 5th-fret note
- MIDI 76 E5: clean high-E 12th-fret note

The source recordings are onset-trimmed, decay-trimmed, peak-normalized and
encoded as mono Ogg Vorbis. Runtime residual pitch shift is at most 3 semitones
over Golden Dragon's E2-G5 range.


## v0.5 static articulation audition banks

The first-pass v0.5 Steel Clean, Distorted Guitar, Palm Mute, Artificial
Harmonic, Pinch Harmonic, and Acoustic Body Hit banks are derived from the
SpeedY CC0 guitar recordings already documented above.

No new restricted/commercial sample library was introduced.

The v0.5 steel/distorted/palm/body timbres are audition prototypes: their
physical block IDs and note/register contracts are intended to stay stable
while their OGG assets may be refined after in-game listening tests.
