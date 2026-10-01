from pathlib import Path
import sys

sys.path.insert(0, str(Path("src").resolve()))

from aurora.simulation.opm import inspect_reference_outputs


def test_required_reference_outputs_detected(tmp_path):
    for suffix in [".EGRID", ".INIT", ".SMSPEC", ".UNSMRY", ".UNRST"]:
        (tmp_path / f"EGG_MODEL_ECL{suffix}").write_bytes(b"x")

    result = inspect_reference_outputs(tmp_path)

    assert result["complete"] is True
    assert result["missing"] == []


def test_missing_reference_output_is_explicit(tmp_path):
    (tmp_path / "EGG_MODEL_ECL.SMSPEC").write_bytes(b"x")

    result = inspect_reference_outputs(tmp_path)

    assert result["complete"] is False
    assert ".UNSMRY" in result["missing"]
