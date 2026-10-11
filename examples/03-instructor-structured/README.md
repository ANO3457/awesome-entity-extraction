# Structured business extraction with Instructor

Extract typed fields from a short note using an OpenAI-compatible hosted model.
This is the only example here that requires credentials and may incur API
charges. The example uses `gpt-4o-mini`; set `OPENAI_API_KEY` before running.
Never commit credentials or use private text in this demo.

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
export OPENAI_API_KEY="..."  # Windows PowerShell: $env:OPENAI_API_KEY="..."
python main.py
```

Python 3.10–3.12 target. Instructor validates the response against a Pydantic model;
that validates shape, not factual correctness. The network call is non-deterministic.
