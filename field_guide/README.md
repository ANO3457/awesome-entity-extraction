# Entity Extraction Field Guide (prototype)

A small decision-and-evidence companion to the catalog. It helps narrow a
starting approach and defines two versioned, synthetic task cards, each with one
recorded, reproducible run. It is **not** a benchmark leaderboard: a six-case
fixture describes behaviour and cannot estimate production accuracy.

## Choose a starting point

The maintained machine-readable version is [`decision_matrix.json`](decision_matrix.json),
the **only** place scenarios are defined (CI rejects a second copy). Paths in it are
relative to the repository root and are checked to exist. This table is its quick
human-readable summary; confirm model, API, license, and system requirements at the
linked source before adoption.

| Your task / constraint | Start by trying | Important caveat | Example |
|---|---|---|---|
| Common English person/company/place spans; local baseline | spaCy `en_core_web_sm` | Fixed common labels; domain recall varies | [Run spaCy NER](../examples/01-spacy-ner/README.md) |
| Caller-defined entity labels; no task-specific training | GLiNER multi v2.1 | Model download; scores are not calibrated probabilities | [Run GLiNER](../examples/02-gliner-zero-shot/README.md) |
| Local PII detection and redaction | Presidio | Missed PII remains possible; not a compliance guarantee | [Run Presidio](../examples/04-presidio-pii/README.md) |
| Typed fields from short messy text; hosted API permitted | Instructor + Pydantic | Needs a provider API key; possible charge; valid schema is not factuality | [Run structured extraction](../examples/03-instructor-structured/README.md) |
| Known-layout text PDF | pdfplumber + explicit rules | Scanned pages require OCR; layout-specific rules need review | [Run invoice demo](../examples/06-invoice-pdf/README.md) |
| Scanned/layout-heavy docs, tables, OCR | Docling / Marker / Unstructured / Surya | Higher setup/model cost; OCR errors affect downstream extraction | [Catalog section](../README.md#-document-and-layout-extraction) |

Recommendations are starting points, not endorsements or performance rankings.
"No API key" does not mean "no model download"; validate whether downloaded
weights, licensing, hardware, and processing location meet your requirements.

The [static chooser](site/index.html) is generated with `python3 scripts/run_field_guide.py build`; it requires no service or client-side JavaScript.

## Field Guide PRs

Contribute a fixture edge case, a fair new adapter, a correction, or a new task
card via a [good first issue](https://github.com/shivamnegi92/awesome-entity-extraction/issues?q=is%3Aissue+is%3Aopen+label%3Agood-first-issue),
[task-card issue](https://github.com/shivamnegi92/awesome-entity-extraction/issues?q=is%3Aissue+is%3Aopen+label%3Atask-card),
or direct PR. Never submit real user text or personal, customer, or health data.


- [Custom-label NER on short text](tasks/custom-ner/README.md) — fixture,
  annotation policy, strict/overlap span-type metrics, and a recorded spaCy run.
- [Synthetic PII redaction](tasks/pii-redaction/README.md) — exact-string
  residual checks, safety caveats, and a recorded Presidio run; not a privacy
  certification.

Fixtures and annotation rules are versioned independently. Please propose a
new task or correction using the [example idea form](https://github.com/shivamnegi92/awesome-entity-extraction/issues/new?template=example_idea.md).
Do not submit private text or real personal/health/customer data.

## Offline development commands

Run from the repository root; these checks require only Python's standard library:

```bash
python3 scripts/run_field_guide.py validate --runs
python3 -m unittest discover -s tests -v
python3 scripts/run_field_guide.py build
```

The `build` command writes `field_guide/site/index.html` and refreshes
`field_guide/results/report.json`. It reads only recorded outputs; it never
downloads models, calls APIs, or fabricates missing results. With no recorded
run, task status is `not_run`.

To score a previously produced prediction file (no inference is performed):

```bash
python3 scripts/run_field_guide.py score custom-ner path/to/predictions.json
python3 scripts/run_field_guide.py score pii-redaction path/to/redacted-outputs.json
```

Prediction schemas are shown by each task's `prediction.schema.json` and enforced by the
offline tests. Candidate outputs must include exactly one result per fixture
case; missing cases are errors, not silently excluded from metrics.

## Adding a task card

Task cards are discovered from `tasks/<id>/fixture.json`; no script edits needed.
A card needs `README.md`, `fixture.json`, `annotation.md`, and
`prediction.schema.json`. The fixture's `"metric"` key picks a scorer from
[`metrics/`](metrics/__init__.py) (`spans` or `pii_residual` today). A new kind of
task (for example, table cells or entity-resolution pairs) adds one metric module
with `validate_fixture`, `validate_predictions`, and `score`, plus one line in
`METRICS`. Existing metrics don't change.

## Current run status

| Task card | Recorded run | Headline | Write-up |
|---|---|---|---|
| custom-ner | spaCy 3.8.7 + `en_core_web_sm` 3.8.0 | Strict F1 0.636; boundaries all right, 4 type errors | [NOTES](results/custom-ner/spacy-3.8.7-en_core_web_sm-3.8.0/NOTES.md) |
| custom-ner | GLiNER multi v2.1 | **not run** (weights download blocked on the recording network) | issue #9 |
| pii-redaction | Presidio 2.2.358 defaults + `en_core_web_lg` 3.8.0 | 3 of 6 sensitive values left; `.test` emails rejected by TLD validation | [NOTES](results/pii-redaction/presidio-2.2.358-en_core_web_lg-3.8.0/NOTES.md) |

Runs were recorded by the maintainers and haven't been independently reproduced
yet. That reproduction is the most useful next contribution: see
[`adapters/README.md`](adapters/README.md) for exact commands and model checksums.
