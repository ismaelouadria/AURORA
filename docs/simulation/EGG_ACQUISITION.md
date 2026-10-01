# Egg Acquisition and Local Preparation

## Purpose

The Egg Model is an external synthetic reservoir benchmark used by AURORA.
Bulk Egg source packages and generated OPM simulation products are not committed
to this repository.

The authoritative project source record is the Egg Model publication/data source
already recorded by AURORA's reservoir-knowledge and feasibility evidence. The
canonical publication is Jansen et al., *The Egg Model — a geological ensemble
for reservoir simulation*, DOI `10.1002/gdj3.21`.

AURORA preserves source provenance and checksums rather than treating an
untracked developer folder as the benchmark definition.

## Fresh clone

1. Obtain the authoritative Egg archive identified by the project source record.
2. Keep the downloaded archive outside Git.
3. Run:

    ./aurora egg acquire --archive /path/to/Egg_archive.zip

4. The default prepared location is `data/egg/local`.
5. The tool validates ZIP integrity, locates the Eclipse Egg case, verifies the
   required deck/include files, hashes them, and writes local provenance.
6. Re-check at any time with:

    ./aurora egg verify

The acquisition tool deliberately does not silently scrape or download a
possibly changed third-party archive. Acquisition provenance is explicit.

## Required Eclipse case

The prepared case must contain one `Egg_Model_ECL.DATA` plus the required
permeability, porosity, and schedule include files declared by the acquisition
tool.

## Failure semantics

Missing archive, corrupt ZIP, ambiguous case layout, missing required files, or
an existing destination produces an actionable non-zero failure. Existing local
data is never silently overwritten.

## Storage boundary

The benchmark remains an external dependency. Generated `EGRID`, `INIT`,
`SMSPEC`, `UNSMRY`, `UNRST`, logs, and bulk prepared cases belong in ignored
local/run storage unless a small, explicitly reviewed evidence artifact is
selected for the repository.
