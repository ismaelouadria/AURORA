# ADR-001: Safety authority sits between controller proposal and simulator application

## Status

Accepted for architecture freeze.

## Context

AURORA requires learned control and a separate safety mechanism. If the controller can directly command the simulator, the safety layer becomes observational rather than authoritative.

## Alternatives considered

1. Controller directly commands simulator; safety only logs.
2. Controller and safety both independently write controls.
3. Controller proposes; safety evaluates; only an applied action crosses the simulator boundary.

## Decision

Use alternative 3.

## Consequences

The controller emits `proposed_action`.

The safety path emits an explicit disposition.

The simulator adapter accepts only `applied_action`.

This creates a single authority path and makes intervention measurable.

## Claim boundary

This architecture enforces software authority. It does not prove the encoded safety model represents all real reservoir hazards.

## Evaluation criteria

- impossible to bypass safety through the normal control path;
- one unambiguous simulator-control authority path;
- proposed versus applied actions remain observable;
- independently testable controller and safety components.

## Trade-offs

The selected design adds an explicit safety/action boundary and therefore more
interfaces than direct controller-to-simulator wiring. The additional boundary is
accepted because it makes intervention, rejection, and authority mechanically
observable and testable.

## Evidence

The candidate interface semantics already distinguish proposed and applied actions.
The architecture validator and tests enforce that the controller cannot directly
apply simulator actions and that simulator-bound controls cross the safety boundary.

Traceability: AUR-REQ-010, AUR-REQ-011; issues #5, #6, #7, #8.
