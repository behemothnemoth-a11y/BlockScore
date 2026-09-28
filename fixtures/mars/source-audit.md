# Mars TEST-001A Source Audit

## Rights

The benchmark composition and selected historical score sources are public domain.

The IMSLP listing for the Pay/Smith wind-band condensed score identifies:

- title: *Mars, The Bringer of War*
- arrangement: L. Pay / George Smith
- publication: London, Boosey & Co., 1924
- plate: H.11069
- IMSLP item: `#1038645`
- copyright status: Public Domain

The repository should store BlockScore's transcription/fixture data, not copied page images from modern editions.

## Source Hierarchy

### Primary

1. Public-domain Pay/Smith 1924 condensed wind-band score.
2. Public-domain original orchestral score.

### Structural Cross-Checks

Secondary educational/analytical sources are used only to confirm high-level facts such as:

- the 5/4 opening
- the repeated G ostinato
- 3+2 grouping
- first melodic-fragment interval contour
- approximate structural entry after the opening two bars

Secondary prose never overrides the score.

## Locked Source Facts

### Meter

```yaml
numerator: 5
denominator: 4
grouping: [3, 2]
confidence: HIGH
```

### Opening Ostinato

The IMSLP incipit encodes the opening rhythm as:

```text
triplet eighth + triplet eighth + triplet eighth
quarter
quarter
eighth + eighth
quarter
```

All attacks are on pitch class G in the incipit.

Represented in BlockScore quarter-note units:

```text
0
1/3
2/3
1
2
3
7/2
4
```

Measure length:

```text
5 QN
```

Attacks per full ostinato measure:

```text
8
```

### Opening Texture

The first two bars are treated structurally as the exposed ostinato texture before Theme A enters.

The full source-instrument event list remains pending transcription.

### Theme A Structural Contour

Working structural contour:

```text
G → D → Db
```

Intervals:

```text
P5 up
m2 down
```

The analytical cross-check describes the first fragment as lasting 20 beats / four 5/4 measures.

For Batch 01 this is stored as structural truth only.

Exact note durations, octave/register, ties, and doublings remain pending score transcription.

## Tempo Audit

Primary marking:

```text
Allegro
```

Batch 01 timing-test value:

```text
quarter = 132
```

Status:

```text
BENCHMARK_VALUE_NOT_SOURCE_CLAIM
```

This value exists only so timing test vectors are deterministic.

## Open Source Decisions

1. Complete event-by-event transcription of measures 1–8.
2. Confirm exact source-register placement for Theme A.
3. Confirm all opening octave doublings.
4. Confirm dynamics and crescendos at event level.
5. Decide whether the Pay/Smith arrangement or orchestral score is authoritative when orchestration differs.
6. Extend TEST-001A from structural fixture to complete Source Score fixture.

## Audit Rule

Do not fill an unknown field from memory merely because the passage is familiar.

Unknown source facts remain explicitly unknown until checked against the score.
