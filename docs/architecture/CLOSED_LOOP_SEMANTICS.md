# Closed-Loop Observation, Action, and Control Semantics

## Purpose

This document is the human-readable companion to
`configs/interfaces/CLOSED_LOOP_SEMANTICS.yaml`.

It defines the candidate semantic contract needed by AURORA's simulator,
controller, safety layer, telemetry, and experiment system before architecture
freeze.

It does **not** claim that every candidate quantity is a final controller input
or action.

## Canonical cycle

AURORA's candidate closed-loop ordering is:

1. simulator state exists at the current decision boundary;
2. named physical quantities are extracted;
3. observation semantics and validity are checked;
4. the controller/baseline creates a **proposed action**;
5. the safety layer evaluates encoded constraints;
6. the safety layer emits an **applied action**;
7. the adapter maps that action to verified simulator-control semantics;
8. the simulator advances one configured control interval;
9. telemetry preserves the full decision record.

The proposed action and applied action are different semantic objects even when
their numerical values happen to be identical.

## Observation candidates

The registry currently represents candidate well bottom-hole pressure,
well phase rates, and cumulative named phase volumes.

Their presence in simulator output or telemetry does not automatically make them
valid RL observations. Final observability is an architecture decision and must
avoid accidental full-state leakage.

Every observation must preserve:

- quantity identity;
- well identity and role where applicable;
- physical units;
- sign convention;
- simulator time/control step;
- realization/configuration identity;
- missing/non-finite handling;
- source and transformations;
- interpretation status.

Pressure quantities are not interchangeable. Rate and cumulative quantities are
not interchangeable.

## Action candidates

The current candidate is a per-well rate target represented canonically by a
nonnegative magnitude plus explicit well role.

This is intentionally an interface convention, not a claim that rate control is
the final AURORA action space.

Simulator-specific signs or control keywords belong at the simulator-adapter
boundary and must be verified against the actual OPM configuration.

## Control interval

The exact control interval remains **UNRESOLVED**.

No controller, simulator adapter, reward calculation, CRM update, or experiment
may silently invent a default control interval. The selected interval must
eventually be explicit experiment configuration with units.

## Mapping boundary

### Simulator → controller

Raw simulator output must first become named, unit-bearing, time-indexed,
provenance-bearing quantities. Only then may explicitly selected quantities be
transformed into a controller observation.

### Controller → safety → simulator

The controller emits a proposed action. The safety layer emits the applied
action. The simulator receives only the applied action through a verified
adapter.

Telemetry must preserve both.

## Decisions deliberately not frozen here

- final observation-vector membership;
- final action-vector membership;
- exact OPM summary-vector identities;
- exact OPM control keywords;
- OPM rate sign semantics;
- normalization/scaling;
- numerical action bounds;
- numerical safety bounds;
- exact control interval.

Those are not omissions to hide. They are explicit unresolved decisions that
later evidence must close.

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
