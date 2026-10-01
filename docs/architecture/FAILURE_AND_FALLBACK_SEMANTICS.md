# Failure and Fallback Semantics

## Purpose

AURORA must fail explicitly rather than manufacture plausible-looking reservoir-control results.

The machine-readable authority is `configs/architecture/FAILURE_SEMANTICS.yaml`.

## Distinction: rejection versus failure

A safety-layer `REJECT` is a legitimate closed-loop decision.

It means the proposed action was not authorized under the encoded model, constraints, and available evidence.

It does **not** prove that the proposal was physically unsafe in a real reservoir.

A numerical solver crash, malformed controller output, missing required observation, or simulator failure is different: those are execution failures.

## Fail-closed action application

When a required observation, proposal, or safety evaluation is invalid, AURORA does not send the raw controller proposal to the simulator.

The default software semantic is to apply **no newly proposed action for that failed step** or terminate the run according to the failure class.

`HOLD_NO_NEW_ACTION` is not a reservoir-safety claim. It only defines what AURORA's software does when it cannot authorize a new action.

## Failure families

The registry covers:

- missing, non-finite, or semantically unresolved observations;
- malformed or numerically invalid controller output;
- insufficient safety evidence;
- infeasible or numerically failed safety optimization;
- invalid applied actions;
- simulator control rejection;
- simulator numerical failure;
- incomplete simulator outputs;
- required provenance-write failure;
- step identity mismatch;
- unsupported contract versions.

## Retry policy

Retry is not a generic fallback.

Only failures explicitly marked retryable may be retried, and retry must repeat the same operation rather than alter reservoir-control intent.

A failed required provenance write is initially retryable because persistence can fail transiently. If evidence still cannot be persisted, the run terminates rather than continuing without reconstructable provenance.

## Prohibited recovery

Automatic recovery may never:

- bypass the safety filter;
- replace required missing observations with zero;
- silently reuse stale observations;
- invent pressure limits or action bounds;
- treat Egg baseline controls as safe fallback controls;
- convert simulator failure into a successful experiment step.

## Why this matters

AURORA's scientific results are meaningful only if failed runs, rejected proposals, degraded inputs, and successful control steps remain distinguishable.

A visually plausible trajectory produced after silent failure recovery would be worse than an explicit failed run because it could support an invalid engineering claim.


## Out-of-range observations

A value is treated as out-of-range only when an explicit, provenance-backed
experiment or interface envelope exists for that quantity.

Crossing such an envelope blocks the current action path and produces
`OBSERVATION_OUT_OF_DECLARED_ENVELOPE`.

This means the value is unsupported for the declared scope. It does not automatically
mean the reservoir state is physically unsafe.

## Robustness-test traceability

Each candidate failure behaviour has a stable `ROB-*` scenario identifier in the
machine-readable failure registry.

Later robustness work can inject the corresponding malformed input, numerical
failure, simulator failure, telemetry failure, identity mismatch, or schema mismatch
and verify the expected fallback deterministically.

This architecture phase defines the expected behaviour; later robustness phases
implement and execute the fault-injection experiments.
