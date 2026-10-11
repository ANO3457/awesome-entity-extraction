"""Detect and anonymize synthetic PII with Microsoft Presidio.

Setup: uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
       python -m spacy download en_core_web_lg
Run:   python main.py
Targeting Python 3.10-3.12. Never use real PII in this example.
"""
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


def main() -> None:
    # Synthetic values only. Keep source text out of output/logs by default.
    text = "Call Jane Doe at 555-123-4567 or jane@example.com."
    findings = AnalyzerEngine().analyze(text=text, language="en")
    redacted = AnonymizerEngine().anonymize(text=text, analyzer_results=findings)
    print("Detected types:", sorted({item.entity_type for item in findings}))
    print("Redacted:", redacted.text)
    assert "jane@example.com" not in redacted.text
    assert "555-123-4567" not in redacted.text
    assert "Jane Doe" not in redacted.text


if __name__ == "__main__":
    main()
