# Telemetry and Provenance

AURORA telemetry is an observer, not a control authority.

Every completed MVP control step records:

- run identity;
- Git commit;
- deterministic seed;
- configuration;
- reference/environment identity;
- observation;
- proposed action;
- safety disposition and intervention reason;
- applied action;
- simulator/environment outcome;
- failure/degraded-mode field.

The machine-readable step schema is
`configs/telemetry/STEP_TELEMETRY_SCHEMA.json`.

Required telemetry persistence is fail-visible. A required provenance write
failure raises `REQUIRED_PROVENANCE_WRITE_FAILED`; it is not converted into a
successful experiment step.

Telemetry must preserve domain semantics rather than infer them. An unusual
value is not automatically invalid, a historical range is not automatically a
physical limit, an encoded safety decision is not proof of real-field physical
safety, and simulator output is numerical reference evidence rather than
physical ground truth.

The JSONL representation is intentionally simple so experiment, validation,
result-interpretation, and demo tooling can consume the same evidence stream.
