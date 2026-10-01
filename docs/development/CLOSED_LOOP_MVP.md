# Closed-Loop Engineering MVP

**Scope boundary:** The toy environment is not a reservoir model. It exists only to exercise the software control loop.

The MVP proves AURORA's software authority path before expensive/full-physics
integration becomes a mandatory inner-loop dependency:

    environment
      -> observation
      -> controller proposed_action
      -> safety evaluation
      -> applied_action
      -> environment
      -> telemetry
      -> repeat

Run:

    ./aurora smoke

The deterministic toy environment is an integration test fixture, not a
reservoir model and not scientific evidence about reservoir behaviour.

The controller cannot send an action directly to the environment. The safety
filter produces the only `AppliedAction` accepted by the environment.

The MVP safety filter validates structural action semantics only. It does not
invent the unresolved reservoir pressure limits, action bounds, control
interval, CRM semantics, or calibrated mismatch mechanism.

Proposed and applied actions are always distinct records, including when their
numeric values happen to be identical.

This gives OPM, controller, CRM/QP, telemetry, and later experiment work a
stable executable seam while preserving the frozen architecture boundaries.
