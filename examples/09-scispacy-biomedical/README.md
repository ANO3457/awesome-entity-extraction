# Biomedical entity extraction with scispaCy

Recognize biomedical entities in a synthetic, non-patient sentence using
scispaCy's `en_ner_bc5cdr_md` model (chemicals and diseases).

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bc5cdr_md-0.5.4.tar.gz
python main.py
```

Python 3.10–3.12 target. Model download is required and may be sizeable; access and
license terms are set by the model publisher. This is a teaching example, not
clinical advice or guidance for handling protected health information.
