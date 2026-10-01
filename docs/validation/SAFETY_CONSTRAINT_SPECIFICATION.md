# Candidate Safety Constraint and Threshold Specification

## Purpose

This document is the human-readable companion to
`configs/safety/CONSTRAINT_REGISTRY.yaml`.

AURORA's safety layer can reason only about constraints represented in its
model. Therefore every constraint must state exactly what quantity is bounded,
what mathematical relationship is enforced, what units apply, where any
threshold came from, and what claim the result supports.

## Constraint classes

AURORA distinguishes:

- hard physical/domain constraints;
- encoded safety-controller constraints;
- simulator control/limit constraints;
- experimental bounds;
- warnings;
- statistical anomaly thresholds;
- expected ranges; and
- performance targets.

These classes must not be silently collapsed into one generic concept of a
"limit."

## Threshold provenance

A numerical threshold is not admissible merely because it is convenient or
observed in data.

Every numerical threshold must identify its:

- value and unit;
- constraint/threshold class;
- quantity and scope;
- provenance;
- evidence/assumption status;
- interpretation and limitations.

In particular, a historical Volve range, Egg baseline range, percentile, or
round number cannot become a hard physical/safety limit without separate
justification.

## Margin semantics

For encoded constraints, the canonical convention is:

`margin > 0` — inside the encoded admissible region.

`margin = 0` — on the encoded boundary, subject to declared numerical tolerance.

`margin < 0` — encoded constraint violation.

A **near miss** exists only if a separate warning threshold has been explicitly
defined and justified. AURORA does not assume a universal near-miss distance.

These semantics concern the encoded experiment/model. They do not by themselves
establish real-field physical safety or unsafety.

## Current candidate constraints

### CTR-001 — selected pressure constraint

A pressure-derived encoded constraint is a candidate because pressure is
potentially relevant to the safety formulation.

Still unresolved:

- exact pressure quantity;
- selected wells/scope;
- lower/upper/both formulation;
- numerical threshold;
- threshold provenance.

No numerical pressure limit is frozen by this specification.

### CTR-002 — controller action bound

Action bounds are candidates because controller and safety optimization require
a defined admissible action space.

Still unresolved:

- final controlled wells;
- final action quantity;
- lower and upper numerical bounds;
- provenance/evidence basis.

No numerical rate bound is frozen by this specification.

### CTR-003 — warning/anomaly criterion

Warnings may be useful for telemetry and result interpretation, but unusual
behaviour is not automatically a physical violation.

No warning threshold is frozen until its monitored quantity and evidence basis
are defined.

## Relationship to later QP work

This specification gives the later safety/QP work typed inputs:

- named quantities;
- units;
- constraint classes;
- mathematical-form placeholders;
- provenance requirements;
- margin/violation semantics;
- explicit unresolved thresholds.

The QP implementation must consume the eventual frozen registry rather than
introducing hidden limits in source code.

## Egg baseline evidence boundary

The supplied Egg benchmark gives AURORA concrete evidence about the baseline
model and schedule without automatically freezing the autonomous-control
interface.

The audited benchmark contains eight water injectors and four producers. The
supplied schedule uses `WCONINJE` water-injection `RATE` control with a raw
baseline value of `79.5` for each injector, while the producers use
`WCONPROD` `BHP` control with a raw baseline value of `395`. The supplied
schedule contains 120 intervals of 30 days.

These are benchmark facts, not universal reservoir rules or automatically
selected AURORA limits:

- `79.5` is a supplied Egg baseline injection setting, not an AURORA action
  bound or physical/safety limit.
- `395` is a supplied Egg producer-BHP control value, not an AURORA pressure
  safety threshold.
- The raw injector value `420` remains semantically **UNRESOLVED** until its
  exact deck-field position is verified against authoritative keyword
  semantics.
- The supplied 30-day schedule spacing does not by itself establish AURORA's
  final autonomous controller intervention interval.
- A requested simulator summary quantity is not evidence that a successful OPM
  execution actually generated and exposed that quantity.

Therefore Egg evidence can justify candidate quantity and control families
without automatically freezing final observation membership, final action
membership, numerical admissible ranges, encoded safety limits, or autonomous
control cadence.
