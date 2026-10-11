"""Biomedical entities with scispaCy's BC5CDR model.

Setup: uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
       Install en_ner_bc5cdr_md from the model link in README.md.
Run:   python main.py
Targeting Python 3.10-3.12. Not for clinical use or patient data.
"""
import json
import spacy


def main() -> None:
    try:
        nlp = spacy.load("en_ner_bc5cdr_md")
    except OSError as exc:
        raise SystemExit("Install en_ner_bc5cdr_md using the README instructions.") from exc
    text = "Aspirin may reduce inflammation, while diabetes requires careful monitoring."
    doc = nlp(text)
    entities = [{"text": ent.text, "label": ent.label_, "start": ent.start_char,
                 "end": ent.end_char} for ent in doc.ents]
    print(json.dumps({"text": text, "entities": entities}, indent=2))
    assert all(text[item["start"]:item["end"]] == item["text"] for item in entities)
    assert entities, "No biomedical entities recognized; inspect model installation."


if __name__ == "__main__":
    main()
