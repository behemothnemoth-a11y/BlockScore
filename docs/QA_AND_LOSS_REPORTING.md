# BlockScore QA and Loss Reporting

## Purpose

This document defines the shared quality-assurance, warning, loss, and certification rules used across BlockScore.

It applies to:

- Source Score auditing
- Minecraft Master arrangement
- timing compilation
- `REDSTONE_PHYSICAL`
- `COMMAND_RAIL_PHYSICAL`
- `COMMAND_RAIL_ENHANCED`
- `DIGITAL_PLAYBACK`
- future export formats

The governing principle is:

> BlockScore must distinguish musical loss, implementation cost, uncertainty, and failed validation instead of collapsing them into one vague quality score.

---

# 1. Four Different Things

BlockScore reports four categories separately:

1. **Loss** — the music changed.
2. **Warning** — something may be acceptable but deserves review.
3. **Failure** — a required rule or validation check did not pass.
4. **Cost** — the music is preserved, but the build or runtime becomes more expensive.

Examples:

```text
Octave shift                 = LOSS
Provisional trumpet register = WARNING / DEPENDENCY
Disconnected redstone path   = FAILURE
Extra Command Rail endpoint  = COST
```

---

# 2. No Opaque Overall Score

BlockScore must not reduce a result to one number such as:

```text
quality = 92%
```

A build with perfect timing but a missing bass line is not equivalent to a build with slightly imperfect timing and complete musical structure.

Expose the individual metrics.

---

# 3. Priority versus Severity

Musical priority and issue severity are different concepts.

Musical priority:

```text
P1
P2
P3
P4
P5
```

Issue severity:

```text
INFO
LOW
MODERATE
HIGH
CRITICAL
```

Example:

```yaml
priority: P5
severity: HIGH
```

means an important musical event has a serious compromise.

---

# 4. Verification Vocabulary

Minecraft-mechanics confidence uses:

```text
VERIFIED
ESTABLISHED
PROVISIONAL
TEST_REQUIRED
NOT_APPLICABLE
```

These values describe evidence confidence, not musical quality.

---

# 5. Workflow Status Vocabulary

Project and section lifecycle uses:

```text
DESIGNED
TRANSCRIBED
ARRANGED
COMPILED
OFFLINE_VALIDATED
GAME_TESTED
USER_APPROVED
LOCKED
```

A later state must not be claimed merely because an earlier state succeeded.

Examples:

```text
Valid generated commands != GAME_TESTED
Correct redstone math      != GAME_TESTED
GAME_TESTED                != USER_APPROVED
```

---

# 6. Arrangement Loss Categories

Canonical arrangement loss categories:

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

Additional categories may be added by a versioned schema, but existing names should remain stable once used in saved song state.

---

# 7. Timing Warning Classes

Canonical timing classifications:

```text
GRID_EXACT
QUANTIZED_LOW_RISK
GROOVE_CHANGE
SEQUENCE_COLLAPSE
ANCHOR_DISPLACEMENT
IOI_DISTORTION
LOOP_SEAM_WARNING
UNREPRESENTABLE_AT_CURRENT_GRID
```

Timing diagnostics should include signed error, absolute error, and inter-onset effects where relevant.

---

# 8. Physical Redstone Failure Classes

Timing failures:

```text
PHYSICAL_EARLY
PHYSICAL_LATE
BRANCH_DESYNC
TURN_DELAY_MISMATCH
RESTORATION_DELAY_MISMATCH
LOOP_PERIOD_MISMATCH
```

Electrical failures:

```text
NO_POWER_PATH
SIGNAL_DECAY_FAILURE
WRONG_REPEATER_DIRECTION
ACCIDENTAL_REPEATER_LOCK
POWER_LEAK
CROSS_TRIGGER
STUCK_POWER
```

Geometry failures and warnings:

```text
BLOCK_COLLISION
CLEARANCE_COLLISION
SUPPORT_COLLISION
MAINTENANCE_COLLISION
CHUNK_LAYOUT_WARNING
AUDIBILITY_WARNING
```

---

# 9. Command Rail Failure and Warning Classes

Canonical Command Rail diagnostics include:

```text
ENDPOINT_COLLISION
DRIVER_COLLISION
RESET_COLLISION
POOL_OVERFLOW
STALE_DRIVER_STATE
UNDECLARED_DIGITAL_EVENT
AUDIBILITY_WARNING
COMMAND_DENSITY_WARNING
COPPER_STABILITY_PENDING
TRUMPET_CALIBRATION_PENDING
```

Endpoint duplication is normally a **cost**, not a loss.

---

# 10. Digital Playback Failure and Warning Classes

Canonical Digital Playback diagnostics include:

```text
MISSING_SOUND_EVENT
DIGITAL_PITCH_RANGE_ERROR
DIGITAL_AUDIBILITY_WARNING
COMMAND_DENSITY_WARNING
STOP_POLICY_CONFLICT
RUNTIME_STRESS_UNVERIFIED
```

Digital convenience does not excuse silent event drops.

---

# 11. Loss Record

A loss record should contain enough information to understand what changed.

Conceptual form:

```yaml
loss_id: loss-0018
category: OCTAVE_SHIFT
priority: P4
severity: HIGH

source:
  voice_id: bass_1
  pitch: E1

master:
  instrument: bass
  pitch: E2

reason: no selected Minecraft timbre supports the original pitch
status: USER_REVIEW_REQUIRED
```

---

# 12. Warning Record

Conceptual form:

```yaml
warning_id: warning-0042
category: TRUMPET_CALIBRATION_PENDING
severity: MODERATE
scope:
  instrument: trumpet_weathered
message: sounding register is still provisional for Java 26.2
calibration_dependency: CAL-001
```

---

# 13. Failure Record

Conceptual form:

```yaml
failure_id: failure-0007
category: BRANCH_DESYNC
severity: CRITICAL
backend: REDSTONE_PHYSICAL
scope:
  onset_group: onset-0142
expected_tick: 120
observed_ticks: [120, 121]
status: BLOCKS_CERTIFICATION
```

---

# 14. Cost Record

Conceptual form:

```yaml
cost_id: cost-0031
category: ENDPOINT_POOL_GROWTH
backend: COMMAND_RAIL_PHYSICAL
scope:
  endpoint_key: guitar:E4
before: 1
after: 2
reason: rapid retrigger safety
```

A cost record does not imply musical degradation.

---

# 15. Required Accounting Rule

Every significant Source event must ultimately be classified as:

```text
PRESERVED
TRANSFORMED
MERGED
REMOVED
UNRESOLVED
```

No significant event may disappear from the workflow without classification.

---

# 16. P5 Accounting

Every completed section should report:

```text
P5 total
P5 unchanged
P5 transformed
P5 unresolved
P5 removed
```

Default expectation:

```text
P5 removed = 0
```

unless explicitly approved by the user.

---

# 17. Backend Comparison Rule

Backend comparisons are valid only when they compile from the same Minecraft Master or from explicitly named backend variants.

Do not compare two backends while quietly giving one a simpler arrangement.

---

# 18. Shared Timing Metrics

Where applicable, report:

```text
event count
exact event count
quantized event count
sequence collapse count
maximum onset error
mean onset error
RMS onset error
maximum IOI error
mean IOI error
anchor error
loop period error
```

Timing error should be reported in both backend units and milliseconds where useful.

---

# 19. Command Rail Metrics

Report at minimum:

```text
unique instrument-pitch combinations
physical endpoint count
maximum pool size
total musical attacks
total activate actions
total reset actions
maximum simultaneous attacks
maximum commands per tick
rail dimensions
material counts
maximum listener distance
physical event percentage
```

For `COMMAND_RAIL_PHYSICAL`:

```text
physical event percentage = 100%
```

for normal musical events.

---

# 20. Physical Redstone Metrics

Report at minimum:

```text
note block count
redstone dust count
repeater count
repeater settings by delay
maximum branch length
maximum chord fan-out
footprint
chunks touched
maximum listener distance
```

---

# 21. Digital Playback Metrics

Report at minimum:

```text
total digital events
maximum simultaneous sounds
maximum commands per tick
mean commands per active tick
sound-event substitutions
sustain approximations
spatial warnings
runtime-calibration dependencies
```

---

# 22. Musical Loss versus Backend Loss

Arrangement loss occurs while creating the Minecraft Master.

Backend loss occurs while compiling that Master into a technical playback system.

Example:

```text
Horn C3 -> Didgeridoo C3
= ARRANGEMENT LOSS / TIMBRE SUBSTITUTION

Exact Master triplet -> nearest redstone ticks
= BACKEND TIMING LOSS
```

Keep those records separate.

---

# 23. Source Error versus Loss

A transcription correction is not arrangement loss.

Use:

```text
SOURCE_ERROR
```

or an equivalent source-audit record when the input itself was wrong.

Fix the Source Score first.

---

# 24. Uncertainty versus Failure

A provisional assumption is not automatically a failed build.

Example:

```text
TRUMPET_CALIBRATION_PENDING
```

may permit an experimental build when provisional mechanics are allowed.

A build dependent on that assumption cannot be certified beyond the appropriate confidence level until calibration is complete.

---

# 25. Calibration Dependencies

Current planned calibration IDs include:

```text
CAL-001  Trumpet sounding-register calibration
CAL-002  Waxed copper trumpet equivalence
CAL-003  Command Rail physical driver behavior
CAL-004  Minimum same-endpoint retrigger interval
CAL-005  Same-tick multi-endpoint synchronization
CAL-006  Note-bank audible-distance practical test
CAL-007  Structure/Litematica state preservation
CAL-008  Digital versus physical attenuation
CAL-009  Digital runtime stress test
```

A result should list every calibration dependency that affects its certification.

---

# 26. Certification Gate

A backend output may advance to `OFFLINE_VALIDATED` only when all required offline checks pass.

A backend output may advance to `GAME_TESTED` only after it has actually been run in the target Minecraft version.

A backend output may advance to `USER_APPROVED` only after user review.

A section or build becomes `LOCKED` only by an explicit workflow decision.

---

# 27. Blocking versus Non-Blocking Diagnostics

Diagnostics should indicate whether they block certification.

Examples:

```text
INFO                           non-blocking
QUANTIZED_LOW_RISK             non-blocking unless policy says otherwise
TRUMPET_CALIBRATION_PENDING    blocks full verification, may allow experimental output
NO_POWER_PATH                  blocking
MISSING_SOUND_EVENT            blocking
P5 REMOVED without approval    blocking
```

---

# 28. User Review Required

Use:

```text
USER_REVIEW_REQUIRED
```

when there are multiple musically defensible solutions and BlockScore should not choose silently.

Typical cases:

- P5 octave shift
- principal melody timbre change
- major bass-register change
- important chord-tone deletion
- major sustain reinterpretation

---

# 29. Locked Decision Conflict

If a later compiler or calibration result contradicts a locked decision, emit:

```text
LOCK_CONFLICT
```

Do not silently override the lock.

---

# 30. Machine-Readable QA Summary

Future compiled artifacts should expose a structure conceptually similar to:

```yaml
status: OFFLINE_VALIDATED

counts:
  losses: 3
  warnings: 7
  failures: 0
  costs: 14

p5:
  total: 82
  unchanged: 78
  transformed: 4
  unresolved: 0
  removed: 0

calibration_dependencies:
  - CAL-001
  - CAL-004
```

---

# 31. Human-Readable Summary

The same result should also explain important changes in plain language.

A good report answers:

- What changed?
- Why did it change?
- How important was it?
- Was there another option?
- Is this verified or provisional?
- Does it block testing or certification?

---

# 32. Deterministic Reporting

Given the same Source Score, Minecraft Master, backend settings, and compiler version, QA record IDs and ordering should be deterministic where practical.

This makes diffs meaningful.

---

# 33. No Fake Execution Rule

BlockScore must never report in-game success based solely on generated files, mathematical simulation, or static validation.

Use the strongest status actually earned.

---

# 34. Governing QA Rule

> If something changed, say what changed. If something is uncertain, say what is uncertain. If something failed, do not disguise it as a compromise.

BlockScore should make difficult music auditable rather than merely plausible.
