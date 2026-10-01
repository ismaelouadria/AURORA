#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
INTERFACE = ROOT / "configs/interfaces/CLOSED_LOOP_SEMANTICS.yaml"
CONSTRAINTS = ROOT / "configs/safety/CONSTRAINT_REGISTRY.yaml"

ALLOWED_STATUS = {
    "SOURCE_BACKED",
    "EXPERIMENTALLY_SUPPORTED",
    "EXPERT_REVIEWED",
    "PROVISIONAL",
    "UNRESOLVED",
}

def fail(message):
    raise ValueError(message)

def read(path):
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")

def ids(text, prefix):
    return re.findall(rf"^\s*-\s+id:\s+({prefix}-\d{{3}})\s*$", text, re.M)

def validate():
    interface = read(INTERFACE)
    constraints = read(CONSTRAINTS)

    obs = ids(interface, "OBS")
    acts = ids(interface, "ACT")
    ctrs = ids(constraints, "CTR")

    if len(obs) != len(set(obs)) or not obs:
        fail("observation IDs must exist and be unique")
    if len(acts) != len(set(acts)) or not acts:
        fail("action IDs must exist and be unique")
    if len(ctrs) != len(set(ctrs)) or not ctrs:
        fail("constraint IDs must exist and be unique")

    required_interface_phrases = [
        "proposed_action:",
        "applied_action:",
        "control_interval:",
        "well_id:",
        "well_role:",
        "realization_id:",
        "control_step:",
        "missing_policy:",
        "sign_convention:",
        "simulator_to_controller:",
        "safety_to_simulator:",
    ]
    for phrase in required_interface_phrases:
        if phrase not in interface:
            fail(f"interface registry missing semantic field: {phrase}")

    required_constraint_phrases = [
        "constraint_classes:",
        "threshold_requirements:",
        "prohibited_promotions:",
        "margin:",
        "violation:",
        "near_miss:",
        "claim_boundary:",
    ]
    for phrase in required_constraint_phrases:
        if phrase not in constraints:
            fail(f"constraint registry missing semantic field: {phrase}")

    if "historical_range_to_physical_limit_without_justification" not in constraints:
        fail("historical-range promotion guard missing")

    if "positive_safe_zero_boundary_negative_violation" not in constraints:
        fail("constraint-margin sign convention missing")

    numeric_limit_patterns = [
        r"lower:\s*[+-]?\d+(?:\.\d+)?",
        r"upper:\s*[+-]?\d+(?:\.\d+)?",
        r"threshold:\s*[+-]?\d+(?:\.\d+)?",
    ]
    combined = interface + "\n" + constraints
    for pattern in numeric_limit_patterns:
        if re.search(pattern, combined):
            fail("unsupported numerical operational limit appears frozen")

    statuses = set(re.findall(r"\b(?:SOURCE_BACKED|EXPERIMENTALLY_SUPPORTED|EXPERT_REVIEWED|PROVISIONAL|UNRESOLVED)\b", combined))
    if not statuses.issubset(ALLOWED_STATUS):
        fail("unsupported status found")

    if "well_bottom_hole_pressure" not in interface or "well_bottom_hole_pressure" not in constraints:
        fail("pressure quantity is not cross-linked between interface and constraint registries")

    if "well_rate_target" not in interface or "well_rate_target" not in constraints:
        fail("action quantity is not cross-linked between interface and constraint registries")

    # Egg benchmark evidence must remain explicitly separated from final
    # interface, action-bound, and safety-limit decisions.
    for label, registry_text in (
        ("interface", interface),
        ("constraint", constraints),
    ):
        required_evidence = [
            "evidence_class: BENCHMARK_BASELINE",
            "injector_count: 8",
            "producer_count: 4",
            "timestep_count: 120",
            "timestep_length_days: 30.0",
            "keyword: WCONINJE",
            "control_mode: RATE",
            "baseline_rate_raw: 79.5",
            "additional_raw_value: 420.0",
            "additional_raw_value_semantics: UNRESOLVED",
            "keyword: WCONPROD",
            "control_mode: BHP",
            "baseline_bhp_raw: 395.0",
            "not an admissible action bound",
            "not a physical limit",
            "not an encoded safety constraint",
            "does not by itself freeze",
        ]
        for phrase in required_evidence:
            if phrase not in registry_text:
                fail(f"{label} registry missing Egg evidence boundary: {phrase}")

    print("INTERFACE / CONSTRAINT REGISTRY: PASS")
    print(f"Observation candidates: {len(obs)}")
    print(f"Action candidates: {len(acts)}")
    print(f"Constraint candidates: {len(ctrs)}")

if __name__ == "__main__":
    try:
        validate()
    except ValueError as exc:
        print(f"INTERFACE / CONSTRAINT REGISTRY: FAIL — {exc}", file=sys.stderr)
        sys.exit(1)
