#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smspec", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--vectors", nargs="+", required=True)
    args = parser.parse_args()

    smspec = Path(args.smspec).resolve()
    output = Path(args.output).resolve()

    if not smspec.is_file():
        print(f"SMSPEC not found: {smspec}", file=sys.stderr)
        return 2

    summary = shutil.which("summary")
    if summary is None:
        print(
            "OPM 'summary' utility is not available natively. "
            "Extraction is intentionally blocked rather than guessing at "
            "binary SMSPEC/UNSMRY semantics.",
            file=sys.stderr,
        )
        return 2

    available_result = subprocess.run(
        [summary, str(smspec), "-l"],
        capture_output=True,
        text=True,
    )

    if available_result.returncode != 0:
        print(available_result.stderr, file=sys.stderr)
        return available_result.returncode or 1

    available_text = available_result.stdout
    missing = [
        vector
        for vector in args.vectors
        if vector not in available_text
    ]

    if missing:
        print(
            "Requested vectors are not proven available in this SMSPEC: "
            + ", ".join(missing),
            file=sys.stderr,
        )
        return 3

    result = subprocess.run(
        [summary, str(smspec), *args.vectors],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode or 1

    output.parent.mkdir(parents=True, exist_ok=True)

    # Preserve the tool output without inventing semantic parsing rules.
    raw_path = output.with_suffix(".summary.txt")
    raw_path.write_text(result.stdout)

    metadata = {
        "schema_version": 1,
        "source_smspec": str(smspec),
        "source_smspec_sha256": sha256(smspec),
        "vectors_requested": args.vectors,
        "units_policy": (
            "Units must be taken from the simulator summary metadata/tool "
            "output and the canonical output contract; never inferred from "
            "vector names alone."
        ),
        "timing_policy": (
            "Simulator report timing must remain traceable to the source run."
        ),
        "raw_extraction": str(raw_path),
    }

    output.write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
