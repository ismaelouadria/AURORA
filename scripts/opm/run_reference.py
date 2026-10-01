#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from aurora.simulation.opm import (
    detect_opm_environment,
    find_deck,
    inspect_reference_outputs,
)


IMAGE = "openporousmedia/opmreleases:latest"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deck-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--engine",
        choices=["auto", "native", "docker"],
        default="auto",
    )
    args = parser.parse_args()

    deck_root = Path(args.deck_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    deck = find_deck(deck_root)
    environment = detect_opm_environment(ROOT)

    engine = args.engine
    if engine == "auto":
        if environment["native_flow"] != "NOT_FOUND":
            engine = "native"
        elif environment["docker"] and environment["docker_image"] != "NOT_CACHED":
            engine = "docker"
        else:
            print(
                "No supported OPM Flow execution environment found. "
                "Install native Flow or make the documented OPM Docker "
                "image available.",
                file=sys.stderr,
            )
            return 2

    log = output_dir / "flow.log"

    if engine == "native":
        command = [
            str(environment["native_flow"]),
            str(deck),
            f"--output-dir={output_dir}",
        ]
    else:
        relative_deck = deck.relative_to(deck_root)
        command = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{deck_root}:/case:ro",
            "-v",
            f"{output_dir}:/output",
            IMAGE,
            "flow",
            f"/case/{relative_deck}",
            "--output-dir=/output",
        ]

    started = datetime.now(timezone.utc).isoformat()

    with log.open("w", encoding="utf-8") as handle:
        result = subprocess.run(
            command,
            stdout=handle,
            stderr=subprocess.STDOUT,
            text=True,
        )

    inspection = inspect_reference_outputs(output_dir)

    manifest = {
        "schema_version": 1,
        "reference_role": (
            "higher-fidelity numerical reference; not physical ground truth"
        ),
        "started_at_utc": started,
        "engine": engine,
        "command": command,
        "deck": str(deck),
        "deck_sha256": sha256(deck),
        "environment": environment,
        "exit_status": result.returncode,
        "outputs": inspection,
        "successful": result.returncode == 0 and inspection["complete"],
    }

    (output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )

    print(json.dumps(manifest, indent=2))

    if result.returncode != 0:
        print(f"OPM Flow failed. Inspect {log}", file=sys.stderr)
        return result.returncode or 1

    if not inspection["complete"]:
        print(
            "Flow exited successfully but required reference outputs are "
            f"missing: {inspection['missing']}",
            file=sys.stderr,
        )
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
