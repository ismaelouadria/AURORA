# Validation and Interpretation

## Purpose

This directory defines how AURORA decides whether an artifact, datum, behaviour, or
result is:

- structurally valid;
- experimentally valid;
- domain-plausible;
- meaningful;
- unusual;
- concerning;
- constraint-violating;
- unsupported; or
- outside the project's claim boundary.

## Canonical documents

| Question | Document |
|---|---|
| What are AURORA's validation levels and rules? | `VALIDATION_SPECIFICATION.md` |
| How should a number/result be interpreted? | `INTERPRETATION_FRAMEWORK.md` |
| What kind of threshold/constraint is this and why? | `CONSTRAINT_AND_THRESHOLD_REGISTER.md` |
| How do I document interpretation for a task? | `DATA_INTERPRETATION_CONTRACT.md` |
| What does the variable itself mean? | `../data-and-logging/DATA_DICTIONARY.md` |
| What reservoir knowledge supports the interpretation? | `../reservoir-knowledge/` |

## Core rule

A result is not understood merely because it has been computed.

A metric becomes evidence only when its semantics, comparator, expected behaviour,
uncertainty, significance, provenance, and claim boundary are sufficiently understood.

## Validation is layered

AURORA distinguishes:

1. implementation correctness;
2. experimental correctness;
3. domain plausibility/grounding; and
4. real-field validity.

Passing one layer does not imply passing the next.


## Machine-readable foundation

Deterministic and policy-level domain-validation rules that are justified
before the final architecture is frozen are registered in:

`../../configs/validation/DOMAIN_INTERPRETATION_RULES.yaml`

Validate the registry with:

    python3 scripts/validation/validate_domain_rules.py

The registry deliberately does not invent unresolved numerical reservoir
thresholds. The richer result-interpretation system is implemented later under
the dedicated result-interpretation workstream.
