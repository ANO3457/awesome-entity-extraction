"""Span + type metric: strict and overlap matching for NER-style tasks."""
from __future__ import annotations

from typing import Any

from .common import prf, unique_ids

Span = tuple[int, int, str]


def validate_fixture(fixture: dict[str, Any]) -> list[str]:
    errors = []
    if fixture.get("offset_convention") != "half_open":
        errors.append("NER fixture must declare half_open offsets")
    if fixture.get("offset_unit") != "unicode_codepoint":
        errors.append("NER fixture must declare unicode_codepoint offsets")
    examples = fixture.get("examples", [])
    errors.extend(unique_ids(examples, "NER"))
    for example in examples:
        text = example.get("text", "")
        for span in example.get("entities", []):
            start, end = span.get("start"), span.get("end")
            if not isinstance(start, int) or not isinstance(end, int):
                errors.append(f"{example['id']}: offsets must be integers")
                continue
            if not 0 <= start < end <= len(text):
                errors.append(f"{example['id']}: invalid offset range {start}:{end}")
            elif text[start:end] != span.get("text"):
                errors.append(f"{example['id']}: span text does not match offsets")
            if span.get("label") not in fixture.get("labels", []):
                errors.append(f"{example['id']}: unknown label {span.get('label')}")
    return errors


def validate_predictions(rows_by_id: dict[str, Any], source_by_id: dict[str, Any]) -> list[str]:
    errors = []
    for case_id, row in rows_by_id.items():
        source = source_by_id.get(case_id, {}).get("text", "")
        for entity in row.get("entities", []):
            start, end = entity.get("start"), entity.get("end")
            if (not isinstance(start, int) or not isinstance(end, int)
                    or not 0 <= start < end <= len(source)):
                errors.append(f"{case_id}: prediction has invalid offsets")
            elif source[start:end] != entity.get("text"):
                errors.append(f"{case_id}: predicted text does not match offsets")
    return errors


def _overlap_matches(gold: set[Span], pred: set[Span]) -> tuple[set[Span], set[Span]]:
    """Greedily pair same-label spans that overlap by at least one codepoint."""
    matched_gold: set[Span] = set()
    matched_pred: set[Span] = set()
    for gold_span in sorted(gold):
        for pred_span in sorted(pred - matched_pred):
            if (gold_span[2] == pred_span[2]
                    and max(gold_span[0], pred_span[0]) < min(gold_span[1], pred_span[1])):
                matched_gold.add(gold_span)
                matched_pred.add(pred_span)
                break
    return matched_gold, matched_pred


def score(fixture: dict[str, Any], predictions: dict[str, Any]) -> dict[str, Any]:
    """Score exact/overlap span+type matches; unknown/missing cases are errors."""
    gold_by_id = {row["id"]: row for row in fixture["examples"]}
    pred_rows = predictions.get("examples", [])
    pred_by_id = {row["id"]: row for row in pred_rows}
    if len(pred_by_id) != len(pred_rows):
        raise ValueError("duplicate prediction case id")
    unknown = set(pred_by_id) - set(gold_by_id)
    if unknown:
        raise ValueError(f"predictions contain unknown case IDs: {sorted(unknown)}")
    missing = set(gold_by_id) - set(pred_by_id)
    if missing:
        raise ValueError(f"predictions must explicitly include every fixture case; missing {sorted(missing)}")

    strict = [0, 0, 0]
    overlap = [0, 0, 0]
    case_rows = []
    for case_id, gold_case in gold_by_id.items():
        gold = {(x["start"], x["end"], x["label"]) for x in gold_case["entities"]}
        pred = {(int(x["start"]), int(x["end"]), x["label"])
                for x in pred_by_id[case_id].get("entities", [])}
        exact_tp = len(gold & pred)
        unmatched_gold, unmatched_pred = gold - pred, pred - gold
        matched_gold, matched_pred = _overlap_matches(unmatched_gold, unmatched_pred)

        strict[0] += exact_tp
        strict[1] += len(unmatched_pred)
        strict[2] += len(unmatched_gold)
        overlap[0] += exact_tp + len(matched_gold)
        overlap[1] += len(unmatched_pred) - len(matched_pred)
        overlap[2] += len(unmatched_gold) - len(matched_gold)
        case_rows.append({
            "id": case_id, "gold_count": len(gold), "prediction_count": len(pred),
            "strict_tp": exact_tp, "strict_fp": len(unmatched_pred),
            "strict_fn": len(unmatched_gold),
            "unmatched_gold": [list(x) for x in sorted(unmatched_gold - matched_gold)],
            "unmatched_predictions": [list(x) for x in sorted(unmatched_pred - matched_pred)],
        })
    return {"metric_note": "Span-level scores on a tiny synthetic fixture; not a real-world accuracy estimate.",
            "strict_span_type": prf(*strict),
            "overlap_span_type": prf(*overlap),
            "cases": case_rows}
