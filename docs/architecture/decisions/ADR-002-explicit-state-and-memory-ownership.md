# ADR-002: State and memory ownership is explicit

## Status

Accepted for architecture freeze.

## Context

A recurrent controller, simulator, reduced-order model, and telemetry system all carry state. Shared implicit mutable state would make experiments difficult to reproduce and subsystem failures difficult to diagnose.

## Alternatives considered

1. Shared global state.
2. Orchestrator owns all subsystem internals.
3. Each subsystem owns only its declared state; interfaces carry explicit records.

## Decision

Use alternative 3.

## Consequences

Controller memory remains controller-owned.

Simulator state remains simulator-adapter-owned.

Safety-model state remains safety-filter-owned.

Telemetry owns persisted experiment evidence.

The orchestrator owns progression but not subsystem algorithms.

This permits independent replacement and testing of components.

## Evaluation criteria

- deterministic and reconstructable experiment state;
- subsystem replacement without hidden shared-state assumptions;
- clear debugging responsibility;
- compatibility with recurrent controllers and stateful safety models.

## Trade-offs

Explicit ownership requires more structured records and plumbing than shared mutable
state. That overhead is accepted because hidden cross-component state would weaken
reproducibility and independent subsystem testing.

## Evidence

AURORA already requires explicit provenance and distinguishable control stages.
The architecture registry now assigns simulator, controller, safety, action-lineage,
telemetry, and orchestration state to named owners.

Traceability: AUR-REQ-007, AUR-REQ-011, AUR-REQ-017, AUR-REQ-018; issues #7 and #8.
