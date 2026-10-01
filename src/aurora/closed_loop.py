from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict

from aurora.contracts import (
    AppliedAction,
    Observation,
    ProposedAction,
    SafetyDecision,
)
from aurora.simulation.toy import DeterministicToyEnvironment
from aurora.telemetry import JsonlTelemetry


class FixedSmokeController:
    """Deterministic integration controller, not the final control policy."""

    def propose_action(self, observation: Observation) -> ProposedAction:
        value = 79.5 if observation.step % 2 == 0 else 75.0

        return ProposedAction(
            step=observation.step,
            well_id="INJECT1",
            well_role="INJECTOR",
            target_kind="well_rate_target",
            target_value=value,
            unit="m3/day",
        )


class StructuralSafetyFilter:
    """MVP authority boundary.

    This checks structural validity only. It intentionally does NOT invent
    unresolved reservoir safety thresholds or claim physical safety.
    """

    def evaluate(
        self,
        observation: Observation,
        proposed: ProposedAction,
    ) -> tuple[SafetyDecision, AppliedAction]:
        if proposed.target_value < 0:
            raise ValueError(
                "SAFETY_INPUT_INSUFFICIENT: canonical target magnitude "
                "must be nonnegative"
            )

        decision = SafetyDecision(
            disposition="AUTHORIZED_STRUCTURALLY",
            intervened=False,
            reason=(
                "MVP structural authorization only; numerical reservoir "
                "safety constraints remain governed by the constraint registry."
            ),
        )

        applied = AppliedAction(
            step=proposed.step,
            well_id=proposed.well_id,
            well_role=proposed.well_role,
            target_kind=proposed.target_kind,
            target_value=proposed.target_value,
            unit=proposed.unit,
        )

        return decision, applied


def _run_id(config: Dict[str, Any]) -> str:
    encoded = json.dumps(config, sort_keys=True).encode()
    return "smoke-" + hashlib.sha256(encoded).hexdigest()[:12]


def run_smoke(
    *,
    root: Path,
    output_dir: Path,
    steps: int,
    seed: int,
) -> Dict[str, Any]:
    if steps <= 0:
        raise ValueError("steps must be positive")

    configuration = {
        "environment": "DeterministicToyEnvironment",
        "controller": "FixedSmokeController",
        "safety": "StructuralSafetyFilter",
        "steps": steps,
        "seed": seed,
        "control_interval": {
            "status": "UNRESOLVED_FOR_RESERVOIR_SYSTEM",
            "toy_step_unit": "integration_step",
        },
    }

    run_id = _run_id(configuration)
    output_dir.mkdir(parents=True, exist_ok=True)
    telemetry_path = output_dir / "telemetry.jsonl"

    if telemetry_path.exists():
        telemetry_path.unlink()

    environment = DeterministicToyEnvironment(seed=seed)
    controller = FixedSmokeController()
    safety = StructuralSafetyFilter()

    telemetry = JsonlTelemetry(
        telemetry_path,
        run_id=run_id,
        root=root,
        seed=seed,
        configuration=configuration,
        reference_id="TOY-INTEGRATION-NOT-RESERVOIR-PHYSICS",
    )

    for _ in range(steps):
        observation = environment.read_state()
        proposed = controller.propose_action(observation)
        safety_decision, applied = safety.evaluate(
            observation,
            proposed,
        )

        # The only simulator-bound object is applied_action.
        environment.apply_action(applied)
        outcome = environment.advance()

        telemetry.record(
            {
                "event_type": "control_step",
                "step": observation.step,
                "observation": observation.to_dict(),
                "proposed_action": proposed.to_dict(),
                "safety_decision": safety_decision.to_dict(),
                "applied_action": applied.to_dict(),
                "simulator_outcome": outcome.to_dict(),
                "failure": None,
            }
        )

    return {
        "status": "PASS",
        "run_id": run_id,
        "steps": steps,
        "telemetry": str(telemetry_path),
    }
