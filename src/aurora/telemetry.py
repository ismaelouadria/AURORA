from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def git_commit(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "UNKNOWN"


class JsonlTelemetry:
    """Required step telemetry.

    Failure to persist a required record is raised to the caller. Telemetry is
    observational and has no authority to modify actions or simulator state.
    """

    def __init__(
        self,
        path: Path,
        *,
        run_id: str,
        root: Path,
        seed: int,
        configuration: Dict[str, Any],
        reference_id: str,
    ) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.run_id = run_id
        self.root = root
        self.seed = seed
        self.configuration = configuration
        self.reference_id = reference_id
        self.commit = git_commit(root)

    def record(self, record: Dict[str, Any]) -> None:
        payload = {
            "schema_version": 1,
            "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
            "run_id": self.run_id,
            "commit": self.commit,
            "seed": self.seed,
            "reference_id": self.reference_id,
            "configuration": self.configuration,
            **record,
        }

        try:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, sort_keys=True) + "\n")
                handle.flush()
        except Exception as exc:
            raise RuntimeError(
                "REQUIRED_PROVENANCE_WRITE_FAILED: "
                f"could not persist {self.path}: {exc}"
            ) from exc
