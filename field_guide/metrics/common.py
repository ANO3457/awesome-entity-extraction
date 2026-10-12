"""Helpers shared by metric modules."""
from __future__ import annotations

from typing import Any


def prf(tp: int, fp: int, fn: int) -> dict[str, float | int]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp": tp, "fp": fp, "fn": fn,
            "precision": precision, "recall": recall, "f1": f1}


def unique_ids(rows: list[dict[str, Any]], what: str) -> list[str]:
    """Return errors for duplicate ``id`` values in fixture rows."""
    seen: set[str] = set()
    errors = []
    for row in rows:
        if row["id"] in seen:
            errors.append(f"duplicate {what} fixture id: {row['id']}")
        seen.add(row["id"])
    return errors
