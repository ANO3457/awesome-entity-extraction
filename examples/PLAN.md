# Plan: 10 Independent End-to-End Entity Extraction Examples

> **Status:** Implemented. Each example now lives in a numbered standalone
> directory with its own `README.md`, `main.py`, and pinned `requirements.txt`.
> Use [README.md](README.md) as the runnable index. The original roadmap below
> is retained as rationale and acceptance criteria.

## Goal

Grow this repository's `examples/` from the original four short snippets into ten small,
copy-and-run demonstrations of distinct entity-extraction use cases represented
in the catalog. A reader should be able to choose one example, install only its
requirements, run it independently, and understand both the extracted result and
its limitations.

This is a plan, not a shared framework proposal. Keep each example self-contained:
no common runtime package, service, database, credentials file, or required setup
from another example. Reuse a consistent *presentation contract* (clear setup,
input, extraction, normalized output, and checks), not shared implementation.

## Design rules

1. **One use case per example.** Don't make ten wrappers around generic NER.
2. **Standalone means standalone.** Each script explains its own installation,
   model download or credential setup, input, and run command. It must not import
   another example or rely on files produced by one.
3. **Show the whole small workflow.** Go from an included, synthetic input to
   extraction and readable output; include a minimal assertion or validation
   where meaningful. No private/customer data or network-dependent input files.
4. **Make costs and limits visible.** Call out model downloads, API keys/API
   charges, CPU/GPU expectations, OCR assumptions, language coverage, and
   confidence/accuracy caveats in the docstring and README row.
5. **Safe, honest outputs.** Do not imply predictions are ground truth. Keep
   secrets out of source; avoid logging sensitive text in the PII example. For
   the optional hosted-LLM example, document the provider/model and API cost, and
   keep the provider/model configurable without making a Chinese-origin model a
   default or fallback.
6. **Keep the examples lightweight.** Each file should be short enough to read
   in one sitting. Use synthetic fixtures and standard output; don't add a web
   app, service, framework, or giant sample corpus.
7. **Check reproducibility.** Pin tested dependency versions in each example's
   setup instructions (or a tiny per-example requirements file if inline pins
   become unwieldy). Record the Python-version target and model identifier.

## Proposed ten-example portfolio

## Portfolio rationale
| 1 | `01-spacy-ner/` | General English news-style sentence | spaCy pretrained NER | Print typed spans with offsets; assert expected person, organization, and location spans are present. Explain that the small English model is a baseline, not open-vocabulary NER. |
| 2 | `02-gliner-zero-shot/` | Custom business sentence and caller-defined labels | GLiNER zero-shot | Print label, exact text, offsets, and score; assert returned spans lie within the source text. Make clear labels are prompt-like input and scores are not calibrated probabilities. |
| 3 | `03-instructor-structured/` | Short unstructured business note | Instructor + Pydantic structured output | Validate a typed record, serialize JSON, and check required fields/types. Clearly identify API setup, provider/model, possible cost, and non-determinism. Keep this an opt-in network example. |
| 4 | `04-presidio-pii/` | Synthetic contact message containing PII | Presidio analyzer + anonymizer | Show detected entity types and a redacted string; assert known synthetic values do not remain in the redacted output. Never use real personal data or print unredacted input by default. |
| 5 | `05-rebel-relations/` | Two-sentence news snippet with an explicit subject/action/object relation | REBEL, listed under Relation and Knowledge Extraction | Extract and display subject–relation–object triples; validate triple structure and show source sentence. Note model download/runtime and that generated relations need review. |
| 6 | `06-invoice-pdf/` | Locally generated synthetic text-based invoice PDF | pdfplumber plus transparent extraction/normalization rules | Extract vendor, invoice number, date, and total into a JSON record; assert a known total and explain that this text-PDF demo does not handle scanned-image OCR. |
| 7 | `07-stanza-multilingual/` | One short sentence in English, Spanish, and French | Stanza multilingual NER | Download documented language models, run each sentence, and print language-tagged spans. Declare downloads; quality varies by language. |
| 8 | `08-temporal-quantity/` | Scheduling/operations note with a relative date, duration, and measurement | dateparser + quantulum3 | Normalize the date against an explicit reference date and extract quantities/units; explain locale, ambiguity, and unit-normalization limits. |
| 9 | `09-scispacy-biomedical/` | Synthetic, non-patient biomedical sentence | scispaCy | Extract and print recognized biomedical spans/types; assert spans are source-grounded. State model install, availability, and that this is not clinical advice or PHI processing guidance. |
| 10 | `10-wikidata-linking/` | Ambiguous mention in a short context (e.g. “Jordan” in a basketball context) | Wikidata public search API (an intentionally lightweight entity-linking alternative to the catalog's ReFinED model) | Resolve a mention to canonical candidates and IDs; validate returned IDs and disclose network, ambiguity, and ranking limitations. |

## Portfolio note

This plan is implemented with a Wikidata API candidate-linking demo instead of
the originally proposed ReFinED model download. It demonstrates candidate
retrieval and a transparent keyword-ranking heuristic, not full context-aware
ReFinED entity linking.


## Standard shape for each script

Each example should remain one direct entry point with a `main()` and a
`if __name__ == "__main__": main()` guard. It should contain:

1. A module docstring with a one-line purpose, tested Python version, exact
   install/model-download commands, run command, and any network/API caveat.
2. A tiny synthetic, inline input (except where a tiny local fixture is essential
   to demonstrate a document workflow).
3. The narrowest useful extraction call, with settings/model ID explicit.
4. A normalized, readable output (JSON is preferred for structured records;
   spans should include text, type, and character offsets when the library makes
   those available).
5. One or more deterministic sanity checks against the fixture. Avoid assertions
   that depend on unstable model wording, ordering, confidence scores, or
   environment-specific model behavior.
6. A short comment or README note on what the example does **not** solve.

The sample should fail with an actionable message when a required model, API key,
or optional file is missing. Do not silently download very large models during
an unexplained first run.

This roadmap was implemented as ten numbered standalone folders. Each includes
an independent `README.md`, `main.py`, and pinned `requirements.txt`; the
existing top-level example snippets were moved into folders 01–04 to avoid
maintaining two versions. The folder index in `examples/README.md` is the
canonical run guide.

### Implementation Sequence (Completed)

#### Phase 1 — Scope and feasibility

- Kept the ten use cases aligned with tools/catalog sections from the repository.
- Replaced the planned ReFinED heavyweight model demo with a small Wikidata API candidate-linking example so the use case remains standalone and runnable with a small dependency. This is a simple contextual ranking baseline, not ReFinED.
- Generated the invoice PDF from synthetic source text at runtime; no binary fixture or external input is needed.

#### Phase 2 — Upgrade the original examples

- Moved the original snippets into example folders and upgraded their setup/output/validation contract.
- Kept each example independently runnable without a shared framework or runtime package.
- Kept hosted LLM use opt-in and PII output redacted by default.

#### Phase 3 — Add distinct examples

- Added temporal/numeric parsing, relation extraction, generated-PDF parsing, multilingual NER, biomedical extraction, and Wikidata candidate linking.
- Kept each example installation isolated using its own pinned requirements file.

#### Phase 4 — Document and verify

- Added a ten-row `examples/README.md` index and a separate setup README in each example folder.
- Added `scripts/check-examples.py` for offline structural verification; it does not download models or call paid APIs.
- Ran syntax compilation and the offline structural checker successfully. Could not run full dependency/model/API end-to-end checks because packages are not installed and outbound network access is unavailable in this environment. The documented `uv venv --python 3.12 .venv` setup was verified.
- Ran awesome-lint successfully. Link checking was attempted but blocked by unavailable DNS and local certificate verification. Inputs are synthetic and no credentials/fixture PDFs are committed.

## Definition of done

- Exactly ten distinct examples are listed in `examples/README.md` and each
  corresponds to a real use case represented in the main catalog.
- Every example can be selected and run on its own using its documented setup;
  no example depends on another example's output or a hidden local file.
- Every script performs input → extraction → inspectable output, with a useful
  sanity check where deterministic behavior permits.
- Inputs are synthetic/public-domain-safe; no secrets or personal data are
  committed. External API usage, model downloads, and important limitations are
  disclosed before the run command.
- The examples remain small teaching artifacts, not a second extraction
  framework. Existing repository lint/link checks continue to pass.
