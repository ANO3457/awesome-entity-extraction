"""Extract a few fields from a locally generated synthetic invoice PDF.

Setup: uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
Run:   python main.py
Targeting Python 3.10-3.12. This reads text PDFs; it does not do OCR.
"""
import json
import re
import tempfile
from pathlib import Path

import pdfplumber
from reportlab.pdfgen import canvas


def make_invoice(path: Path) -> None:
    pdf = canvas.Canvas(str(path))
    for y, line in zip((780, 750, 720, 690), (
        "ACME Sample Supplies", "Invoice Number: DEMO-1042",
        "Invoice Date: 2026-03-15", "Total: $1,234.50")):
        pdf.drawString(72, y, line)
    pdf.save()


def extract_fields(text: str) -> dict[str, str | float]:
    patterns = {
        "vendor": r"(?m)^([A-Z][A-Za-z ]+)$",
        "invoice_number": r"Invoice Number:\s*([A-Z0-9-]+)",
        "invoice_date": r"Invoice Date:\s*(\d{4}-\d{2}-\d{2})",
        "total": r"Total:\s*\$([\d,]+\.\d{2})",
    }
    result: dict[str, str | float] = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            value = match.group(1)
            result[field] = float(value.replace(",", "")) if field == "total" else value
    return result


def main() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = Path(temp_dir) / "synthetic-invoice.pdf"
        make_invoice(pdf_path)
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    fields = extract_fields(text)
    print(json.dumps({"fields": fields}, indent=2))
    assert fields["invoice_number"] == "DEMO-1042"
    assert fields["total"] == 1234.50
    assert fields["vendor"] == "ACME Sample Supplies"


if __name__ == "__main__":
    main()
