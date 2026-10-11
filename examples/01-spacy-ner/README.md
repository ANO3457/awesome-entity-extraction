# General-purpose NER with spaCy

Extract familiar person, organization, location, and date spans from a short
news-style sentence using spaCy's small English pipeline.

## Requirements

- Python 3.10–3.12 target
- CPU; first model download is about 12 MB

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
python -m spacy download en_core_web_sm
python main.py
```

Expected output includes `Tim Cook`, `Apple`, and `Paris`, with entity labels
and character offsets. The script checks those expected spans. Model predictions
are not a guarantee; this small pipeline is not open-vocabulary extraction.
