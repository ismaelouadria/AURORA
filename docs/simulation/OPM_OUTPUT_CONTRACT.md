# OPM Output Contract

AURORA downstream code consumes a standardized extraction boundary rather than
independently parsing raw OPM files.

The machine-readable authority is
`configs/simulation/OPM_OUTPUT_CONTRACT.json`.

The contract preserves source-run identity, simulator/configuration provenance,
vector identity, well identity where applicable, source metadata units, and
simulator timing/report identity.

The currently named field and well rate/cumulative families are quantities
already supported by AURORA's prior OPM feasibility evidence. Their presence in
the extraction contract does **not** make them final controller observations.

Pressure and saturation restart information may exist in `UNRST`, but restart
availability likewise does not authorize controller observability.

Extraction fails when a required requested vector cannot be demonstrated in the
source summary metadata. Units are not guessed from vector names. Missing or
invalid required output is never silently replaced with zero.

The final controller observation membership, normalization, autonomous control
interval, and numerical action/safety bounds remain separate engineering
decisions.
