"""Record Presidio redactions for the pii-redaction Field Guide task card.

Runs inside an isolated environment with Presidio and its spaCy model
installed (see field_guide/adapters/README.md). CI never imports it.

Configuration (fixed before looking at results): Presidio defaults, i.e.
``AnalyzerEngine()`` with the built-in English recognizers and spaCy
``en_core_web_lg``, and ``AnonymizerEngine()`` default replace-with-type.
No thresholds, allow-lists, or custom recognizers. Only redacted text is
recorded; the source text is never written out.
"""
from __future__ import annotations

import argparse
from importlib import metadata
from pathlib import Path

from common import base_manifest, load_fixture, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    import spacy
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine

    fixture = load_fixture("pii-redaction")
    analyzer, anonymizer = AnalyzerEngine(), AnonymizerEngine()
    rows = []
    for case in fixture["examples"]:
        findings = analyzer.analyze(text=case["text"], language="en")
        rows.append({"id": case["id"],
                     "redacted_text": anonymizer.anonymize(text=case["text"], analyzer_results=findings).text,
                     "detected_types": sorted({f.entity_type for f in findings})})

    spacy_model = spacy.load("en_core_web_lg").meta.get("version", "unknown")
    run = {
        "tool": "presidio", "version": metadata.version("presidio-analyzer"),
        "model": f"en_core_web_lg=={spacy_model} (spaCy {metadata.version('spacy')})",
        **base_manifest(fixture),
        "status": "passed", "network_or_api": False,
        "notes": ("status=passed means the adapter produced output for every case; it is not a quality "
                  "verdict. Presidio defaults: AnalyzerEngine() built-in English recognizers, "
                  "AnonymizerEngine() replace-with-type; no thresholds or custom recognizers. "
                  "Model weights installed beforehand; inference ran offline."),
    }
    write_json(args.out / "predictions.json", {"run": run, "examples": rows})
    print(f"Wrote {args.out}/predictions.json ({len(rows)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
