# Multilingual named entities with Stanza

Run a pretrained NER pipeline on short English, Spanish, and French examples.
Each language model downloads on the first run; this can take several minutes
and requires network access.

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
python main.py
```

Python 3.10–3.12 target; CPU inference. The example checks result structure, not exact
predictions, because multilingual model outputs can vary. Coverage and quality
vary by language.
