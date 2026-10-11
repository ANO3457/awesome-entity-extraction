"""General-purpose named entities with spaCy's small English model.

Setup: uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
       python -m spacy download en_core_web_sm
Run:   python main.py
Targeting Python 3.10-3.12; model download required once.
"""
import json
import spacy


def main() -> None:
    nlp = spacy.load("en_core_web_sm")
    text = "Tim Cook said Apple will open a store in Paris on March 3, 2026."
    doc = nlp(text)
    entities = [
        {"text": ent.text, "label": ent.label_, "start": ent.start_char,
         "end": ent.end_char}
        for ent in doc.ents
    ]
    print(json.dumps({"text": text, "entities": entities}, indent=2))
    found = {(ent["text"], ent["label"]) for ent in entities}
    assert {("Tim Cook", "PERSON"), ("Apple", "ORG"), ("Paris", "GPE")} <= found


if __name__ == "__main__":
    main()
