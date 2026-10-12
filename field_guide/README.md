# Entity Extraction Field Guide (prototype)

A small decision-and-evidence companion to the catalog. It helps narrow a
starting approach and defines two versioned, synthetic task cards. It is **not**
a benchmark leaderboard: no model outputs have been run or scored in the checked-in
prototype, and a tiny fixture cannot estimate production accuracy.

## Choose a starting point

The maintained machine-readable version is [`decision_matrix.json`](decision_matrix.json).
This table is its quick human-readable summary; confirm model, API, license, and
system requirements at the linked source before adoption.

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
  annotation policy, strict/overlap span-type metrics, and explicit not-run status.
- [Synthetic PII redaction](tasks/pii-redaction/README.md) — exact-string
  residual checks and safety caveats; not a privacy certification.

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

Prediction schemas are shown by `field_guide/evaluate.py` and enforced by the
offline tests. Candidate outputs must include exactly one result per fixture
case; missing cases are errors, not silently excluded from metrics.

## Current run status

**No model/provider outputs are published yet.** The fixtures, schemas, checks,
and evaluator are implemented; they are not evidence that any extractor passed.
The next step is to run a small, declared candidate set in isolated environments,
record manifests/raw outputs, and get independent review before publishing scores.
