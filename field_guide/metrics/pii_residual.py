"""PII residual metric: which known sensitive strings survive redaction."""
from __future__ import annotations

from typing import Any

from .common import unique_ids


def validate_fixture(fixture: dict[str, Any]) -> list[str]:
    examples = fixture.get("examples", [])
    errors = unique_ids(examples, "PII")
    for example in examples:
        text = example.get("text", "")
        for value in example.get("sensitive_values", []):
            if value not in text:
                errors.append(f"{example['id']}: sensitive value is not in source text")
    return errors


def validate_predictions(rows_by_id: dict[str, Any], source_by_id: dict[str, Any]) -> list[str]:
    errors = []
    for case_id, row in rows_by_id.items():
        if "source_text" in row or "original_text" in row:
            errors.append(f"{case_id}: raw input must not be stored in PII results")
        if not isinstance(row.get("redacted_text"), str):
            errors.append(f"{case_id}: missing redacted_text")
    return errors


def score(fixture: dict[str, Any], outputs: dict[str, Any]) -> dict[str, Any]:
    """Score exact residual strings only; this is not a privacy guarantee."""
    gold_by_id = {row["id"]: row for row in fixture["examples"]}
    output_rows = outputs.get("examples", [])
    output_by_id = {row["id"]: row for row in output_rows}
    if len(output_by_id) != len(output_rows):
        raise ValueError("duplicate PII output case id")
    if set(output_by_id) != set(gold_by_id):
        raise ValueError("PII outputs must include exactly one result per fixture case")
    rows, expected, residuals = [], 0, 0
    for case_id, source in gold_by_id.items():
        redacted = output_by_id[case_id].get("redacted_text")
        if not isinstance(redacted, str):
            raise ValueError(f"{case_id}: redacted_text must be a string")
        sensitive = source.get("sensitive_values", [])
        remain = [value for value in sensitive if value in redacted]
        expected += len(sensitive)
        residuals += len(remain)
        rows.append({"id": case_id, "sensitive_value_count": len(sensitive),
                     "residual_values": remain,
                     "expected_type_coverage": output_by_id[case_id].get("detected_types", [])})
    return {"metric_note": "Exact fixture-string residuals only; not comprehensive PII recall, safety, or compliance.",
            "sensitive_values_expected": expected, "sensitive_values_remaining": residuals,
            "residual_rate": residuals / expected if expected else None, "cases": rows}
