# ADR-005: Telemetry is an observer and evidence system, not a control authority

## Status

Accepted for architecture freeze.

## Context

AURORA needs enough evidence to reconstruct decisions, interventions, failures, and outcomes. Coupling logging with control authority would make the control path harder to reason about and test.

## Alternatives considered

1. Telemetry may modify or repair actions.
2. Telemetry and orchestrator jointly own action decisions.
3. Telemetry records control-cycle artifacts but never authorizes or modifies actions.

## Decision

Use alternative 3.

## Consequences

Telemetry records state, observation, proposal, safety decision, applied action, simulator outcome, and failures.

A required evidence-write failure can block the run because reproducibility is part of experimental validity, but telemetry still does not choose the reservoir-control action.

## Evaluation criteria

- reconstructable control-step evidence;
- no second action-authority path;
- independent telemetry implementation;
- failures remain observable even when execution stops.

## Trade-offs

Making required provenance persistence run-blocking can reduce availability when
logging infrastructure fails. AURORA accepts this for controlled experiments because
a run whose consequential decisions cannot be reconstructed is not adequate evidence
for later scientific claims.

## Evidence

AUR-REQ-011 requires observable decisions and AUR-REQ-018 requires provenance.
The failure registry explicitly handles required provenance-write failure without
granting telemetry authority to alter reservoir-control decisions.

Traceability: AUR-REQ-011, AUR-REQ-018; issues #7, #8, #9.
