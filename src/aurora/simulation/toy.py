from __future__ import annotations

from dataclasses import dataclass

from aurora.contracts import AppliedAction, Observation, SimulatorOutcome


@dataclass
class DeterministicToyEnvironment:
    """Fast integration environment, not a reservoir-physics claim."""

    seed: int = 7
    step_index: int = 0
    simulation_time: float = 0.0
    applied_target: float = 79.5

    def read_state(self) -> Observation:
        return Observation(
            step=self.step_index,
            simulation_time=self.simulation_time,
            quantities={
                "toy_state": float(self.applied_target),
            },
        )

    def apply_action(self, action: AppliedAction) -> None:
        if action.well_id != "INJECT1":
            raise ValueError("APPLIED_ACTION_INVALID: unsupported toy well")
        if action.target_kind != "well_rate_target":
            raise ValueError("APPLIED_ACTION_INVALID: unsupported target kind")
        self.applied_target = float(action.target_value)

    def advance(self) -> SimulatorOutcome:
        self.step_index += 1
        self.simulation_time += 1.0

        return SimulatorOutcome(
            step=self.step_index,
            simulation_time=self.simulation_time,
            status="OK",
            quantities={
                "toy_state": float(self.applied_target),
            },
        )
