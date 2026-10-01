from pathlib import Path


def test_controller_cannot_directly_apply_proposed_action():
    text = Path("src/aurora/closed_loop.py").read_text()

    assert "environment.apply_action(applied)" in text
    assert "environment.apply_action(proposed)" not in text


def test_runtime_docs_do_not_claim_opm_ground_truth():
    text = (
        Path("docs/simulation/OPM_REFERENCE_RUN.md")
        .read_text()
        .lower()
    )

    assert "numerical reference" in text
    assert "ground truth" in text
    assert (
        "not" in text
        or "does not" in text
    )


def test_control_interval_remains_unresolved():
    text = Path(
        "configs/experiments/SMOKE_CLOSED_LOOP.json"
    ).read_text()

    assert "UNRESOLVED" in text
