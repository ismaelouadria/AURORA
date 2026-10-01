# ADR-004: Blocking failures do not pass controller proposals through

## Status

Accepted for architecture freeze.

## Context

A missing observation, malformed action, failed safety computation, or unresolved required constraint must not accidentally turn the safety layer into a pass-through path.

## Alternatives considered

1. Apply controller proposal when safety evaluation fails.
2. Substitute a convenient default action.
3. Authorize no new action and follow explicit failure semantics.

## Decision

Use alternative 3.

## Consequences

Blocking failures prevent raw proposals from reaching the simulator.

Some failures terminate the run; others hold application of a newly proposed action.

No fallback value is interpreted as physically safe merely because it is convenient.

## Claim boundary

Fail-closed is a software authority property. It is not a guarantee that unchanged reservoir controls are physically safe.

## Evaluation criteria

- safety failure cannot become silent pass-through;
- missing evidence cannot be replaced with invented control values;
- failure outcome is observable;
- behaviour can be fault-injection tested.

## Trade-offs

Blocking a new action can terminate or degrade experiments that a permissive system
might continue. That availability cost is accepted because silently applying an
unevaluated controller proposal would invalidate the intended safety architecture.

## Evidence

The domain and constraint registries prohibit unsupported numerical assumptions.
The failure registry maps blocking failures to explicit fallbacks and stable
robustness-test scenarios.

Traceability: AUR-REQ-009, AUR-REQ-010, AUR-REQ-019, AUR-REQ-021; issues #6, #8, #9.
