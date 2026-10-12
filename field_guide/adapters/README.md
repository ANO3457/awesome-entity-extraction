# Field Guide adapters

An adapter runs **one** extractor on **one** task card's fixture and records the
output. Adapters need heavy dependencies (models, ML libraries), so they run
in their own virtual environment. CI never imports them: the offline
evaluator only reads the `predictions.json` they write.

| Adapter | Task card | Environment |
|---|---|---|
| [`spacy_custom_ner.py`](spacy_custom_ner.py) | `custom-ner` | `examples/01-spacy-ner/requirements.txt` + `en_core_web_sm` 3.8.0 |
| [`presidio_pii.py`](presidio_pii.py) | `pii-redaction` | `examples/04-presidio-pii/requirements.txt` + `en_core_web_lg` 3.8.0 |

Each adapter writes down its configuration **before** results are seen, in its
docstring and the manifest `notes`: label mapping, thresholds, recognizers.
Don't tune them against the fixture. If you change a policy, record a new run
in a new folder; don't overwrite the old one.

## Reproduce a recorded run

From the repository root (Python 3.12, CPU only, no API keys):

```bash
IDX="--index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com"

# custom-ner with spaCy
uv venv --python 3.12 /tmp/fg-spacy
VIRTUAL_ENV=/tmp/fg-spacy uv pip install $IDX -r examples/01-spacy-ner/requirements.txt \
  https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
/tmp/fg-spacy/bin/python field_guide/adapters/spacy_custom_ner.py \
  --out /tmp/fg-repro/custom-ner

# pii-redaction with Presidio (en_core_web_lg is ~400 MB)
uv venv --python 3.12 /tmp/fg-presidio
VIRTUAL_ENV=/tmp/fg-presidio uv pip install $IDX -r examples/04-presidio-pii/requirements.txt \
  https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl
/tmp/fg-presidio/bin/python field_guide/adapters/presidio_pii.py \
  --out /tmp/fg-repro/pii-redaction

# Score your output (standard library only)
python3 scripts/run_field_guide.py score custom-ner /tmp/fg-repro/custom-ner/predictions.json
python3 scripts/run_field_guide.py score pii-redaction /tmp/fg-repro/pii-redaction/predictions.json
```

Model wheel checksums (SHA-256) used for the recorded runs:

| File | SHA-256 |
|---|---|
| `en_core_web_sm-3.8.0-py3-none-any.whl` | `1932429db727d4bff3deed6b34cfc05df17794f4a52eeb26cf8928f7c1a0fb85` |
| `en_core_web_lg-3.8.0-py3-none-any.whl` | `293e9547a655b25499198ab15a525b05b9407a75f10255e405e8c3854329ab63` |

Both adapters gave identical predictions across three runs on the recording
machine (timestamps aside). If yours differ, please
[open an issue](https://github.com/shivamnegi92/awesome-entity-extraction/issues/new/choose)
with your OS, CPU architecture, and `pip freeze`. An independent reproduction,
matching or not, is one of the most useful contributions to this project
(see issue #9).

## Add an adapter

1. Copy an existing adapter. Import `base_manifest`, `load_fixture`, and
   `write_json` from [`common.py`](common.py) so every manifest is recorded
   the same way.
2. Write the configuration policy in the docstring before running anything.
3. Write to `field_guide/results/<task>/<tool>-<version>-<model>-<model-version>/`.
4. Run `python3 scripts/run_field_guide.py validate --runs`, then `build`.
5. In the PR, include the exact environment and keep every miss. Don't remove
   cases that look bad.
