# Entity linking with Wikidata search

Resolve an ambiguous `Jordan` mention from context by querying Wikidata's public
MediaWiki API, then show the selected item ID and label. No model download or
API key is needed; a network connection is required. Please use responsibly and
respect the API's usage guidelines.

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
python main.py
```

Python 3.10–3.12 target. This small baseline uses context keywords to rank search
results, not a learned linker. Ambiguity remains; the script reports candidates
and may explicitly return no selected candidate when context provides no signal.
