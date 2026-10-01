# Closed-Loop Architecture Freeze

## Status

This document freezes AURORA's **software responsibility and authority boundaries** for architecture review.

It does **not** freeze reservoir quantities that remain unresolved in the domain, interface, or constraint registries.

## Core loop

AURORA executes one explicit stepwise control cycle:

1. simulator adapter reads simulator state;
2. observation adapter constructs the allowed observation;
3. controller proposes an action;
4. safety filter evaluates the proposal;
5. action adapter constructs the applied action from the safety disposition;
6. simulator adapter applies only the applied action;
7. simulator advances;
8. telemetry records the reconstructable step.

The numerical control interval remains unresolved.

## Authority boundary

The central architectural invariant is:

**controller proposal != safety authorization != applied simulator control**

The controller owns proposal generation. It does not own simulator authority.

The safety filter owns encoded safety evaluation. It does not establish universal real-field physical safety.

The action adapter preserves the lineage between the proposal, safety disposition, and applied action.

The simulator adapter owns simulator-specific translation and execution. It does not choose actions.

Telemetry observes and records. It does not control.

## Component contracts

### Simulator adapter

Owns simulator session state and simulator-step identity.

It isolates OPM-specific or other simulator-specific details from the controller and safety layers.

It exposes only explicitly mapped outputs and receives only validated `applied_action` records.

### Observation adapter

Maps simulator outputs into controller-visible quantities.

A quantity being available from OPM does not make it observable by the controller.

The adapter is responsible for quantity identity, unit/sign semantics, missing-value validity, well identity, and visibility.

### Controller

Consumes a valid observation and emits `proposed_action`.

Recurrent implementations may own controller memory.

The controller cannot command the simulator directly and cannot label its own action physically safe.

### Safety filter

Consumes the observation and proposed action and returns an explicit safety disposition.

The candidate dispositions are `ACCEPT`, `MODIFY`, `REJECT`, `INSUFFICIENT_EVIDENCE`, and `NUMERICAL_FAILURE`.

Acceptance is relative to the encoded model and constraints.

### Action adapter

Constructs the canonical `applied_action`.

It is deliberately separate from the controller so proposed and applied actions remain distinguishable and auditable.

### Telemetry

Records the chain needed to reconstruct what happened:

simulator state → observation → proposal → safety disposition → applied action → simulator outcome.

Telemetry has no action authority.

### Orchestrator

Owns cycle progression, not reservoir-control policy.

It enforces ordering, propagates failures, and prevents downstream stages from running after a blocking failure.

## State ownership

State ownership is explicit:

- simulator physical/session state → simulator adapter
- observation transformation → observation adapter
- policy/recurrent memory → controller
- reduced-order/safety evaluation state → safety filter
- proposed/applied lineage → action adapter
- run and step evidence → telemetry
- cycle progression → orchestrator

This prevents accidental hidden coupling.

## Frozen architecture invariants

The machine-readable registry is authoritative for exact invariant text.

The most important consequences are:

- controller cannot bypass safety;
- simulator receives applied action, not raw controller output;
- proposed and applied actions remain distinct even when equal;
- full simulator state is not automatically controller state;
- missing/non-finite required data cannot silently become valid;
- safety failure cannot silently become pass-through;
- benchmark settings cannot silently become physical limits;
- numerical control cadence remains unresolved;
- completed steps must be reconstructable.

## Deliberately unresolved

Architecture freeze does not manufacture answers to domain questions.

Still unresolved are final observation membership, final action membership, numerical cadence, exact OPM mappings, numerical action bounds, physical safety thresholds, final CRM formulation, and final learned-controller implementation.

Those items require their own evidence and decisions.

## Relationship to later implementation

This architecture is the contract against which the simulator, controller, safety layer, telemetry, and experiment infrastructure can evolve independently.

An implementation may change internally without changing architecture provided it preserves these contracts and invariants. Consequential contract changes require an explicit decision record.


## Explicit interface contract dimensions

Every major interface specifies six dimensions so adjacent subsystem owners can
implement independently:

1. **input/output** — the record crossing the boundary;
2. **timing** — where the exchange occurs in the synchronous control cycle;
3. **configuration** — controlled configuration required to interpret or execute it;
4. **ownership** — which subsystem constructs, transforms, validates, or persists it;
5. **errors** — named failure semantics when the contract cannot be honoured;
6. **compatibility** — schema version, identity, and semantic references that must
   agree before consumption.

The machine-readable source is
`configs/architecture/CLOSED_LOOP_ARCHITECTURE.yaml`.

`validate_architecture.py` verifies the required interface dimensions and authority
invariants automatically. Runtime schema validation can become stricter as concrete
Python data models are implemented, without changing these frozen responsibility
boundaries.
