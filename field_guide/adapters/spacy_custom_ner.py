"""Record spaCy predictions for the custom-ner Field Guide task card.

Runs inside an isolated environment with spaCy and the model installed (see
field_guide/adapters/README.md). CI never imports it; the offline evaluator
only reads its output.

Label policy (fixed before looking at results): a spaCy label is kept only
when it is identical to one of the fixture's labels. Every other prediction
is dropped from scoring and kept in ``raw_predictions.json`` for review. No
label remapping (for example, LOC to GPE) is applied.
"""
from __future__ import annotations

import argparse
from importlib import metadata
from pathlib import Path

from common import base_manifest, load_fixture, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--model", default="en_core_web_sm")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    import spacy  # imported here so --help works without spaCy installed

    fixture = load_fixture("custom-ner")
    labels = set(fixture["labels"])
    nlp = spacy.load(args.model)

    scored, raw = [], []
    for case in fixture["examples"]:
        ents = [{"text": e.text, "label": e.label_, "start": e.start_char, "end": e.end_char}
                for e in nlp(case["text"]).ents]
        raw.append({"id": case["id"], "entities": ents})
        scored.append({"id": case["id"], "entities": [e for e in ents if e["label"] in labels]})

    dropped = sum(len(r["entities"]) - len(s["entities"]) for r, s in zip(raw, scored))
    model = f"{args.model}=={nlp.meta.get('version', 'unknown')}"
    run = {
        "tool": "spacy", "version": metadata.version("spacy"), "model": model,
        **base_manifest(fixture),
        "status": "passed", "network_or_api": False,
        "notes": (f"status=passed means the adapter produced output for every case; it is not a quality "
                  f"verdict. Label policy: identity on fixture labels {sorted(labels)}; {dropped} "
                  f"prediction(s) with other labels dropped from scoring and kept in raw_predictions.json. "
                  f"Model weights installed beforehand; inference ran offline."),
    }
    write_json(args.out / "predictions.json", {"run": run, "examples": scored})
    write_json(args.out / "raw_predictions.json", {"model": model, "examples": raw})
    print(f"Wrote {args.out}/predictions.json ({len(scored)} cases, {dropped} dropped label(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
