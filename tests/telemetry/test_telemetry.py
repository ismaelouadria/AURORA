import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path("src").resolve()))

from aurora.telemetry import JsonlTelemetry


def test_telemetry_records_required_provenance(tmp_path):
    path = tmp_path / "telemetry.jsonl"

    telemetry = JsonlTelemetry(
        path,
        run_id="run-1",
        root=Path.cwd(),
        seed=17,
        configuration={"mode": "test"},
        reference_id="fixture",
    )

    telemetry.record(
        {
            "event_type": "control_step",
            "step": 0,
            "observation": {},
            "proposed_action": {},
            "safety_decision": {},
            "applied_action": {},
            "simulator_outcome": {},
            "failure": None,
        }
    )

    record = json.loads(path.read_text())

    assert record["run_id"] == "run-1"
    assert record["seed"] == 17
    assert record["configuration"] == {"mode": "test"}
    assert record["reference_id"] == "fixture"
    assert record["commit"]


def test_required_telemetry_failure_is_visible(tmp_path):
    directory = tmp_path / "directory"
    directory.mkdir()

    telemetry = JsonlTelemetry(
        directory,
        run_id="run-1",
        root=Path.cwd(),
        seed=1,
        configuration={},
        reference_id="fixture",
    )

    try:
        telemetry.record({"event_type": "control_step"})
    except RuntimeError as exc:
        assert "REQUIRED_PROVENANCE_WRITE_FAILED" in str(exc)
    else:
        raise AssertionError("telemetry write failure was hidden")
