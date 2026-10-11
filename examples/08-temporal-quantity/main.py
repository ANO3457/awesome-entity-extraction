"""Normalize dates and extract quantities from an operations note.

Setup: uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
Run:   python main.py
Targeting Python 3.10-3.12. Uses an explicit reference date for reproducibility.
"""
import json
from datetime import datetime

import dateparser
from quantulum3 import parser as quantity_parser


def main() -> None:
    reference = datetime(2026, 1, 1)
    text = "Ship 12 pallets within 3 days and keep each below 500 kilograms."
    date_text = "in 3 days"
    parsed_date = dateparser.parse(
        date_text,
        settings={"RELATIVE_BASE": reference, "PREFER_DATES_FROM": "future"},
    )
    quantities = quantity_parser.parse(text)
    records = [{"value": item.value, "unit": item.unit.name,
                "surface": item.surface} for item in quantities]
    result = {"reference_date": reference.date().isoformat(),
              "normalized_date": parsed_date.date().isoformat() if parsed_date else None,
              "quantities": records}
    print(json.dumps(result, indent=2))
    assert result["normalized_date"] == "2026-01-04"
    assert any(item["value"] == 12 for item in records)
    assert any(item["value"] == 500 for item in records)


if __name__ == "__main__":
    main()
