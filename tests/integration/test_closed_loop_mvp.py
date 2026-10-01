import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path("src").resolve()))

from aurora.closed_loop import run_smoke


def test_closed_loop_repeats_and_preserves_authority_boundary(tmp_path):
    result = run_smoke(
        root=Path.cwd(),
        output_dir=tmp_path,
        steps=4,
        seed=7,
    )

    assert result["status"] == "PASS"

    records = [
        json.loads(line)
        for line in (tmp_path / "telemetry.jsonl").read_text().splitlines()
    ]

    assert len(records) == 4

    for index, record in enumerate(records):
        assert record["step"] == index
        assert "observation" in record
        assert "proposed_action" in record
        assert "safety_decision" in record
        assert "applied_action" in record
        assert "simulator_outcome" in record

        assert (
            record["proposed_action"]["target_value"]
            == record["applied_action"]["target_value"]
        )

        assert (
            record["safety_decision"]["disposition"]
            == "AUTHORIZED_STRUCTURALLY"
        )


def test_smoke_is_deterministic_in_control_values(tmp_path):
    first = tmp_path / "a"
    second = tmp_path / "b"

    run_smoke(
        root=Path.cwd(),
        output_dir=first,
        steps=4,
        seed=7,
    )
    run_smoke(
        root=Path.cwd(),
        output_dir=second,
        steps=4,
        seed=7,
    )

    def values(path):
        return [
            json.loads(line)["applied_action"]["target_value"]
            for line in (path / "telemetry.jsonl").read_text().splitlines()
        ]

    assert values(first) == values(second)
