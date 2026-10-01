# AURORA Bounded Reservoir-Domain Expert Review Packet

## Purpose

This packet requests targeted review of domain-sensitive assumptions that can
materially change AURORA's software architecture, validation logic, or claim
boundaries.

It is **not** a request for an expert to validate every simulator run, design
the project, or certify AURORA as safe for field operation.

The desired output is a small set of traceable corrections, confirmations,
sources, and unresolved questions that the team can encode into reusable
documentation and validation rules.

## Context supplied to reviewer

AURORA studies autonomous closed-loop control in a synthetic waterflood
experiment.

Current intended reasoning chain:

    Egg reservoir benchmark
        -> OPM Flow higher-fidelity numerical reference
        -> controller observation
        -> learned controller proposed action
        -> reduced-order / CRM-style safety model
        -> QP-style safety filter
        -> applied simulator action
        -> OPM response
        -> telemetry / validation
        -> comparative experiment

Important claim boundary:

OPM + Egg is a numerical reference experiment, not physical ground truth or
validation of an operating reservoir.

## Reviewer instructions

For each question, please provide where possible:

- **Assessment:** correct / partly correct / incorrect / depends / unknown
- **Reason:** short explanation
- **Evidence:** source, equation, simulator documentation, or domain principle
- **Conditions:** assumptions under which the answer holds
- **Correction:** exact wording or interpretation you recommend
- **Decision impact:** whether AURORA should change a variable, rule, model,
  experiment, constraint, or claim

Please explicitly say when the available information is insufficient.

---

## Q1 — Pressure semantics

### Question

Which pressure quantities are most important for AURORA to distinguish when
interpreting an Egg/OPM waterflood experiment, particularly reservoir/grid
pressure versus well bottom-hole pressure and any pressure target/limit?

### Why this matters

Pressure quantities may feed observations, CRM predictions, constraints,
validation, and mismatch calculations. Treating them as interchangeable could
invalidate the control and safety logic.

### Current understanding

AURORA treats each pressure representation as a separate semantic object and
will not freeze exact OPM quantities until the configured simulator outputs are
verified.

### Decision affected

Issues #5, #6, #12, #30, #31, #32, #33.

---

## Q2 — OPM rate sign conventions and quantity identity

### Question

For the OPM outputs AURORA is likely to use, what must be verified before
interpreting injection and production rates: sign convention, surface versus
reservoir basis, phase, well/field scope, target versus realized value, or
other semantics?

### Why this matters

A sign or basis mistake could invert a controller signal, corrupt a residual,
or make two incompatible quantities appear comparable.

### Current understanding

No sign convention or exact rate vector is considered frozen until verified
against the applicable OPM version/configuration.

### Decision affected

Issues #5, #7, #12, #24.

---

## Q3 — Requested versus effective well control

### Question

In the intended Egg/OPM setting, what is the correct way to determine whether
a requested well target was actually the effective limiting control at a
particular report/control step?

### Why this matters

AURORA must distinguish proposed action, safety-filtered action,
simulator-requested control, effective control, and realized response.

### Current understanding

The requested target alone is not treated as proof that it governed the well.

### Decision affected

Issues #5, #7, #12, #23, #24.

---

## Q4 — Physically meaningful action candidates

### Question

Which candidate well-control quantities are physically meaningful for the
specific Egg waterflood experiment, and which would be poor choices for the
controller action vector even if OPM technically exposes them?

### Why this matters

Simulator capability does not automatically imply a sensible control action.

### Current understanding

AURORA has intentionally not frozen the action vector.

### Decision affected

Issue #5.

---

## Q5 — Observation candidates and hidden/full-state leakage

### Question

Which reservoir/well quantities would be defensible controller observations
for this experiment, and which quantities should be treated as simulator-only
validation state rather than controller-visible information?

### Why this matters

Giving the controller inappropriate simulator state could eliminate the
partial-observability problem or create future/reference leakage.

### Current understanding

Availability in simulator output does not automatically authorize a quantity
as an RL observation.

### Decision affected

Issues #5, #7, #27, #28, #29.

---

## Q6 — Physical limits versus experimental bounds

### Question

For candidate pressure/rate/action bounds, which values could legitimately be
described as physical or operational constraints, and which should instead be
described only as simulator limits, experimental bounds, warning thresholds,
or expected ranges?

### Why this matters

AURORA must not transform a convenient Egg/Volve range into an unsupported
physical safety claim.

### Current understanding

No final numerical physical/safety limit is currently frozen.

### Decision affected

Issues #6, #31, #33.

---

## Q7 — Waterflood response plausibility

### Question

Which qualitative relationships among injection, production, pressure, water
production, and time are sufficiently general to use as plausibility checks,
and which depend too strongly on reservoir/configuration context to automate
without additional evidence?

### Why this matters

The project needs scalable validation but must not encode oversimplified
reservoir heuristics as universal laws.

### Current understanding

Cross-variable checks are desirable, but contextual relationships should
remain warnings/review triggers unless strongly justified.

### Decision affected

Issues #4, #6, #12, #26.

---

## Q8 — Injector-producer connectivity evidence

### Question

What evidence would be sufficient to make a bounded claim about
injector-producer connectivity or influence in an Egg realization?

### Why this matters

AURORA should not treat simple contemporaneous correlation as causal
connectivity.

### Current understanding

Candidate evidence includes controlled perturbation, lagged response,
model-identification behaviour, consistency across realizations, and domain
reasoning.

### Decision affected

Issues #30, #32.

---

## Q9 — CRM formulation suitability

### Question

For AURORA's intended use as a fast reduced-order model in or near a safety
filter, which CRM/CRMIP formulation family and assumptions deserve serious
consideration, and what failure modes or limitations are most important?

### Why this matters

The exact CRM structure determines what can be predicted, what mismatch means,
and what the QP can legitimately use.

### Current understanding

CRM is only a candidate model family; no exact formulation has been frozen.

### Decision affected

Issues #30, #31, #32, #33.

---

## Q10 — Meaningful OPM-versus-CRM mismatch

### Question

What constitutes a physically and experimentally meaningful comparison between
CRM predictions and OPM reference behaviour?

Please consider quantity identity, units, temporal alignment, control history,
well identity, fitting/calibration conditions, and direction of error.

### Why this matters

A numerical residual is meaningless if the compared quantities are not
semantically aligned.

### Current understanding

AURORA requires quantity/entity/unit/time alignment before interpreting
OPM-versus-CRM residuals.

### Decision affected

Issues #30, #32, #33.

---

## Q11 — Mismatch relevance to constraints

### Question

For a selected constraint quantity, when can model mismatch reasonably be
treated as safety-relevant rather than merely predictive error?

### Why this matters

AURORA's differentiating research question depends on mismatch-aware safety
logic, but not every model error has the same consequence.

### Current understanding

The direction and consequence of mismatch must be interpreted relative to the
specific encoded constraint and operating/experimental envelope.

### Decision affected

Issues #32 and #33.

---

## Q12 — Abnormal but plausible outputs

### Question

What examples of unusual-looking Egg/OPM behaviour could still be physically
or numerically plausible and therefore should not automatically invalidate a
run?

### Why this matters

The validation system needs to avoid treating every unusual result as a
physical impossibility or safety violation.

### Current understanding

Potential benign explanations include transients, changed control mode,
realization differences, unit/sign mistakes, timing differences, and numerical
or configuration effects. These explanations must themselves be checked.

### Decision affected

Issues #4, #12, #26, #34.

---

## Q13 — Automatic validation versus expert review

### Question

Which domain checks in this project are safe to automate deterministically,
which should produce only a warning/review request, and which fundamentally
require contextual expert interpretation?

### Why this matters

The team needs scalable validation without pretending software can replace
reservoir-engineering judgment.

### Current understanding

Structural semantics/provenance checks are good automation candidates.
Context-sensitive physical interpretation should remain bounded by evidence.

### Decision affected

Issues #4, #12, #26.

---

## Q14 — Claim boundaries

### Question

Are there any statements in the following claim boundary that should be
tightened?

> Egg is a synthetic benchmark. OPM Flow provides a higher-fidelity numerical
> reference for the configured experiment. CRM is a simplified predictive
> model. Agreement with OPM does not establish real-field validity. A
> QP-style safety filter enforces only its encoded model/constraints under its
> documented assumptions and does not establish unconditional physical safety.

### Why this matters

These boundaries affect the proposal, final report, demonstration, and any
publication-style claims.

### Decision affected

Issues #13, #26, #39, #40, #43.

---

## Q15 — Missing high-consequence misconception

### Question

Given the intended architecture above, what is the single most consequential
reservoir-engineering misconception a software-engineering team is likely to
make that is **not already covered by Questions 1–14**?

### Why this matters

This gives the reviewer one deliberately bounded opportunity to identify a
high-risk blind spot without turning the review into an open-ended redesign.

---

# Review resolution record

After review, AURORA should record each material answer as one of:

- `SOURCE_BACKED`
- `EXPERT_REVIEWED`
- `PROVISIONAL`
- `UNRESOLVED`
- `SUPERSEDED`

For each resulting change, record:

| Question | Reviewer conclusion | Evidence | AURORA decision | Artifact changed | Remaining uncertainty |
|---|---|---|---|---|---|
| Q1 | | | | | |
| Q2 | | | | | |
| Q3 | | | | | |
| Q4 | | | | | |
| Q5 | | | | | |
| Q6 | | | | | |
| Q7 | | | | | |
| Q8 | | | | | |
| Q9 | | | | | |
| Q10 | | | | | |
| Q11 | | | | | |
| Q12 | | | | | |
| Q13 | | | | | |
| Q14 | | | | | |
| Q15 | | | | | |

## Exit condition

The review is useful only when its consequential conclusions are transferred
into canonical AURORA artifacts, source records, validation rules, or explicit
unresolved assumptions.

The completed packet itself is evidence of review; it is not a substitute for
updating the controlled engineering record.
