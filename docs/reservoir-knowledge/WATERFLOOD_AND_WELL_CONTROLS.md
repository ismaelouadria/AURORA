# Waterflood and Well-Control Interpretation

## Purpose

This document connects waterflood/well concepts to AURORA's control problem.

It does not prescribe final operating limits or freeze the controller interface.

## Closed-loop interpretation

AURORA's intended loop is:

    reservoir simulation
        -> observation
        -> learned controller
        -> proposed action
        -> safety controller
        -> applied action
        -> reservoir evolution
        -> telemetry and validation
        -> next control step

The action applied to the simulator and the response observed afterward are different
events separated by reservoir dynamics and simulator evolution.

## Injection and production

Injection and production quantities may be represented as targets, realized rates,
limits, cumulative quantities, or other simulator outputs.

These categories must not be conflated.

For every well-related value used by AURORA, the data dictionary must eventually record:

- well identity;
- producer/injector role;
- physical quantity;
- requested versus realized status;
- units;
- sign convention;
- effective control semantics;
- time basis;
- source;
- missing/stale behaviour; and
- whether the controller can observe it.

## Well-control semantics

OPM Flow supports well constraints including bottom-hole pressure, tubing-head pressure,
and surface/reservoir rates.

That does not mean AURORA should use every available control.

The final action space must be justified against:

- experimental question;
- Egg configuration;
- simulator support;
- controllability;
- safety-layer formulation;
- interpretability; and
- integration complexity.

## Delayed and coupled effects

A control change may influence multiple later quantities.

Therefore AURORA should not interpret a simple contemporaneous correlation as proof of
causal injector-producer connectivity.

Potential evidence can include:

- controlled simulation perturbations;
- lagged response analysis;
- reduced-order model behaviour;
- consistency across realizations;
- physical/domain reasoning; and
- qualified review.

## Requested versus realized behaviour

The project must distinguish at least:

    proposed controller action
    safety-filtered action
    simulator-requested control
    effective simulator control
    realized reservoir/well response

If these differ, telemetry should preserve the difference rather than overwrite earlier
stages.

## Constraint interpretation

AURORA must distinguish:

- simulator control/limit semantics;
- project-defined experimental bounds;
- warning thresholds;
- optimization targets;
- statistical anomaly thresholds;
- encoded safety-controller constraints; and
- any externally justified physical/operational limit.

A numerical value does not become a safety limit merely because it appears in a
historical dataset or one simulation run.

See `../validation/CONSTRAINT_AND_THRESHOLD_REGISTER.md`.


## Evidence discipline

AURORA separates three different statements that are easy to conflate:

1. **General domain relationship** — supported by established
   reservoir-engineering knowledge or literature.
2. **Simulator/configuration behaviour** — supported by OPM documentation,
   the Egg configuration, and reproducible simulation evidence.
3. **AURORA experiment conclusion** — supported by the controlled experiment
   actually executed.

For example, reservoir-domain knowledge can justify investigating delayed and
coupled injector/producer response. It does not by itself establish the
connectivity strength, lag, or causal effect for a particular Egg realization.

Likewise, an observed Egg/OPM response establishes behaviour of that configured
numerical experiment. It must not be silently generalized into a real-field
operating claim.

When a relationship materially affects an AURORA design decision, validation
rule, constraint, or reported conclusion, preserve the evidence class and
claim boundary with the result.
