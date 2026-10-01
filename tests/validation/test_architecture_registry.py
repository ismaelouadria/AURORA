import re
from pathlib import Path
import importlib.util
import shutil

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validation/validate_architecture.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_architecture", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_canonical_architecture_passes():
    validator = load_validator()
    validator.ERRORS.clear()
    assert validator.validate() == 0


def test_controller_cannot_bypass_safety():
    text = (ROOT / "configs/architecture/CLOSED_LOOP_ARCHITECTURE.yaml").read_text()
    assert "may not directly apply an action to the simulator" in text
    assert "Every simulator-bound control passes through the safety authority boundary." in text
    assert "The simulator adapter receives applied_action, never raw controller output." in text


def test_proposed_and_applied_actions_are_distinct():
    text = (ROOT / "configs/architecture/CLOSED_LOOP_ARCHITECTURE.yaml").read_text()
    assert "proposed_action and applied_action are distinct records" in text
    assert "proposed_action:" in text
    assert "applied_action:" in text


def test_control_interval_remains_unresolved():
    text = (ROOT / "configs/architecture/CLOSED_LOOP_ARCHITECTURE.yaml").read_text()
    section = text.split("control_interval:", 1)[1].split("components:", 1)[0]
    assert "value: null" in section
    assert "unit: null" in section
    assert "status: UNRESOLVED" in section


def test_benchmark_numbers_do_not_leak_into_architecture():
    text = (ROOT / "configs/architecture/CLOSED_LOOP_ARCHITECTURE.yaml").read_text()
    for forbidden in ("79.5", "395.0", "420.0"):
        assert forbidden not in text


def test_failure_policy_does_not_invent_defaults():
    text = (ROOT / "configs/architecture/FAILURE_SEMANTICS.yaml").read_text()
    assert "replace missing required observations with zero" in text
    assert "invent action bounds" in text
    assert "invent pressure limits" in text
    assert "reinterpret benchmark controls as safe fallback controls" in text


def test_safety_rejection_is_not_physical_truth():
    text = (ROOT / "configs/architecture/FAILURE_SEMANTICS.yaml").read_text()
    assert "is_failure: false" in text
    assert "does not by itself prove" in text
    assert "physically unsafe" in text


def test_failure_registry_has_unique_ids():
    """Definitions are unique; robustness references resolve to definitions."""
    text = (
        ROOT / "configs/architecture/FAILURE_SEMANTICS.yaml"
    ).read_text()

    definitions = re.findall(
        r"(?m)^\s*-\s+id:\s+(FAIL-[A-Z0-9-]+)\s*$",
        text,
    )

    references = re.findall(
        r"(?m)^\s*failure:\s+(FAIL-[A-Z0-9-]+)\s*$",
        text,
    )

    assert len(definitions) >= 10
    assert len(definitions) == len(set(definitions))
    assert references
    assert set(references) <= set(definitions)

def test_validator_rejects_controller_bypass(tmp_path):
    validator = load_validator()

    arch = tmp_path / "CLOSED_LOOP_ARCHITECTURE.yaml"
    failure = tmp_path / "FAILURE_SEMANTICS.yaml"

    arch_text = (ROOT / "configs/architecture/CLOSED_LOOP_ARCHITECTURE.yaml").read_text()
    arch.write_text(
        arch_text.replace(
            "Every simulator-bound control passes through the safety authority boundary.",
            "Simulator-bound controls may bypass safety.",
        )
    )
    shutil.copy(ROOT / "configs/architecture/FAILURE_SEMANTICS.yaml", failure)

    original_arch = validator.ARCH
    original_fail = validator.FAIL
    validator.ARCH = arch
    validator.FAIL = failure
    validator.ERRORS.clear()

    try:
        assert validator.validate() == 1
    finally:
        validator.ARCH = original_arch
        validator.FAIL = original_fail
        validator.ERRORS.clear()


def test_major_interfaces_declare_required_contract_dimensions():
    text = (ROOT / "configs/architecture/CLOSED_LOOP_ARCHITECTURE.yaml").read_text()
    assert "interface_requirements:" in text
    for dimension in (
        "timing:",
        "configuration:",
        "ownership:",
        "errors:",
        "compatibility:",
    ):
        assert dimension in text


def test_out_of_range_observation_has_explicit_behavior():
    text = (ROOT / "configs/architecture/FAILURE_SEMANTICS.yaml").read_text()
    assert "OBSERVATION_OUT_OF_DECLARED_ENVELOPE" in text
    assert "fallback: HOLD_NO_NEW_ACTION" in text
    assert "does not automatically mean physically unsafe" in text


def test_failure_semantics_are_traceable_to_robustness_scenarios():
    text = (ROOT / "configs/architecture/FAILURE_SEMANTICS.yaml").read_text()
    assert "robustness_traceability:" in text
    assert "ROB-OBS-MISSING" in text
    assert "ROB-OBS-OUT-OF-ENVELOPE" in text
    assert "ROB-CONTROLLER-MALFORMED" in text
    assert "ROB-SAFETY-INFEASIBLE" in text
    assert "ROB-SIM-NUMERICAL" in text
    assert "ROB-TELEMETRY-WRITE" in text


def test_adrs_record_criteria_tradeoffs_and_evidence():
    root = ROOT / "docs/architecture/decisions"
    adrs = sorted(root.glob("ADR-*.md"))
    assert len(adrs) >= 5

    for path in adrs:
        text = path.read_text()
        assert "## Alternatives considered" in text
        assert "## Decision" in text
        assert "## Evaluation criteria" in text
        assert "## Trade-offs" in text
        assert "## Evidence" in text
