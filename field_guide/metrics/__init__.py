"""Pluggable task metrics for Field Guide task cards.

Each metric module exposes three functions:

* ``validate_fixture(fixture) -> list[str]``: gold-data sanity checks.
* ``validate_predictions(rows_by_id, source_by_id) -> list[str]``: per-row
  checks on a recorded run (case coverage and the manifest are checked by the
  caller, once, for every metric).
* ``score(fixture, predictions) -> dict``: scores for a validated run.

A task card picks its metric with the ``"metric"`` key in ``fixture.json``.
Adding a metric means adding a module and one line to ``METRICS``. No other
metric needs to change.
"""
from __future__ import annotations

from types import ModuleType

from . import pii_residual, spans

METRICS: dict[str, ModuleType] = {
    "spans": spans,
    "pii_residual": pii_residual,
}


def get_metric(name: str) -> ModuleType:
    try:
        return METRICS[name]
    except KeyError:
        known = ", ".join(sorted(METRICS))
        raise KeyError(f"unknown metric {name!r}; known metrics: {known}") from None
