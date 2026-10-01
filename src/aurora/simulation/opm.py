from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_OUTPUT_SUFFIXES = [
    ".EGRID",
    ".INIT",
    ".SMSPEC",
    ".UNSMRY",
    ".UNRST",
]


def docker_available() -> bool:
    if shutil.which("docker") is None:
        return False

    return subprocess.run(
        ["docker", "info"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def detect_opm_environment(root: Path) -> Dict[str, Any]:
    native = shutil.which("flow")
    docker = docker_available()

    cached_image = False
    if docker:
        probe = subprocess.run(
            [
                "docker",
                "image",
                "inspect",
                "openporousmedia/opmreleases:latest",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        cached_image = probe.returncode == 0

    preserved_version = root / "docs/tooling/raw/flow_version.txt"

    return {
        "native_flow": native or "NOT_FOUND",
        "docker": docker,
        "docker_image": (
            "openporousmedia/opmreleases:latest"
            if cached_image
            else "NOT_CACHED"
        ),
        "preserved_reference_version": (
            preserved_version.read_text().strip()
            if preserved_version.exists()
            else "UNKNOWN"
        ),
    }


def find_deck(deck_root: Path) -> Path:
    candidates = sorted(deck_root.rglob("Egg_Model_ECL.DATA"))
    if not candidates:
        candidates = sorted(deck_root.rglob("*.DATA"))

    if not candidates:
        raise FileNotFoundError(
            "No Eclipse DATA deck found under "
            f"{deck_root}. Run ./aurora egg acquire/verify first."
        )

    return candidates[0]


def inspect_reference_outputs(output_dir: Path) -> Dict[str, Any]:
    found: Dict[str, List[str]] = {}

    for suffix in REQUIRED_OUTPUT_SUFFIXES:
        found[suffix] = sorted(
            str(path)
            for path in output_dir.rglob(f"*{suffix}")
        )

    missing = [
        suffix
        for suffix, paths in found.items()
        if not paths
    ]

    return {
        "output_dir": str(output_dir),
        "required_suffixes": REQUIRED_OUTPUT_SUFFIXES,
        "found": found,
        "missing": missing,
        "complete": not missing,
    }
