"""Multilingual NER in English, Spanish, and French with Stanza.

Setup: uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
Run:   python main.py
Targeting Python 3.10-3.12. Downloads three language models on first run.
"""
import json
import stanza

SAMPLES = {
    "en": "Apple opened a new office in London.",
    "es": "Apple abrió una nueva oficina en Madrid.",
    "fr": "Apple a ouvert un nouveau bureau à Paris.",
}


def main() -> None:
    output = {}
    for language, text in SAMPLES.items():
        stanza.download(language, processors="tokenize,ner", verbose=False)
        doc = stanza.Pipeline(language, processors="tokenize,ner", verbose=False)(text)
        entities = [{"text": entity.text, "type": entity.type}
                    for entity in doc.ents]
        output[language] = {"text": text, "entities": entities}
        assert all("text" in item and "type" in item for item in entities)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
