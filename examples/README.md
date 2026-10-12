# Runnable Examples

Independent, end-to-end entity-extraction examples. Each directory has its
own `README.md`, `main.py`, pinned `requirements.txt`, and `example.json`
metadata; no example imports another. Pick a use case from the table (generated
from the `example.json` files), then follow that directory's setup instructions.
These are small teaching demos, not production-ready extractors.

<!-- BEGIN GENERATED EXAMPLES INDEX: edit example.json files, then run scripts/check-examples.py --write -->

| # | Example | Stack | What it demonstrates | Needs |
|---|---------|-------|----------------------|-------|
| 1 | [General NER](01-spacy-ner/README.md) | spaCy | People, organizations, locations, dates, and source offsets | model download |
| 2 | [Zero-shot custom NER](02-gliner-zero-shot/README.md) | GLiNER | Caller-defined entity labels and grounded spans | model download |
| 3 | [Typed structured extraction](03-instructor-structured/README.md) | Instructor + OpenAI API | Validated business fields from free text; API key and possible charges | API key, network |
| 4 | [PII redaction](04-presidio-pii/README.md) | Presidio | Detect and redact synthetic contact details | model download |
| 5 | [Relation triples](05-rebel-relations/README.md) | REBEL | Subject–relation–object extraction; large model download | model download |
| 6 | [Invoice fields](06-invoice-pdf/README.md) | pdfplumber | Generate and parse a synthetic text PDF; no OCR | none |
| 7 | [Multilingual NER](07-stanza-multilingual/README.md) | Stanza | English, Spanish, and French entity recognition | model download |
| 8 | [Dates and quantities](08-temporal-quantity/README.md) | dateparser + quantulum3 | Normalize a relative date and extract measurements | none |
| 9 | [Biomedical entities](09-scispacy-biomedical/README.md) | scispaCy | Extract disease/chemical mentions from synthetic text | model download |
| 10 | [Entity linking](10-wikidata-linking/README.md) | Wikidata API | Resolve a contextual mention to canonical knowledge-base candidates | network |

<!-- END GENERATED EXAMPLES INDEX -->

See the [Extraction Field Guide](../field_guide/README.md) for a constraint-based
shortlist and two versioned, synthetic task cards. Its current task-card status
is explicitly `not_run`; it does not publish model scores until outputs are
reproducibly recorded.

Want to help make the examples better? Pick a [good first issue](https://github.com/shivamnegi92/awesome-entity-extraction/issues?q=is%3Aissue+is%3Aopen+label%3Agood-first-issue), propose a [new task card](https://github.com/shivamnegi92/awesome-entity-extraction/issues?q=is%3Aissue+is%3Aopen+label%3Atask-card), or improve one of these examples. A starter PR does not need a prior issue.


## Run one example

Choose a directory and follow its `README.md`; for example:

```bash
cd examples/06-invoice-pdf
uv venv --python 3.12 .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com -r requirements.txt
python main.py
```

Each environment is independent. Model-based examples may download models on
first run; the Instructor example may incur API charges; the Wikidata example
requires internet. Do not use real personal, customer, or health data.

See [PLAN.md](PLAN.md) for the portfolio rationale and quality bar. For the
catalog of tools, models, and datasets, see the [main list](../README.md).
