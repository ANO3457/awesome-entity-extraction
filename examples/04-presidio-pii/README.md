# PII detection and redaction with Presidio

Detect likely personal data in a synthetic contact message, then redact it. The
demo prints entity types and the redacted text only (not the original message).

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
python -m spacy download en_core_web_lg
python main.py
```

Python 3.10–3.12 target; model download is required once. Detection is probabilistic
and may miss PII; redaction is not a compliance guarantee. Use synthetic data.
