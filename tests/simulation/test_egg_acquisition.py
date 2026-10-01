import importlib.util
import zipfile
from pathlib import Path


def load_module():
    path = Path("scripts/egg/acquire_egg.py")
    spec = importlib.util.spec_from_file_location("egg_acquire", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_verify_representative_egg_layout(tmp_path):
    module = load_module()

    eclipse = (
        tmp_path
        / "Egg_Model_Data_Files_v2"
        / "Eclipse"
    )
    eclipse.mkdir(parents=True)

    for name in module.REQUIRED_ECLIPSE_FILES:
        (eclipse / name).write_text(f"{name}\n")

    manifest = module.verify(tmp_path)

    assert manifest["dataset"] == "Egg Model"
    assert set(manifest["files"]) == set(module.REQUIRED_ECLIPSE_FILES)
    assert all(
        len(record["sha256"]) == 64
        for record in manifest["files"].values()
    )


def test_verify_rejects_missing_required_file(tmp_path):
    module = load_module()

    eclipse = tmp_path / "Eclipse"
    eclipse.mkdir()
    (eclipse / "Egg_Model_ECL.DATA").write_text("RUNSPEC\n")

    try:
        module.verify(tmp_path)
    except RuntimeError as exc:
        assert "Missing required files" in str(exc)
    else:
        raise AssertionError("missing Egg files were accepted")
