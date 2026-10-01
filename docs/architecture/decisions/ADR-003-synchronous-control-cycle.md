# ADR-003: Use a synchronous stepwise control cycle for the engineering baseline

## Status

Accepted for architecture freeze.

## Context

AURORA must connect simulator, controller, safety evaluation, action application, and telemetry while preserving deterministic step identity.

## Alternatives considered

1. Asynchronous event-driven control.
2. Multiple independently scheduled subsystem loops.
3. One explicit synchronous stepwise orchestration cycle.

## Decision

Use alternative 3 for the engineering baseline.

## Rationale

The synchronous cycle is easier to reproduce, validate, instrument, and explain. It also prevents races between proposal, safety evaluation, and simulator application.

## Consequences

A control step has one ordered lineage.

This decision freezes ordering, not the numerical duration of a control interval.

Future asynchronous execution would require a new architecture decision and equivalent provenance guarantees.

## Evaluation criteria

- deterministic ordering;
- simple step identity and provenance;
- reproducible experiments;
- no race between proposal, safety evaluation, and simulator application;
- suitability for the current simulator-driven engineering baseline.

## Trade-offs

A synchronous loop sacrifices potential asynchronous throughput and concurrency.
AURORA accepts that cost for the baseline because experiment reproducibility and
unambiguous decision lineage are currently more important than control-loop
throughput.

## Evidence

The candidate semantics from #5 already define an ordered simulator → observation →
proposal → safety → applied-action → simulator → telemetry cycle. The architecture
registry preserves that ordering while deliberately leaving numerical cadence
unresolved.

Traceability: AUR-REQ-007, AUR-REQ-010, AUR-REQ-011; issues #5, #7, #8.
