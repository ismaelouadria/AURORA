from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Observation:
    step: int
    simulation_time: float
    quantities: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProposedAction:
    step: int
    well_id: str
    well_role: str
    target_kind: str
    target_value: float
    unit: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SafetyDecision:
    disposition: str
    intervened: bool
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AppliedAction:
    step: int
    well_id: str
    well_role: str
    target_kind: str
    target_value: float
    unit: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SimulatorOutcome:
    step: int
    simulation_time: float
    status: str
    quantities: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
