"""Shared helpers for Field Guide adapters (run-manifest fields, output).

Adapters run in isolated environments with heavy dependencies installed. This
module is standard-library only, so any adapter can import it.
"""
from __future__ import annotations

import datetime as dt
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def load_fixture(task_id: str) -> dict[str, Any]:
    return json.loads((ROOT / "field_guide/tasks" / task_id / "fixture.json").read_text(encoding="utf-8"))


def base_manifest(fixture: dict[str, Any]) -> dict[str, Any]:
    """Manifest fields every adapter records the same way."""
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True, check=False).stdout.strip()
    script = Path(sys.argv[0]).resolve()
    try:
        script_rel = script.relative_to(ROOT).as_posix()
    except ValueError:
        script_rel = script.name
    return {
        "fixture_version": fixture["version"],
        "run_date_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "environment": f"{platform.system()} {platform.machine()}; Python {platform.python_version()}; CPU",
        "command": " ".join(["python", script_rel, *sys.argv[1:]]),
        "git_commit": commit or "unknown",
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
