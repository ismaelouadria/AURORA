import json
from pathlib import Path


def test_output_contract_preserves_semantic_boundaries():
    contract = json.loads(
        Path(
            "configs/simulation/OPM_OUTPUT_CONTRACT.json"
        ).read_text()
    )

    assert contract["status"] == "PROVISIONAL"
    assert (
        contract["missing_policy"]
        == "fail_explicitly_for_required_configured_output"
    )

    families = contract["candidate_summary_families"]
    assert families

    for family in families:
        assert (
            family["controller_observation_authority"]
            == "UNRESOLVED"
        )
