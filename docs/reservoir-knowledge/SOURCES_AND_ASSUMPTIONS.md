# Sources and Assumptions Register

## Purpose

This document defines how AURORA grounds domain-sensitive statements and records
assumptions.

It is a source-governance document, not a bibliography dump.

## Source hierarchy

Use the most direct authoritative source appropriate to the claim.

### Tier A — primary / authoritative technical sources

Examples:

- official OPM documentation for OPM behaviour and simulator semantics;
- canonical Egg dataset/publication for Egg structure;
- Equinor documentation/licence for Volve provenance and usage conditions;
- primary peer-reviewed work for a specific model/method.

### Tier B — peer-reviewed technical literature

Use for equations, methods, empirical findings, comparisons, and domain relationships
not defined by a primary software/data source.

### Tier C — established textbooks/reference works

Use for stable reservoir-engineering fundamentals.

### Tier D — qualified domain review

Use to review bounded assumptions, interpretations, proposed operating logic, and
questions for which documentary evidence alone is insufficient.

Qualified review supplements evidence. It should not become an undocumented oracle.

### Tier E — AURORA experiments

Use to establish behaviour of AURORA under defined experimental conditions.

AURORA's own experiments do not establish general petroleum-engineering truth.

## Canonical current sources

### Egg Model

Jansen et al., canonical Egg Model dataset / associated publication.

DOI:

https://doi.org/10.4121/uuid:916c86cd-3558-4672-829a-105c62985ab2

Supported use:

- benchmark identity;
- ensemble structure;
- synthetic/channelized nature;
- waterflood configuration;
- canonical well counts;
- benchmark provenance.

### OPM Flow

Official OPM Flow page:

https://opm-project.org/?page_id=19

Official Flow manual page:

https://opm-project.org/?page_id=955

Supported use:

- simulator role/capabilities;
- input/output semantics;
- supported controls/constraints;
- simulator-specific interpretation.

Version-sensitive semantics must be checked against the version actually used by
AURORA.

### Volve

Official Equinor Volve page:

https://www.equinor.com/energy/volve-data-sharing

Local licence copy:

`../../references/volve/Equinor_Volve_Data_Licence.pdf`

Supported use:

- dataset provenance;
- real-field status;
- release purpose;
- licensing/usage context.

The exact semantics of individual workbook columns require the applicable metadata,
documentation, or defensible cross-check. They must not be guessed from column names
alone.


## Domain-fundamentals grounding

The following source classes ground stable reservoir concepts used by AURORA.
They do **not** freeze project-specific numerical limits, controller variables,
or safety constraints.

### Reservoir-flow fundamentals

For stable concepts such as porosity, permeability, saturation, pressure-driven
flow, multiphase reservoir behaviour, well behaviour, and waterflooding,
AURORA should rely on established reservoir-engineering references or
peer-reviewed literature appropriate to the exact claim.

These sources may support qualitative physical meaning and established
relationships. They do not automatically support a project-specific numerical
threshold.

### OPM-specific semantics

OPM-specific behaviour must be grounded in the documentation for the version
actually used by AURORA.

The official OPM Flow documentation establishes, among other capabilities, that
Flow is a fully implicit black-oil reservoir simulator and supports well
constraints including bottom-hole pressure, tubing-head pressure, and
surface/reservoir rates.

Canonical entry points:

- https://opm-project.org/?page_id=19
- https://opm-project.org/?page_id=955

Exact keyword, summary-vector, unit, sign, report-step, control-mode, and output
semantics must be verified against the applicable Flow release and experiment
configuration before becoming frozen AURORA semantics.

### Waterflood interpretation

AURORA may rely on established reservoir-engineering sources for the general
facts that injection and production interact through reservoir dynamics and
that response depends on the reservoir model, connectivity, fluid/rock
properties, well configuration, controls, and time.

AURORA must **not** infer a specific injector-producer causal relationship from
a simple contemporaneous correlation alone.

Project-specific connectivity or response claims require evidence appropriate
to the experiment, such as controlled perturbation, model identification,
cross-realization analysis, or qualified review.

### CRM / reduced-order modelling

Capacitance-resistance-model literature is the appropriate evidence class for
claims about CRM structure, assumptions, identification, connectivity
parameters, time response, and predictive limitations.

Until AURORA selects and records a specific CRM/CRMIP formulation, the project
must not silently treat one literature formulation as the canonical
implementation.

The selected primary CRM source(s), equations, parameter semantics, fitting
procedure, assumptions, and validation envelope must be recorded as part of the
controlled CRM design decision before the reduced-order model is considered
frozen.

### Evidence-to-claim rule

For every domain-sensitive statement used in design or evaluation, ask:

1. What exact claim are we making?
2. Which source or experiment supports that exact claim?
3. Is the evidence simulator-specific, benchmark-specific, general domain
   knowledge, project experimental evidence, or qualified review?
4. Does the evidence justify a qualitative relationship only, or also a
   numerical value?
5. Under what conditions does the statement hold?
6. What stronger interpretation remains unsupported?

A source is not sufficient merely because it discusses the same topic.


## Assumption states

Every material domain assumption should be identifiable as one of:

- **SOURCE-BACKED** — directly supported by an appropriate source;
- **EXPERIMENTALLY SUPPORTED** — supported within defined AURORA experiments;
- **EXPERT-REVIEWED** — reviewed by a suitably qualified person;
- **PROVISIONAL** — plausible working assumption awaiting stronger support;
- **UNRESOLVED** — insufficient basis for use as a controlled assumption;
- **SUPERSEDED** — retained historically but replaced.

## Assumption record

For a material assumption record:

| Field | Meaning |
|---|---|
| ID | stable identifier |
| Statement | exact assumption |
| Status | state from above |
| Scope | where it applies |
| Evidence | source/experiment/review |
| Risk if wrong | engineering/scientific consequence |
| Resolver | person/task responsible |
| Resolution condition | evidence required to close it |

## Current high-priority unresolved assumptions

The project must not silently invent:

- operational pressure limits;
- injection/production action bounds;
- control interval;
- exact observation availability;
- exact CRM formulation;
- exact mismatch-calibration method;
- reward weights;
- final safety constraints;
- statistical alarm thresholds;
- protected evaluation methodology.

These should become explicit issue/decision records as their roadmap gates are reached.

## Expert review package

A bounded expert review should eventually ask focused questions such as:

1. Are the selected reservoir quantities interpreted correctly?
2. Are the proposed control variables physically meaningful in the chosen experiment?
3. Are candidate constraint types defensible for the stated experiment?
4. Are any simulator quantities being mistaken for real-field measurements?
5. Are the proposed comparisons physically meaningful?
6. Are important confounders or missing variables being overlooked?
7. Are the project's claim boundaries appropriately conservative?
8. Which assumptions most need correction before final evaluation?

The expert should not be asked to validate every simulation run.
