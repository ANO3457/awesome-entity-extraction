# Relation triples with REBEL

Extract subject–relation–object triples from a synthetic two-sentence news
snippet. The model is large and downloads on first run; CPU works but can be
slow. Requires network access to Hugging Face. Output is model-generated and
must be reviewed before use.

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
python main.py
```

This requirements file selects the CPU PyTorch wheel; a GPU is optional, and CPU inference may be slow. Model `Babelscape/rebel-large` downloads on first run and generated relations require review.

Targeting Python 3.10–3.12.
