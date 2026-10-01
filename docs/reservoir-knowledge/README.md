# Reservoir Knowledge

## Purpose

This directory is AURORA's canonical home for reservoir-domain knowledge required
to design, interpret, and validate the software system responsibly.

The goal is not to turn the software team into reservoir engineers. The goal is to
prevent software decisions from depending on misunderstood variables, undocumented
physical assumptions, arbitrary thresholds, or unsupported interpretations.

AURORA uses reservoir engineering as its application domain. Domain-sensitive claims
must therefore be sourced, experimentally justified where appropriate, or explicitly
marked for qualified review.

## Start here

| Question | Canonical document |
|---|---|
| What reservoir concepts do I need to understand? | `RESERVOIR_DOMAIN_GUIDE.md` |
| How do waterflooding and well controls relate to AURORA? | `WATERFLOOD_AND_WELL_CONTROLS.md` |
| What do Egg, OPM Flow, Volve, and CRM each represent? | `MODEL_AND_DATA_ROLES.md` |
| What does a term mean? | `GLOSSARY.md` |
| Where did a domain statement or assumption come from? | `SOURCES_AND_ASSUMPTIONS.md` |
| What should a reservoir-domain expert review? | `EXPERT_REVIEW_PACKET.md` |
| What does an AURORA variable mean? | `../data-and-logging/DATA_DICTIONARY.md` |
| How should data be interpreted? | `../validation/INTERPRETATION_FRAMEWORK.md` |
| Why does a threshold or constraint exist? | `../validation/CONSTRAINT_AND_THRESHOLD_REGISTER.md` |
| How do I document interpretation for a new data-heavy task? | `../validation/DATA_INTERPRETATION_CONTRACT.md` |
| What makes a result valid? | `../validation/VALIDATION_SPECIFICATION.md` |

## Domain rule

No important reservoir-sensitive quantity may be used merely because the software can
read, calculate, or plot it.

Before a quantity supports a controller, safety decision, experiment, or report claim,
the project must understand enough of its:

- definition;
- units and sign convention;
- source and provenance;
- spatial and temporal meaning;
- expected behaviour;
- relevant relationships;
- limitations and uncertainty;
- validation basis; and
- claim boundary.

## Scope boundary

AURORA distinguishes:

1. implementation correctness;
2. correctness within the defined experiment;
3. reservoir-domain plausibility and grounding; and
4. real-field validity.

The first three are legitimate project targets.

The fourth is not established merely because AURORA uses a reservoir simulator,
a real-field dataset, or reservoir-engineering terminology.

OPM Flow with Egg is treated as a higher-fidelity numerical reference environment
for controlled experiments. It is not physical ground truth.

Volve is a separate real-field data resource used for grounding and interpretation.
It is not interchangeable with the Egg/OPM simulation environment.

## Historical feasibility material

`../feasibility/` contains valuable feasibility evidence gathered before the current
canonical documentation system was established.

Those reports remain evidence and design history. They do not automatically become
current specification.

If a historical feasibility statement conflicts with a later controlled specification,
the controlled specification governs and the reason for the change should be traceable.
