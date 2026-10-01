#!/usr/bin/env python3

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]

ARCH = ROOT / "configs/architecture/CLOSED_LOOP_ARCHITECTURE.yaml"
FAIL = ROOT / "configs/architecture/FAILURE_SEMANTICS.yaml"

ERRORS = []


def require(text, phrase, label):
    if phrase not in text:
        ERRORS.append(f"{label}: missing required invariant: {phrase}")


def ids(text, prefix):
    return re.findall(rf"\b({re.escape(prefix)}-[A-Z]+-\d{{3}}|{re.escape(prefix)}-\d{{3}})\b", text)


def simple_ids(text, prefix):
    return re.findall(rf"\b({re.escape(prefix)}-\d{{3}})\b", text)


def unique(values, label):
    dupes = sorted({v for v in values if values.count(v) > 1})
    if dupes:
        ERRORS.append(f"{label}: duplicate IDs: {', '.join(dupes)}")


def validate():
    if not ARCH.exists():
        ERRORS.append(f"missing {ARCH.relative_to(ROOT)}")
        return
    if not FAIL.exists():
        ERRORS.append(f"missing {FAIL.relative_to(ROOT)}")
        return

    arch = ARCH.read_text(encoding="utf-8")
    fail = FAIL.read_text(encoding="utf-8")

    invariant_ids = simple_ids(arch, "ARCH-INV")
    unique(invariant_ids, "architecture")
    if len(set(invariant_ids)) < 12:
        ERRORS.append("architecture: expected at least 12 explicit architecture invariants")

    failure_ids = re.findall(r"(?m)^\s*-\s+id:\s+(FAIL-[A-Z0-9-]+)\s*$", fail)
    unique(failure_ids, "failure registry")
    if len(set(failure_ids)) < 10:
        ERRORS.append("failure registry: expected at least 10 explicit failure classes")

    for component in (
        "simulator_adapter",
        "observation_adapter",
        "controller",
        "safety_filter",
        "action_adapter",
        "telemetry",
        "orchestrator",
    ):
        require(arch, component, "architecture")

    for contract in (
        "simulator_state:",
        "observation:",
        "proposed_action:",
        "safety_decision:",
        "applied_action:",
        "simulator_outcome:",
        "failure_event:",
    ):
        require(arch, contract, "architecture")

    for dimension in (
        "interface_requirements:",
        "timing:",
        "configuration:",
        "ownership:",
        "errors:",
        "compatibility:",
    ):
        require(arch, dimension, "architecture interface compatibility")

    for component in (
        "simulator_adapter:",
        "observation_adapter:",
        "controller:",
        "safety_filter:",
        "action_adapter:",
        "telemetry:",
    ):
        require(arch, component, "architecture interface compatibility")

    for phrase in (
        "The controller may propose an action but may not directly apply an action to the simulator.",
        "Every simulator-bound control passes through the safety authority boundary.",
        "proposed_action and applied_action are distinct records",
        "The simulator adapter receives applied_action, never raw controller output.",
        "Telemetry observes decisions and outcomes but has no control authority.",
        "Simulator state availability does not imply controller observability.",
        "Historical or benchmark values do not become physical safety limits",
        "The control interval remains unresolved",
    ):
        require(arch, phrase, "architecture")

    require(arch, "value: null", "architecture")
    require(arch, "status: UNRESOLVED", "architecture")

    # Architecture must not freeze the known Egg benchmark numbers as control
    # or safety limits. They belong in evidence registries, not architecture.
    for forbidden in ("79.5", "395.0", "420.0"):
        if forbidden in arch:
            ERRORS.append(
                f"architecture: benchmark numeric value {forbidden} leaked into architecture contract"
            )

    for disposition in (
        "ACCEPT",
        "MODIFY",
        "REJECT",
        "INSUFFICIENT_EVIDENCE",
        "NUMERICAL_FAILURE",
    ):
        require(arch, disposition, "architecture")

    for fallback in (
        "HOLD_NO_NEW_ACTION",
        "REJECT_PROPOSAL",
        "TERMINATE_RUN",
        "RETRY_SAME_OPERATION",
        "CONTINUE_WITH_WARNING",
    ):
        require(fail, fallback, "failure registry")

    for phrase in (
        "No fallback may bypass the safety authority boundary.",
        "No fallback may invent reservoir measurements, limits, or control targets.",
        "replace missing required observations with zero",
        "reuse stale observations without an explicit supported stale-data policy",
        "invent action bounds",
        "invent pressure limits",
        "reinterpret benchmark controls as safe fallback controls",
        "convert simulator failure into a successful experiment step",
    ):
        require(fail, phrase, "failure registry")

    required_failure_names = (
        "REQUIRED_OBSERVATION_MISSING",
        "OBSERVATION_NONFINITE",
        "OBSERVATION_OUT_OF_DECLARED_ENVELOPE",
        "OBSERVATION_SEMANTICS_UNRESOLVED",
        "CONTROLLER_OUTPUT_MALFORMED",
        "CONTROLLER_NUMERICAL_FAILURE",
        "SAFETY_INPUT_INSUFFICIENT",
        "SAFETY_OPTIMIZATION_INFEASIBLE",
        "SAFETY_NUMERICAL_FAILURE",
        "APPLIED_ACTION_INVALID",
        "SIMULATOR_CONTROL_REJECTED",
        "SIMULATOR_NUMERICAL_FAILURE",
        "SIMULATOR_OUTPUT_INCOMPLETE",
        "REQUIRED_PROVENANCE_WRITE_FAILED",
        "STEP_IDENTITY_MISMATCH",
        "UNSUPPORTED_SCHEMA_VERSION",
    )
    for name in required_failure_names:
        require(fail, name, "failure registry")

    require(fail, "robustness_traceability:", "failure registry")
    require(fail, "ROB-OBS-OUT-OF-ENVELOPE", "failure registry")
    require(fail, "ROB-SAFETY-INFEASIBLE", "failure registry")
    require(fail, "ROB-TELEMETRY-WRITE", "failure registry")

    if ERRORS:
        print("ARCHITECTURE REGISTRY: FAIL")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    print("ARCHITECTURE REGISTRY: PASS")
    print(f"Architecture invariants: {len(set(invariant_ids))}")
    print(f"Failure classes: {len(set(failure_ids))}")
    print("Authority path: controller -> safety -> applied_action -> simulator")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
