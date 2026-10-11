# Custom zero-shot NER with GLiNER

Give the model custom labels at inference time, then inspect grounded spans and
scores. No task-specific training is required.

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
python main.py
```

Python 3.10–3.12 target; first run downloads the `urchade/gliner_multi-v2.1` model
(large download; allow network access and disk space). Output shows label,
source offsets, and a model score. Scores are not calibrated probabilities;
zero-shot predictions need review.
