# Synthetic invoice fields from PDF text

Generate a tiny synthetic text PDF locally, read it with `pdfplumber`, then
normalize invoice fields with transparent rules. No external invoice fixture or
OCR is involved.

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
python main.py
```

Python 3.10–3.12 target. The demo PDF is generated in a temporary directory and
removed automatically. Scanned/image PDFs, varied layouts, tax interpretation,
and production invoice validation are out of scope.
