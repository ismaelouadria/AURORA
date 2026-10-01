#!/usr/bin/env python3
"""Validate the AURORA domain-interpretation rule registry.

This validator intentionally uses only the Python standard library. It validates
the controlled structure and invariants of the registry without pretending to
validate petroleum-engineering truth.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


DEFAULT_REGISTRY = Path("configs/validation/DOMAIN_INTERPRETATION_RULES.yaml")

REQUIRED_TOP_LEVEL = {
    "schema_version",
    "purpose",
    "claim_boundary",
    "allowed_statuses",
    "allowed_result_states",
    "rules",
}

REQUIRED_RULE_FIELDS = {
    "id",
    "name",
    "category",
    "automation",
    "status",
    "applies_to",
    "check",
    "failure_state",
    "rationale",
    "evidence",
    "limitation",
}

ALLOWED_AUTOMATION = {"deterministic", "policy"}
ALLOWED_STATUSES = {
    "SOURCE_BACKED",
    "EXPERIMENTALLY_SUPPORTED",
    "EXPERT_REVIEWED",
    "PROVISIONAL",
    "UNRESOLVED",
}
ALLOWED_FAILURE_STATES = {
    "VALID_FOR_SCOPE",
    "VALID_WITH_WARNING",
    "INSUFFICIENT_EVIDENCE",
    "INVALID_DATA",
    "INVALID_EXPERIMENT",
    "OUTSIDE_ENVELOPE",
    "NUMERICAL_FAILURE",
    "DOMAIN_REVIEW_REQUIRED",
}

PROHIBITED_CLAIM_PATTERNS = [
    re.compile(r"\bguarantees?\s+(?:physical\s+)?safety\b", re.I),
    re.compile(r"\bopm\b.*\bground truth\b", re.I),
    re.compile(r"\bhistorical range\b.*\bphysical (?:safety )?limit\b", re.I),
]


def _top_level_keys(text: str) -> set[str]:
    keys = set()
    for line in text.splitlines():
        if not line or line.startswith((" ", "\t", "#", "-")):
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):", line)
        if match:
            keys.add(match.group(1))
    return keys


def _parse_rules(text: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line == "rules:")
    except StopIteration:
        return []

    rules: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    in_evidence = False

    for line in lines[start + 1 :]:
        id_match = re.match(r"^  - id:\s*(\S+)\s*$", line)
        if id_match:
            if current is not None:
                rules.append(current)
            current = {"id": id_match.group(1)}
            in_evidence = False
            continue

        if current is None:
            continue

        field_match = re.match(r"^    ([A-Za-z_][A-Za-z0-9_]*):(?:\s*(.*))?$", line)
        if field_match:
            key, value = field_match.groups()
            current[key] = (value or "").strip()
            in_evidence = key == "evidence"
            if in_evidence:
                current[key] = []
            continue

        if in_evidence:
            evidence_match = re.match(r"^      -\s+(.+?)\s*$", line)
            if evidence_match:
                evidence = current.setdefault("evidence", [])
                assert isinstance(evidence, list)
                evidence.append(evidence_match.group(1))

    if current is not None:
        rules.append(current)

    return rules


def validate_text(text: str, repo_root: Path) -> list[str]:
    errors: list[str] = []

    missing_top = REQUIRED_TOP_LEVEL - _top_level_keys(text)
    if missing_top:
        errors.append(
            "missing top-level fields: " + ", ".join(sorted(missing_top))
        )

    rules = _parse_rules(text)
    if not rules:
        errors.append("registry contains no rules")
        return errors

    ids: list[str] = []

    for index, rule in enumerate(rules, start=1):
        rule_id = str(rule.get("id", f"<rule-{index}>"))
        ids.append(rule_id)

        missing = REQUIRED_RULE_FIELDS - set(rule)
        if missing:
            errors.append(
                f"{rule_id}: missing fields: {', '.join(sorted(missing))}"
            )
            continue

        if not re.fullmatch(r"DVR-\d{3}", rule_id):
            errors.append(f"{rule_id}: invalid rule ID format")

        automation = str(rule["automation"])
        if automation not in ALLOWED_AUTOMATION:
            errors.append(
                f"{rule_id}: unsupported automation value {automation!r}"
            )

        status = str(rule["status"])
        if status not in ALLOWED_STATUSES:
            errors.append(f"{rule_id}: unsupported status {status!r}")

        failure_state = str(rule["failure_state"])
        if failure_state not in ALLOWED_FAILURE_STATES:
            errors.append(
                f"{rule_id}: unsupported failure_state {failure_state!r}"
            )

        evidence = rule["evidence"]
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{rule_id}: evidence must contain at least one entry")
        else:
            for source in evidence:
                if source.startswith(("docs/", "references/")):
                    if not (repo_root / source).exists():
                        errors.append(
                            f"{rule_id}: missing repository evidence path {source}"
                        )

        limitation = str(rule["limitation"]).strip()
        if not limitation:
            errors.append(f"{rule_id}: limitation must not be empty")

    duplicates = sorted({x for x in ids if ids.count(x) > 1})
    if duplicates:
        errors.append("duplicate rule IDs: " + ", ".join(duplicates))

    for pattern in PROHIBITED_CLAIM_PATTERNS:
        if pattern.search(text):
            errors.append(
                f"registry contains prohibited overclaim pattern: {pattern.pattern}"
            )

    return errors


def validate_file(path: Path) -> list[str]:
    return validate_text(path.read_text(), Path.cwd())


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT_REGISTRY

    if not path.exists():
        print(f"FAIL: registry not found: {path}")
        return 2

    errors = validate_file(path)

    if errors:
        print("DOMAIN RULE REGISTRY: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    rules = _parse_rules(path.read_text())
    deterministic = sum(r.get("automation") == "deterministic" for r in rules)
    policy = sum(r.get("automation") == "policy" for r in rules)

    print("DOMAIN RULE REGISTRY: PASS")
    print(f"Rules: {len(rules)}")
    print(f"Deterministic rules: {deterministic}")
    print(f"Policy rules: {policy}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
