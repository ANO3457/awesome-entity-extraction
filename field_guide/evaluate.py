"""Dependency-free validation and scoring for field-guide runs.

This is not a model runner. It only scores outputs already produced by an
explicitly versioned adapter and recorded in a run manifest.

Tasks are discovered from ``tasks/<id>/fixture.json``; each fixture names its
metric (see ``field_guide/metrics``). Adding a task card needs no edits here.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .metrics import get_metric, pii_residual, spans

ROOT = Path(__file__).resolve().parent
TASKS = ROOT / "tasks"
RESULTS = ROOT / "results"
GUIDE_VERSION = "0.2.0"
MANIFEST_KEYS = ("tool", "version", "fixture_version", "run_date_utc", "environment",
                 "status", "command", "git_commit", "network_or_api")
RUN_STATUSES = {"passed", "partial", "failed"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def task_ids() -> list[str]:
    return sorted(p.parent.name for p in TASKS.glob("*/fixture.json"))


def load_fixture(task_id: str) -> dict[str, Any]:
    return load_json(TASKS / task_id / "fixture.json")


def _metric_for(task_id: str, fixture: dict[str, Any]):
    if "metric" not in fixture:
        raise KeyError(f"{task_id}: fixture.json must declare a 'metric'")
    return get_metric(fixture["metric"])


def validate_run(task_id: str, predictions: dict[str, Any], fixture: dict[str, Any]) -> list[str]:
    run = predictions.get("run")
    if not isinstance(run, dict):
        return ["prediction file must contain a run manifest"]
    errors = [f"run manifest missing {key}" for key in MANIFEST_KEYS
              if key not in run or run[key] in (None, "")]
    if run.get("fixture_version") != fixture.get("version"):
        errors.append("run fixture_version does not match current fixture")
    if run.get("status") not in RUN_STATUSES:
        errors.append("run status must be passed, partial, or failed")

    rows = predictions.get("examples", [])
    ids = [row.get("id") for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate prediction case id")
    if set(ids) != {row["id"] for row in fixture.get("examples", [])}:
        errors.append("predictions must include exactly one result for every fixture case")

    try:
        metric = _metric_for(task_id, fixture)
    except KeyError as exc:
        return errors + [str(exc)]
    rows_by_id = {row.get("id"): row for row in rows}
    source_by_id = {row["id"]: row for row in fixture.get("examples", [])}
    return errors + metric.validate_predictions(rows_by_id, source_by_id)


def score_task(task_id: str, fixture: dict[str, Any], predictions: dict[str, Any]) -> dict[str, Any]:
    return _metric_for(task_id, fixture).score(fixture, predictions)


def validate_task_fixtures() -> list[str]:
    errors = []
    for task_id in task_ids():
        rel = f"{task_id}/fixture.json"
        try:
            fixture = load_fixture(task_id)
            errors.extend(f"{rel}: {e}" for e in _metric_for(task_id, fixture).validate_fixture(fixture))
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
            errors.append(f"{rel}: {exc}")
    return errors


def recorded_runs(task_id: str) -> list[Path]:
    return sorted((RESULTS / task_id).glob("*/predictions.json"))


def build_report() -> dict[str, Any]:
    """Assemble only recorded runs; absent candidate data is explicitly not_run."""
    report: dict[str, Any] = {"guide_version": GUIDE_VERSION, "status": "draft",
                              "notice": "Tiny synthetic tasks. No results are inferred or run by report generation.",
                              "tasks": []}
    for task_id in task_ids():
        fixture = load_fixture(task_id)
        task: dict[str, Any] = {"id": task_id, "metric": fixture.get("metric"),
                                "fixture_version": fixture["version"], "runs": []}
        for predictions_path in recorded_runs(task_id):
            predictions = load_json(predictions_path)
            run = predictions.get("run", {})
            errors = validate_run(task_id, predictions, fixture)
            if errors:
                task["runs"].append({"status": "failed", "tool": run.get("tool"),
                                     "version": run.get("version"), "errors": errors})
                continue
            task["runs"].append({"status": run["status"], "manifest": run,
                                 "scores": score_task(task_id, fixture, predictions)})
        if not task["runs"]:
            task["status"] = "not_run"
        report["tasks"].append(task)
    return report


# Backwards-compatible names used by tests and the README's documented API.
validate_ner_fixture = spans.validate_fixture
validate_pii_fixture = pii_residual.validate_fixture
score_ner = spans.score
score_pii_residuals = pii_residual.score
