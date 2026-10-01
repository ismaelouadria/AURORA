#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path


REQUIRED_ECLIPSE_FILES = [
    "Egg_Model_ECL.DATA",
    "PERMX.INC",
    "PERMY.INC",
    "PERMZ.INC",
    "PORO.INC",
    "SCHEDULE_NEW.INC",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def locate_eclipse(root: Path) -> Path:
    matches = [
        path.parent
        for path in root.rglob("Egg_Model_ECL.DATA")
    ]

    if len(matches) != 1:
        raise RuntimeError(
            "Expected exactly one Egg Eclipse directory containing "
            f"Egg_Model_ECL.DATA; found {len(matches)}."
        )

    return matches[0]


def verify(root: Path) -> dict:
    eclipse = locate_eclipse(root)

    missing = [
        name
        for name in REQUIRED_ECLIPSE_FILES
        if not (eclipse / name).is_file()
    ]

    if missing:
        raise RuntimeError(
            "Egg verification failed. Missing required files: "
            + ", ".join(missing)
        )

    manifest = {
        "schema_version": 1,
        "dataset": "Egg Model",
        "source_policy": (
            "External benchmark dependency. Do not commit bulk Egg source "
            "or generated OPM outputs to the repository."
        ),
        "eclipse_root": str(eclipse),
        "files": {
            name: {
                "sha256": sha256(eclipse / name),
                "bytes": (eclipse / name).stat().st_size,
            }
            for name in REQUIRED_ECLIPSE_FILES
        },
    }

    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive")
    parser.add_argument("--destination", required=True)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    destination = Path(args.destination)

    if args.verify_only:
        if not destination.exists():
            print(
                "Egg root does not exist. Obtain the authoritative Egg "
                "package described in docs/simulation/EGG_ACQUISITION.md "
                "and run ./aurora egg acquire --archive <zip>.",
                file=sys.stderr,
            )
            return 2
    else:
        if not args.archive:
            print(
                "No archive supplied. AURORA intentionally does not embed "
                "or silently fetch an unverified bulk Egg package. Download "
                "the authoritative Egg archive documented in "
                "docs/simulation/EGG_ACQUISITION.md, then provide "
                "--archive <path>.",
                file=sys.stderr,
            )
            return 2

        archive = Path(args.archive)
        if not archive.is_file():
            print(f"Archive not found: {archive}", file=sys.stderr)
            return 2

        if destination.exists():
            print(
                f"Destination already exists: {destination}. "
                "Refusing to overwrite an existing prepared dataset.",
                file=sys.stderr,
            )
            return 2

        destination.mkdir(parents=True)

        try:
            with zipfile.ZipFile(archive) as zf:
                bad = zf.testzip()
                if bad is not None:
                    raise RuntimeError(
                        f"ZIP integrity failure at member: {bad}"
                    )
                zf.extractall(destination)
        except Exception:
            shutil.rmtree(destination, ignore_errors=True)
            raise

        archive_record = {
            "archive": archive.name,
            "sha256": sha256(archive),
            "bytes": archive.stat().st_size,
        }
        (destination / "ARCHIVE_PROVENANCE.json").write_text(
            json.dumps(archive_record, indent=2) + "\n"
        )

    manifest = verify(destination)
    (destination / "AURORA_EGG_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )

    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
