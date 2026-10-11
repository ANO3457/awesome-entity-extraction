"""Zero-shot custom entity types using GLiNER.

Setup: uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
Run:   python main.py
Targeting Python 3.10-3.12. First run downloads a pretrained model.
"""
import json
from gliner import GLiNER


def main() -> None:
    text = "Tim Cook said Apple will invest $2 billion in Paris by 2026."
    labels = ["person", "company", "money amount", "location", "date"]
    model = GLiNER.from_pretrained("urchade/gliner_multi-v2.1")
    predictions = model.predict_entities(text, labels)
    entities = []
    for item in predictions:
        start, end = int(item["start"]), int(item["end"])
        assert 0 <= start < end <= len(text)
        assert text[start:end] == item["text"]
        entities.append({"text": item["text"], "label": item["label"],
                         "start": start, "end": end,
                         "score": round(float(item["score"]), 3)})
    print(json.dumps({"text": text, "entities": entities}, indent=2))
    assert entities, "Model returned no spans; try reviewing labels/model setup."


if __name__ == "__main__":
    main()
