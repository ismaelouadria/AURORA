#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def require(relative: str) -> Path:
    path = ROOT / relative
    if not path.is_file():
        raise AssertionError(f"missing required file: {relative}")
    return path


def load_json(relative: str):
    return json.loads(require(relative).read_text())


def main() -> int:
    reference = load_json(
        "configs/simulation/EGG_REFERENCE_RUN.json"
    )
    output = load_json(
        "configs/simulation/OPM_OUTPUT_CONTRACT.json"
    )
    telemetry = load_json(
        "configs/telemetry/STEP_TELEMETRY_SCHEMA.json"
    )
    smoke = load_json(
        "configs/experiments/SMOKE_CLOSED_LOOP.json"
    )

    # Reservoir-reference claim boundary.
    assert reference["simulator"]["physical_ground_truth"] is False

    # OPM extraction remains provisional until later domain/interface
    # decisions freeze final observation membership.
    assert output["status"] == "PROVISIONAL"
    assert (
        output["missing_policy"]
        == "fail_explicitly_for_required_configured_output"
    )
    assert output["invalid_policy"] == "do_not_silently_coerce"

    # Required closed-loop telemetry/provenance.
    required = set(telemetry["required"])

    expected_telemetry = {
        "run_id",
        "commit",
        "seed",
        "reference_id",
        "configuration",
        "event_type",
        "step",
        "observation",
        "proposed_action",
        "safety_decision",
        "applied_action",
        "simulator_outcome",
        "failure",
    }

    missing = expected_telemetry - required
    assert not missing, (
        "telemetry schema missing required fields: "
        + ", ".join(sorted(missing))
    )

    # Toy smoke environment is explicitly an integration proof, not
    # reservoir validation, and must not freeze reservoir cadence.
    assert (
        smoke["purpose"]
        == "software integration proof; not reservoir validation"
    )
    assert (
        smoke["control_interval"]["reservoir_semantics"]
        == "UNRESOLVED"
    )

    # The canonical architecture validator owns architecture-registry
    # semantics. Here we only ensure the runtime implementation respects
    # the already-frozen authority boundary.
    closed_loop = require(
        "src/aurora/closed_loop.py"
    ).read_text()

    assert "environment.apply_action(applied)" in closed_loop
    assert "environment.apply_action(proposed)" not in closed_loop

    assert "controller.propose_action" in closed_loop
    assert "safety.evaluate" in closed_loop
    assert "telemetry.record" in closed_loop

    # Runtime documentation must preserve scientific scope boundaries.
    opm_doc = require(
        "docs/simulation/OPM_REFERENCE_RUN.md"
    ).read_text().lower()

    mvp_doc = require(
        "docs/development/CLOSED_LOOP_MVP.md"
    ).read_text().lower()

    assert "numerical reference" in opm_doc
    assert "not physical ground truth" in opm_doc
    assert "toy environment is not a reservoir model" in mvp_doc

    print("RUNTIME FOUNDATION: PASS")
    print("Reference simulator: OPM Flow")
    print("Reference physical-ground-truth claim: prohibited")
    print("Output contract: PROVISIONAL")
    print("Telemetry proposed/applied distinction: required")
    print("Reservoir control interval: UNRESOLVED")
    print("Safety bypass static check: PASS")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(
            f"RUNTIME FOUNDATION: FAIL — {exc}",
            file=sys.stderr,
        )
        raise
