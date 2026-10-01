from pathlib import Path
import importlib.util


SCRIPT = Path("scripts/validation/validate_domain_rules.py")

spec = importlib.util.spec_from_file_location("validate_domain_rules", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def registry_text() -> str:
    return Path(
        "configs/validation/DOMAIN_INTERPRETATION_RULES.yaml"
    ).read_text()


def test_canonical_registry_passes():
    assert module.validate_text(registry_text(), Path.cwd()) == []


def test_duplicate_rule_id_is_rejected():
    text = registry_text()
    block_start = text.index("  - id: DVR-001")
    block_end = text.index("  - id: DVR-002")
    first_rule = text[block_start:block_end]

    errors = module.validate_text(
        text + "\n" + first_rule,
        Path.cwd(),
    )

    assert any("duplicate rule IDs" in error for error in errors)


def test_missing_evidence_path_is_rejected():
    text = registry_text().replace(
        "docs/validation/VALIDATION_SPECIFICATION.md",
        "docs/validation/DOES_NOT_EXIST.md",
        1,
    )

    errors = module.validate_text(text, Path.cwd())

    assert any("missing repository evidence path" in error for error in errors)


def test_unsupported_status_is_rejected():
    text = registry_text().replace(
        "status: SOURCE_BACKED",
        "status: CERTAIN_FOREVER",
        1,
    )

    errors = module.validate_text(text, Path.cwd())

    assert any("unsupported status" in error for error in errors)


def test_physical_safety_overclaim_is_rejected():
    text = registry_text().replace(
        "Passing these rules establishes only the checks explicitly represented here.",
        "Passing these rules guarantees physical safety.",
        1,
    )

    errors = module.validate_text(text, Path.cwd())

    assert any("prohibited overclaim pattern" in error for error in errors)
