# AURORA Component

Implementation for this AURORA component has not yet been populated.

When development begins, document the component's responsibility, inputs, outputs, configuration, dependencies, verification strategy, and integration contract before allowing this directory to become a collection of unexplained code.

# Experiment platform (`src/experiments`)

Owner: Mahdi · Milestones 0.2, 0.3, 1.5

Every AURORA result must be traceable to the code, config, seed and geology that produced it.
This package guarantees that for any experiment that runs through it.

## Quick start

```bash
# run the toy batch (20 runs: 4 margins x 5 seeds), 4 processes
PYTHONPATH=src python -m experiments batch experiments/configs/toy_batch.yaml --workers 4

# list every run, or only failed / crashed ones
PYTHONPATH=src python -m experiments index
PYTHONPATH=src python -m experiments failures

# copy a run's manifest + summary into experiments/ so it can be committed as evidence
PYTHONPATH=src python -m experiments export <run_id>
```

Re-running a batch skips combinations that already succeeded **at the same commit**
(`--no-resume` to force). After any code change, everything re-runs.

## What a run leaves behind

Bulk output goes to `artifacts/runs/` (git-ignored; override with `--root`):

```
artifacts/runs/manifests/<run_id>.json      always, including failed runs
artifacts/runs/results/<run_id>/steps.parquet
artifacts/runs/results/<run_id>/summary.parquet
artifacts/runs/results/<run_id>/error.txt   failed runs only (full traceback)
```

`export` copies only the manifest and one-row summary into `experiments/manifests/` and
`experiments/results/<run_id>/`, which are version-controlled. It refuses runs made from a dirty
working tree, because their commit does not identify the code that produced them.

Run ID: `<UTC time>-<7-char commit>-<8 hex>`, e.g. `20261005T143012Z-a1b2c3d-9f3e21c4`.
Sorts by time; shows the commit at a glance; IDs are reserved exclusively, so they never collide.

The manifest records: experiment, entrypoint, config, config hash, seed, geology ID, split,
git commit / dirty flag / branch, status, timestamps, duration, error, output paths, parent run IDs
(for ROM/OPM pairs later) and package versions.

## Writing an experiment

```python
from experiments.runner import ExperimentOutput, RunContext

def run(ctx: RunContext) -> ExperimentOutput:
    # use ctx.rng for ALL randomness; ctx.config holds the parameters
    steps = ...      # DataFrame with "step", "time_days" + unit-suffixed columns
    summary = {...}  # one row: "npv_usd", "violation_count", ...
    return ExperimentOutput(steps=steps, summary=summary)
```

Point a YAML spec at it with `entrypoint: package.module:run` (see `experiments/configs/toy_batch.yaml`).

## Rules the platform enforces

| Rule | How |
| --- | --- |
| Units in every column name (NFR4) | Columns must end in an approved suffix (`_bar`, `_m3_per_day`, `_usd`, `_days`, `_count`, `_flag`, ...) or the write fails |
| Failed runs are never lost (NFR3) | Exceptions mark the run `failed`, keep manifest + traceback, batch continues |
| Manifest written before work starts | A hard crash still leaves a `running` manifest as evidence |
| Config can't drift from its hash | Manifest validation recomputes the hash |
| Valid seed and split | Checked before the experiment function is called |
| Same seed, same result | Python, NumPy (and PyTorch if installed) are seeded; tested |
| Resume never reuses stale results | Resume key includes the git commit |
| Evidence is traceable | `export` refuses runs from a dirty tree |

## Not here yet (later milestones)

- Geology split manifest + guard that blocks test geology from calibration (3.1)
- ROM/OPM pairing via `parent_run_ids` (3.0)
- Paired statistics and bootstrap CIs (2.3, 3.8)