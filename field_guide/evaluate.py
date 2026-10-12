"""Dependency-free validation and task-specific scoring for field-guide runs.

This is not a model runner. It only scores outputs already produced by an
explicitly versioned adapter and recorded in a run manifest.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
TASKS = ROOT / "tasks"
RESULTS = ROOT / "results"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_ner_fixture(fixture: dict[str, Any]) -> list[str]:
    errors = []
    if fixture.get("offset_convention") != "half_open":
        errors.append("NER fixture must declare half_open offsets")
    if fixture.get("offset_unit") != "unicode_codepoint":
        errors.append("NER fixture must declare unicode_codepoint offsets")
    ids = set()
    for example in fixture.get("examples", []):
        if example["id"] in ids:
            errors.append(f"duplicate NER fixture id: {example['id']}")
        ids.add(example["id"])
        text = example.get("text", "")
        for span in example.get("entities", []):
            start, end = span.get("start"), span.get("end")
            if not isinstance(start, int) or not isinstance(end, int):
                errors.append(f"{example['id']}: offsets must be integers")
                continue
            if not (0 <= start < end <= len(text)):
                errors.append(f"{example['id']}: invalid offset range {start}:{end}")
            elif text[start:end] != span.get("text"):
                errors.append(f"{example['id']}: span text does not match offsets")
            if span.get("label") not in fixture.get("labels", []):
                errors.append(f"{example['id']}: unknown label {span.get('label')}")
    return errors


def validate_pii_fixture(fixture: dict[str, Any]) -> list[str]:
    errors = []
    ids = set()
    for example in fixture.get("examples", []):
        if example["id"] in ids:
            errors.append(f"duplicate PII fixture id: {example['id']}")
        ids.add(example["id"])
        text = example.get("text", "")
        for value in example.get("sensitive_values", []):
            if value not in text:
                errors.append(f"{example['id']}: sensitive value is not in source text")
    return errors


def validate_run(task_id: str, predictions: dict[str, Any], fixture: dict[str, Any]) -> list[str]:
    errors = []
    run = predictions.get("run")
    if not isinstance(run, dict):
        return ["prediction file must contain a run manifest"]
    required = ("tool", "version", "fixture_version", "run_date_utc", "environment", "status", "command", "git_commit", "network_or_api")
    for key in required:
        if key not in run or run[key] in (None, ""):
            errors.append(f"run manifest missing {key}")
    if run.get("fixture_version") != fixture.get("version"):
        errors.append("run fixture_version does not match current fixture")
    if run.get("status") not in {"passed", "partial", "failed"}:
        errors.append("run status must be passed, partial, or failed")
    expected_ids = {row["id"] for row in fixture.get("examples", [])}
    actual_rows = predictions.get("examples", [])
    actual_ids = [row.get("id") for row in actual_rows]
    if len(actual_ids) != len(set(actual_ids)):
        errors.append("duplicate prediction case id")
    if set(actual_ids) != expected_ids:
        errors.append("predictions must include exactly one result for every fixture case")
    by_id = {row.get("id"): row for row in actual_rows}
    source_by_id = {row["id"]: row for row in fixture.get("examples", [])}
    if task_id == "custom-ner":
        for case_id, row in by_id.items():
            source = source_by_id.get(case_id, {}).get("text", "")
            for entity in row.get("entities", []):
                start, end = entity.get("start"), entity.get("end")
                if not isinstance(start, int) or not isinstance(end, int) or not 0 <= start < end <= len(source):
                    errors.append(f"{case_id}: prediction has invalid offsets")
                elif source[start:end] != entity.get("text"):
                    errors.append(f"{case_id}: predicted text does not match offsets")
    elif task_id == "pii-redaction":
        for case_id, row in by_id.items():
            if "source_text" in row or "original_text" in row:
                errors.append(f"{case_id}: raw input must not be stored in PII results")
            if not isinstance(row.get("redacted_text"), str):
                errors.append(f"{case_id}: missing redacted_text")
    else:
        errors.append(f"unknown task: {task_id}")
    return errors


def _prf(tp: int, fp: int, fn: int) -> dict[str, float | int]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp": tp, "fp": fp, "fn": fn,
            "precision": precision, "recall": recall, "f1": f1}


def score_ner(fixture: dict[str, Any], predictions: dict[str, Any]) -> dict[str, Any]:
    """Score exact/overlap span+type matches; unknown/missing cases are errors."""
    gold_by_id = {row["id"]: row for row in fixture["examples"]}
    pred_by_id = {row["id"]: row for row in predictions.get("examples", [])}
    if len(pred_by_id) != len(predictions.get("examples", [])):
        raise ValueError("duplicate prediction case id")
    unknown = set(pred_by_id) - set(gold_by_id)
    if unknown:
        raise ValueError(f"predictions contain unknown case IDs: {sorted(unknown)}")
    if set(pred_by_id) != set(gold_by_id):
        missing = set(gold_by_id) - set(pred_by_id)
        raise ValueError(f"predictions must explicitly include every fixture case; missing {sorted(missing)}")
    strict_tp = strict_fp = strict_fn = 0
    overlap_tp = overlap_fp = overlap_fn = 0
    case_rows = []
    for case_id, gold_case in gold_by_id.items():
        gold = {(x["start"], x["end"], x["label"]) for x in gold_case["entities"]}
        pred = {(int(x["start"]), int(x["end"]), x["label"])
                for x in pred_by_id[case_id].get("entities", [])}
        exact_tp = len(gold & pred)
        strict_tp += exact_tp
        strict_fp += len(pred - gold)
        strict_fn += len(gold - pred)
        unmatched_gold, unmatched_pred = set(gold - pred), set(pred - gold)
        matched_gold: set[tuple[int, int, str]] = set()
        matched_pred: set[tuple[int, int, str]] = set()
        for gold_span in sorted(unmatched_gold):
            for pred_span in sorted(unmatched_pred - matched_pred):
                if (gold_span[2] == pred_span[2]
                        and max(gold_span[0], pred_span[0]) < min(gold_span[1], pred_span[1])):
                    matched_gold.add(gold_span)
                    matched_pred.add(pred_span)
                    break
        overlap_tp += exact_tp + len(matched_gold)
        overlap_fp += len(unmatched_pred) - len(matched_pred)
        overlap_fn += len(unmatched_gold) - len(matched_gold)
        case_rows.append({"id": case_id, "gold_count": len(gold),
                          "prediction_count": len(pred), "strict_tp": exact_tp,
                          "strict_fp": len(pred - gold), "strict_fn": len(gold - pred),
                          "unmatched_gold": [list(x) for x in sorted(unmatched_gold - matched_gold)],
                          "unmatched_predictions": [list(x) for x in sorted(unmatched_pred - matched_pred)]})
    return {"metric_note": "Span-level scores on a tiny synthetic fixture; not a real-world accuracy estimate.",
            "strict_span_type": _prf(strict_tp, strict_fp, strict_fn),
            "overlap_span_type": _prf(overlap_tp, overlap_fp, overlap_fn),
            "cases": case_rows}


def score_pii_residuals(fixture: dict[str, Any], outputs: dict[str, Any]) -> dict[str, Any]:
    """Score exact residual strings only; this is not a privacy guarantee."""
    gold_by_id = {row["id"]: row for row in fixture["examples"]}
    output_by_id = {row["id"]: row for row in outputs.get("examples", [])}
    if len(output_by_id) != len(outputs.get("examples", [])):
        raise ValueError("duplicate PII output case id")
    if set(output_by_id) != set(gold_by_id):
        raise ValueError("PII outputs must include exactly one result per fixture case")
    rows, expected, residuals = [], 0, 0
    for case_id, source in gold_by_id.items():
        output = output_by_id[case_id]
        redacted = output.get("redacted_text")
        if not isinstance(redacted, str):
            raise ValueError(f"{case_id}: redacted_text must be a string")
        remain = [value for value in source.get("sensitive_values", []) if value in redacted]
        expected += len(source.get("sensitive_values", []))
        residuals += len(remain)
        rows.append({"id": case_id, "sensitive_value_count": len(source.get("sensitive_values", [])),
                     "residual_values": remain,
                     "expected_type_coverage": output.get("detected_types", [])})
    return {"metric_note": "Exact fixture-string residuals only; not comprehensive PII recall, safety, or compliance.",
            "sensitive_values_expected": expected, "sensitive_values_remaining": residuals,
            "residual_rate": residuals / expected if expected else None, "cases": rows}


def validate_task_fixtures() -> list[str]:
    errors = []
    for rel, validator in (("custom-ner/fixture.json", validate_ner_fixture),
                            ("pii-redaction/fixture.json", validate_pii_fixture)):
        try:
            errors.extend(f"{rel}: {error}" for error in validator(load_json(TASKS / rel)))
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
            errors.append(f"{rel}: {exc}")
    return errors


def build_report() -> dict[str, Any]:
    """Assemble only recorded runs; absent candidate data is explicitly not_run."""
    report: dict[str, Any] = {"guide_version": "0.1.0", "status": "draft",
                              "notice": "Tiny synthetic tasks. No results are inferred or run by report generation.",
                              "tasks": []}
    for task_id in ("custom-ner", "pii-redaction"):
        task_path = TASKS / task_id
        fixture = load_json(task_path / "fixture.json")
        task: dict[str, Any] = {"id": task_id, "fixture_version": fixture["version"], "runs": []}
        result_dir = RESULTS / task_id
        if result_dir.exists():
            for predictions_path in sorted(result_dir.glob("*/predictions.json")):
                predictions = load_json(predictions_path)
                errors = validate_run(task_id, predictions, fixture)
                run = predictions.get("run", {})
                if errors:
                    task["runs"].append({"status": "failed", "tool": run.get("tool"),
                                         "version": run.get("version"), "errors": errors})
                    continue
                scores = (score_ner(fixture, predictions) if task_id == "custom-ner"
                          else score_pii_residuals(fixture, predictions))
                task["runs"].append({"status": run["status"], "manifest": run,
                                     "scores": scores})
        if not task["runs"]:
            task["status"] = "not_run"
        report["tasks"].append(task)
    return report
