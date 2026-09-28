# Mars TEST-001A — Measures 1–8 Transcription Review

## Batch 02 purpose

Batch 02 promotes the opening from a structural sketch to a machine-readable source-score core.

The pitched material needed to begin the Minecraft arrangement is now locked:

- all eight measures of the G ostinato
- sounding registers of the ostinato layers
- the exact first low-theme timing
- the exact first low-theme sounding registers
- the m.8 Theme A restart
- the source forces carrying those layers

## Primary score evidence

The primary authority remains the public-domain 1921 score of *Mars* available through IMSLP.

The first score page contains measures 1–5. The next page is explicitly numbered at measure 6, making the bar mapping unambiguous.

The score confirms:

- `5/4`, Allegro
- Timpani I with wooden sticks
- two harps
- col legno strings
- a quiet tam-tam/gong underlay
- low-theme entry in Bassoons I–II, Contrabassoon, and Horns V–VI
- Bassoon III and Bass Oboe reinforcement on the Db portion
- the next low-theme entry begins at m.8

## CC0 OpenScore cross-check

The OpenScore engraving is CC0 and states that it is intended as a faithful reproduction of the public-domain score.

It makes the first two pages considerably easier to inspect and confirms the same measure layout and source forces.

## Secondary MIDI cross-check

A publicly available orchestral MIDI (`MARS11-1.mid`) was used only as a transcription aid.

It contains a one-measure lead-in before score measure 1. With that offset accounted for:

| Score event | MIDI tick at 120 PPQ | Concert pitch |
|---|---:|---|
| m.3 Theme A entry | 1800 | G2 / G1 |
| m.4 beat 4 | 2760 | D3 / D2 |
| m.5 | 3000 | Db3 / Db2 |
| m.8 Theme A restart | 4800 | G2 / G1 |

The score, not the MIDI, controls enharmonic spelling. MIDI note 49 is stored as **Db3**, not C#3.

The MIDI also confirms the opening ostinato registers used by this fixture:

- Timpani I: G2
- Harps: alternating G1/G2 in opposite phase
- Violins: G3
- Violas: G3
- Cellos: G2
- Contrabasses: G1 sounding

The original score visually confirms both violin sections are active; the secondary MIDI combines/optimizes some orchestral doublings and therefore is not used to decide source-force membership by itself.

## Exact Theme A timing now locked

Theme A begins at absolute QN 10 (m.3):

```text
G  : QN 10 → 18
D  : QN 18 → 20
Db : QN 20 → 28
rest: QN 28 → 30
```

That is exactly four 5/4 measures when the final two-beat rest is included.

The phrase therefore behaves as:

```text
m.3: G for all 5 beats
m.4: G for beats 1–3, D for beats 4–5
m.5: Db for all 5 beats
m.6: Db for beats 1–3, rest for beats 4–5
m.7: primary Theme A tacet
m.8: next G entry begins
```

This resolves the earlier ambiguous OCR in one secondary analysis that appeared to say the process repeated at m.6. The score itself shows the next entry at m.8.

## Remaining review items

Two details remain intentionally below full lock:

1. **Tam-tam/gong roll detail** — the score clearly shows the underlay and 3+2-shaped spans, but Batch 02 marks the exact roll/dynamic treatment `SOURCE_REVIEW_REQUIRED`.
2. **Fine-grained dynamics/hairpins** — the core pitch/rhythm is locked, while event-level dynamic shaping will be transcribed before the final Minecraft Master dynamics pass.

Neither item blocks Minecraft instrument mapping or timing work.

## Status after Batch 02

```text
OSTINATO PITCH/RHYTHM/REGISTER: LOCKED
THEME A PITCH/RHYTHM/REGISTER THROUGH M8: LOCKED
SOURCE FORCE ACTIVITY: LOCKED EXCEPT LISTED REVIEW ITEMS
TAM-TAM DETAIL: PARTIAL LOCK
FINE DYNAMICS: PARTIAL LOCK
MINECRAFT MASTER: READY TO BEGIN
```
