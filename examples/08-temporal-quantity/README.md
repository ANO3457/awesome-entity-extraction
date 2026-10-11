# Temporal and quantity extraction

Normalize a relative deadline against a fixed reference date and extract a
quantity/unit from an operations note using `dateparser` and `quantulum3`.

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
python main.py
```

Python 3.10–3.12 target. The reference date is fixed to keep the example reproducible.
Natural-language dates are ambiguous; locale, timezone, and unit conversions
need task-specific handling.
