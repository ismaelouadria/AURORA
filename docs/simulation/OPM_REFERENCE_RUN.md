# Reproducible OPM Flow Reference Run

## Role

**Claim boundary:** OPM Flow is a numerical reference; it is not physical ground truth.

OPM Flow is AURORA's higher-fidelity numerical reference simulator. It is not
physical ground truth and successful execution does not establish real-field
validity or unconditional physical safety.

Feasibility evidence previously verified Egg with Flow 2026.04. The runtime
foundation turns that evidence into a repeatable project command.

## Environment

Use:

    ./aurora doctor

AURORA supports either:

- native `flow`; or
- the project Docker execution path using
  `openporousmedia/opmreleases:latest`.

The actual environment is captured in each run manifest. The preserved
feasibility reference version is not a claim that an unpinned `latest` image
will forever resolve to the same version; reproducible scientific experiments
must preserve the concrete version/image identity they actually use.

## Run

After preparing Egg:

    ./aurora opm run-reference \
      --deck-root data/egg/local \
      --output-dir runs/opm-reference

Success requires both a zero Flow exit status and the configured reference
products: `EGRID`, `INIT`, `SMSPEC`, `UNSMRY`, and `UNRST`.

`run_manifest.json` records the engine, command, deck checksum, environment,
exit status, and output inspection. `flow.log` preserves diagnostics.

## Failure semantics

A missing deck, missing simulator environment, non-zero Flow exit, or missing
required output product is explicit failure. A zero process status alone is not
enough.

Large generated simulator files remain local/regenerable rather than becoming
normal Git artifacts.
