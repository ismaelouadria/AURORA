from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validation/validate_interface_constraints.py"

spec = importlib.util.spec_from_file_location("validate_interface_constraints", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_canonical_interface_constraint_registries_pass():
    module.validate()

def test_interface_distinguishes_proposed_and_applied_actions():
    text = (ROOT / "configs/interfaces/CLOSED_LOOP_SEMANTICS.yaml").read_text()
    assert "proposed_action:" in text
    assert "applied_action:" in text
    assert "required_when_actions_differ: true" in text

def test_control_interval_is_not_silently_frozen():
    text = (ROOT / "configs/interfaces/CLOSED_LOOP_SEMANTICS.yaml").read_text()
    assert "control_interval:" in text
    assert "status: UNRESOLVED" in text
    assert "value: null" in text

def test_constraint_registry_has_no_frozen_numeric_operational_bounds():
    text = (ROOT / "configs/safety/CONSTRAINT_REGISTRY.yaml").read_text()
    assert "lower: null" in text
    assert "upper: null" in text
    assert "historical_range_to_physical_limit_without_justification" in text

def test_margin_semantics_are_explicit():
    text = (ROOT / "configs/safety/CONSTRAINT_REGISTRY.yaml").read_text()
    assert "positive_safe_zero_boundary_negative_violation" in text
    assert "near_miss:" in text

def test_egg_baseline_evidence_boundary():
    import yaml

    root = Path(__file__).resolve().parents[2]

    for rel in (
        "configs/interfaces/CLOSED_LOOP_SEMANTICS.yaml",
        "configs/safety/CONSTRAINT_REGISTRY.yaml",
    ):
        registry = yaml.safe_load((root / rel).read_text())
        evidence = registry["egg_benchmark_evidence"]

        assert evidence["evidence_class"] == "BENCHMARK_BASELINE"

        assert evidence["observed_topology"]["injector_count"] == 8
        assert evidence["observed_topology"]["producer_count"] == 4

        schedule = evidence["observed_schedule"]
        assert schedule["timestep_count"] == 120
        assert schedule["timestep_length_days"] == 30.0

        injectors = evidence["observed_controls"]["injectors"]
        assert injectors["keyword"] == "WCONINJE"
        assert injectors["control_mode"] == "RATE"
        assert injectors["baseline_rate_raw"] == 79.5
        assert injectors["additional_raw_value"] == 420.0
        assert injectors["additional_raw_value_semantics"] == "UNRESOLVED"

        producers = evidence["observed_controls"]["producers"]
        assert producers["keyword"] == "WCONPROD"
        assert producers["control_mode"] == "BHP"
        assert producers["baseline_bhp_raw"] == 395.0

        boundary = " ".join(evidence["claim_boundary"]).lower()

        assert "not an admissible action bound" in boundary
        assert "not a physical limit" in boundary
        assert "not an encoded safety constraint" in boundary
        assert "does not by itself freeze" in boundary
        assert "420" in boundary
        assert "unresolved" in boundary
