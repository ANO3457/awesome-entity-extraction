"""Generate relation triples with the REBEL sequence-to-sequence model.

Setup: uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
Run:   python main.py
Targeting Python 3.10-3.12. Model download is large; CPU inference is slow.
"""
import json
import re
from transformers import pipeline


def parse_triples(generated: str) -> list[dict[str, str]]:
    """Parse REBEL's <triplet>/<subj>/<obj> marker format."""
    triples = []
    subject = relation = obj = ""
    current = None
    for token in re.split(r"(<triplet>|<subj>|<obj>)", generated):
        token = token.strip()
        if token == "<triplet>":
            if subject and relation and obj:
                triples.append({"subject": subject, "relation": relation,
                                "object": obj})
            subject, relation, obj, current = "", "", "", "subject"
        elif token == "<subj>":
            current = "object"
        elif token == "<obj>":
            current = "relation"
        elif current == "subject":
            subject += token
        elif current == "object":
            obj += token
        elif current == "relation":
            relation += token
    if subject and relation and obj:
        triples.append({"subject": subject, "relation": relation, "object": obj})
    return triples


def main() -> None:
    text = "The Eiffel Tower is in Paris. Paris is the capital of France."
    extractor = pipeline("text2text-generation", model="Babelscape/rebel-large")
    generated = extractor(text, max_new_tokens=128, do_sample=False)[0]["generated_text"]
    triples = parse_triples(generated)
    print(json.dumps({"text": text, "triples": triples}, indent=2))
    assert all(set(row) == {"subject", "relation", "object"} for row in triples)
    assert triples, "No triples parsed; inspect generated model output."


if __name__ == "__main__":
    main()
