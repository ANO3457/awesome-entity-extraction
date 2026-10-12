# Scope Expansion Plan

> Goal: grow from "entity extraction catalog + 10 examples + 2 task cards" into
> the practitioner reference for **getting structured data out of unstructured
> inputs, with evidence**: across tasks, input types, languages, and the full
> lifecycle from labeling to monitoring.
>
> This plan sits under [GROWTH_PLAN.md](GROWTH_PLAN.md). Its "Expand only if"
> gates still apply. More scope is a cost, not a goal: every new area has to
> answer a real reader question that the current repo can't.

---

## 1. Where the repo is today (2026-10)

| Asset | State | Limit on growth |
|---|---|---|
| Curated catalog (`README.md`) | ~16 sections, awesome-lint clean | Flat list; no machine-readable metadata (license, local/hosted, languages, last checked) |
| Standalone examples | 10 independent folders | `scripts/check-examples.py` hardcodes exactly 10; an 11th would fail CI |
| Field Guide | 2 synthetic task cards (custom NER, PII), both `not_run` | No recorded runs yet; scoring only covers spans and PII residuals |
| Decision data | `field_guide/decision_matrix.json` **and** `field_guide/tasks/index.json` | Same 6 scenarios kept in two files (DRY violation); every new scenario has to be written twice |
| Community | 5 scoped open issues (#6–#10), Discussions on | No merged outside contributions yet |

**Implication:** Wave 0 below is required. Expanding before fixing the
duplicated matrix and the hardcoded count just piles up debt.

---

## 2. Expansion axes

Scope can grow along six independent axes. Each wave below picks a few cells,
not all of them.

| Axis | Today | Expansion target |
|---|---|---|
| **Task** | NER, PII, relations, linking, temporal, biomedical, invoice fields | + events, nested/overlapping spans, entity resolution, attribute/value, key-value forms, tables, slot filling, geoparsing, security IOCs |
| **Input type** | Plain text, text PDF | + scanned images/OCR, HTML/web pages, chat/email threads, ASR transcripts, spreadsheets |
| **Lifecycle** | Inference only | + annotation → weak supervision → fine-tuning → evaluation → serving → monitoring/drift → human review |
| **Language** | English-heavy + one Stanza example | + documented multilingual coverage, script/tokenization edge cases, low-resource notes |
| **Ecosystem** | Python only | + JS/TS, JVM (Spark NLP/CoreNLP), Rust/CLI where real tools exist |
| **Audience** | Practitioners | + researchers (dataset/metric map), educators (learning path) |

---

## 3. Non-negotiable rules for any new scope

1. **One reader question per addition.** Every new example/task card says which
   decision it helps someone make ("Should I use rules or a model for X under
   constraint Y?").
2. **Synthetic or clearly redistributable data only.** No customer, health,
   HR, or scraped personal data. Generate fixtures at runtime where possible
   (the invoice example already does this).
3. **No unrun claims.** Results stay `not_run` until reproduced, with a manifest
   (versions, commit, hardware, date).
4. **Isolation stays.** Every example keeps its own `README.md`, `main.py`,
   pinned `requirements.txt`, and no cross-example imports.
5. **Model-origin policy.** Don't add Chinese-origin models or derivatives
   (Qwen, DeepSeek, GLM, Yi, Baichuan, InternLM, MiniCPM, Kimi, Hunyuan, and
   similar), including fine-tunes built on them, to examples or task-card
   candidates. If a model's base is unclear, ask before adding it. OK examples:
   Llama, Phi, Gemma, Mistral, Nemotron, OLMo, ModernBERT/DeBERTa encoders.
6. **Bounded maintenance.** Each wave lists its CI cost. Anything needing GPUs
   or paid APIs runs manually or on a schedule, never on every PR.
7. **No competitor-pricing or assortment scrapers** as examples, even as
   "web extraction" demos. Web examples use synthetic local HTML.

---

## 4. Waves

Each wave has a **gate**. Don't start a wave until the previous gate passes.

### Wave 0: Fix the foundation (1 week, required)

Pay off the structural debt so that adding item N+1 costs one folder, not five
edits.

| # | Deliverable | Acceptance |
|---|---|---|
| 0.1 | **Single decision source.** Merge `tasks/index.json` into `decision_matrix.json` (or generate one from the other). | One file defines scenarios; chooser + tests read only it; test fails if a duplicate appears |
| 0.2 | **Registry-driven examples.** Each example gets an `example.json` (`id`, `title`, `task`, `input_type`, `local`, `needs_api_key`, `needs_gpu`, `languages`, `models`, `model_origin`). `check-examples.py` discovers folders instead of hardcoding 10. | Adding `11-*` with valid metadata passes CI with no script edits; missing/invalid metadata fails with a clear error |
| 0.3 | **Generated examples index.** `examples/README.md` table generated from `example.json` files. | CI fails if the generated index is stale |
| 0.4 | **Catalog metadata sidecar.** `catalog/entries.yaml` with `name`, `url`, `section`, `license`, `deployment` (local/hosted/both), `languages`, `last_checked`. Hand-write the first slice (Document & Layout, which pairs with issue #10). | Schema-validated in CI; README stays hand-written for now (don't auto-generate the awesome list yet; YAGNI) |
| 0.5 | **Model-origin audit.** Review catalog and example models against rule 3.5. | Non-compliant entries removed or flagged with rationale. Starts with NuExtract 2.0 (likely Qwen2.5-VL-based, so verify then remove) |
| 0.6 | **Generalize the scorer.** Split `field_guide/evaluate.py` into metric plugins (`spans`, `pii_residual`, plus new ones later) behind one interface. | Existing 10 tests pass unchanged; adding a metric doesn't change other metrics' code |

**Gate 0:** CI green; adding a dummy 11th example and a dummy scenario each
touch exactly one location.

---

### Wave 1: Deepen what exists (2–3 weeks)

Before going wider, make current scope trustworthy. These are mostly the open
issues already filed.

| # | Deliverable | Ties to |
|---|---|---|
| 1.1 | First recorded reproducible run (spaCy or GLiNER on custom-NER card) | #9 |
| 1.2 | Document OCR/layout task card (synthetic, generated at runtime) | #6 |
| 1.3 | Multilingual NER card with Unicode/script edge cases | #8 |
| 1.4 | Reader-scenario validation of the chooser (3–5 real people) | #7 |
| 1.5 | Document & Layout catalog freshness audit, written into `catalog/entries.yaml` | #10, 0.4 |
| 1.6 | **Failure gallery** per existing example: 3–5 realistic misses each (wrong type, boundary error, hallucinated field, missed PII), committed as fixtures | New |

**Gate 1 (the GROWTH_PLAN expand gate):** at least one independent
reproduction or correction merged, **and** at least one real reader decision
documented in #7 or Discussions. If this gate fails twice, stop expanding and
put the effort into curation quality.

---

### Wave 2: New extraction tasks (4–6 weeks)

Ten new standalone examples (`11`–`20`), each aimed at a task the current
examples don't cover. Same contract as `01`–`10`.

| ID | Example | Reader decision it supports | Candidate stack (verify origin + license first) | Data |
|---|---|---|---|---|
| 11 | `11-event-extraction` | "Can I pull who-did-what-when events, or only entities?" | Event schema with Pydantic + local encoder or rules baseline | Synthetic news-style sentences |
| 12 | `12-nested-spans` | "My entities overlap (e.g. *Bank of America Tower*). What handles that?" | spaCy `spancat` vs flat NER, side by side | Synthetic, with gold nested spans |
| 13 | `13-entity-resolution` | "Same company, five spellings: how do I dedupe?" | Splink or recordlinkage + normalization rules | Synthetic company/vendor list |
| 14 | `14-product-attributes` | "Extract brand/size/color/material from product titles" | Rules + GLiNER custom labels | Synthetic catalog titles (no scraped retailer data) |
| 15 | `15-form-key-value` | "Key-value pairs from forms with checkboxes" | Generated PDF form + pdfplumber/pypdf form fields vs layout heuristics | Runtime-generated synthetic form |
| 16 | `16-table-extraction` | "Tables in PDFs: when is camelot/pdfplumber enough?" | pdfplumber tables vs Camelot | Runtime-generated PDF with tricky merged cells |
| 17 | `17-conversation-slots` | "Slot filling from chat/support transcripts" | Rules + small encoder; handles speaker turns | Synthetic dialogue |
| 18 | `18-geoparsing` | "Turn place mentions into coordinates, with ambiguity" | spaCy GPE + offline gazetteer (GeoNames subset with license note) | Synthetic travel text with *Paris, TX* vs *Paris, FR* |
| 19 | `19-security-ioc` | "Pull IPs, hashes, CVEs, and domains from incident notes" | Regex + defanging/refanging + validation | Synthetic incident report (no real indicators) |
| 20 | `20-legal-clause-fields` | "Parties, dates, governing law from contracts" | Rules + structured-output LLM, compared on the same fixture | Synthetic contract text |

**Per-example acceptance:**
- `example.json` valid; offline syntax/structure checks pass
- README sections: *When to use / When not to / Setup / Run / Expected output / Known failures / Cost & privacy*
- At least 2 committed failure cases
- Runs on CPU in under ~2 minutes after install, or README says why not

**Field Guide additions in this wave (only where data is cheap to make):**
- `entity-resolution` task card (pairwise precision/recall/F1 metric plugin)
- `table-extraction` task card (cell-level exact match metric plugin)

**Gate 2:** at least 3 of the 10 new examples have an outside contributor
or reviewer, **and** issue/Discussion requests justify at least one more task area.

---

### Wave 3: Full lifecycle (4–6 weeks)

Readers don't just pick a model. They label, train, evaluate, ship, and watch
it drift. Add a `lifecycle/` track: **guides with small runnable demos**, not
production platforms.

| # | Guide | Runnable piece | Reader decision |
|---|---|---|---|
| 3.1 | **Annotation guidelines that work** | Template annotation policy + inter-annotator agreement script (Cohen's κ on spans) | "Are my labels consistent enough to train on?" |
| 3.2 | **Weak supervision / bootstrapping** | Labeling functions → noisy labels → small model, on synthetic data | "Can I avoid labeling 5,000 examples by hand?" |
| 3.3 | **Fine-tune a small encoder** | ModernBERT or DeBERTa token-classification on synthetic data, CPU-feasible | "When does fine-tuning beat zero-shot for me?" |
| 3.4 | **Evaluation beyond F1** | Per-type, boundary-vs-type error breakdown, confusion report; reuses Field Guide scorers | "Where exactly is my model failing?" |
| 3.5 | **Serving extraction** | Minimal FastAPI wrapper with schema validation and timeouts | "What breaks when I put this behind an API?" |
| 3.6 | **Monitoring and drift** | Label-distribution drift + "unknown entity rate" check over batches | "How do I know quality dropped in production?" |
| 3.7 | **Human-in-the-loop review** | Confidence-based routing to a review queue (static HTML) | "Which outputs should a person check?" |

**Gate 3:** lifecycle guides referenced from at least one Discussion or
external post, and CI cost still bounded (all lifecycle demos CPU-only and
smoke-tested offline).

---

### Wave 4: New input types (4–6 weeks)

| # | Input type | Deliverable | Key caveat to document |
|---|---|---|---|
| 4.1 | **HTML/web pages** | Boilerplate removal + extraction on synthetic local HTML (trafilatura-style), no live scraping | Respect robots/ToS; no competitor scrapers |
| 4.2 | **Email/chat threads** | Quote/signature stripping before NER | Quoted text causes duplicate entities |
| 4.3 | **ASR transcripts** | Synthetic transcript with disfluencies, number words, no casing | NER trained on cased text degrades on ASR output |
| 4.4 | **Spreadsheets/CSV with free-text columns** | Column-aware extraction + type normalization | Mixed types, header ambiguity |
| 4.5 | **Images via vision-language models** | One VLM example using a model that passes rule 3.5 (e.g. a Llama/Gemma/Phi vision variant) on a generated receipt image | Hallucinated fields; no grounding to pixels unless the model provides boxes |

**Gate 4:** each input type has a matching decision-matrix scenario, and
the chooser routes to it.

---

### Wave 5: Ecosystem and audience (ongoing, contributor-led)

| # | Deliverable | Notes |
|---|---|---|
| 5.1 | **JS/TS track** (`examples-js/`) | 2–3 examples (compromise/nlp.js NER, regex PII, structured LLM output with zod). Separate CI job |
| 5.2 | **JVM notes** | Spark NLP / CoreNLP pointers + one batch example if a contributor owns it |
| 5.3 | **Researcher map** | `field_guide/datasets.md`: task → public datasets → standard metric → license. Links only, no redistribution |
| 5.4 | **Learning path** | Ordered route through examples 01→20 + lifecycle guides, for workshops/courses |
| 5.5 | **Cost/latency cookbook** | How to measure (not claim) throughput and per-document cost honestly |

Only start a 5.x item when someone volunteers to maintain it. Orphaned
ecosystem tracks rot faster than anything else.

---

## 5. Target repository shape (after Wave 4)

```text
awesome-entity-extraction/
├── README.md                  # curated list (hand-written, awesome-lint clean)
├── catalog/
│   ├── entries.yaml           # machine-readable metadata (Wave 0.4)
│   └── schema.json
├── examples/                  # 01–20, each self-contained with example.json
├── lifecycle/                 # Wave 3 guides + small demos
├── field_guide/
│   ├── decision_matrix.json   # single source (Wave 0.1)
│   ├── metrics/               # pluggable scorers (Wave 0.6)
│   ├── tasks/                 # custom-ner, pii, ocr-layout, multilingual,
│   │                          # entity-resolution, table-extraction, ...
│   ├── datasets.md            # researcher map (Wave 5.3)
│   └── site/                  # generated static chooser
├── examples-js/               # Wave 5.1 (only if maintained)
└── scripts/                   # discovery-based checks, generators
```

---

## 6. CI and maintenance budget

| Check | Trigger | Cost |
|---|---|---|
| awesome-lint, catalog schema, `example.json` schema, generated-index freshness | Every PR | Seconds |
| Example structure + syntax + no cross-imports (discovery-based) | Every PR | Seconds |
| Field Guide fixtures + metric unit tests | Every PR | Seconds |
| Changed-example smoke run (install + run only the touched folder, CPU, no API keys) | PR, path-filtered | Minutes |
| Link check | Weekly + on README change | ~1 min |
| Full example sweep (all 20, model downloads) | Weekly scheduled / manual | Tens of minutes |
| API-key or GPU examples | Manual only, documented | Never on PRs |
| Catalog freshness (`last_checked` older than 180 days) | Monthly scheduled, opens an issue | Seconds |

Rule: if a wave would push per-PR CI past ~5 minutes, path-filter it or move it to a schedule.

---

## 7. Contributor issues to seed per wave

Open these only when their wave starts (a stale backlog looks abandoned):

- **Wave 0:** "Merge duplicate decision matrices", "Discovery-based example check", "Add `example.json` to examples 01–10" (one issue per 2–3 examples = good first issues), "Catalog metadata schema + Document slice".
- **Wave 2:** one issue per example `11`–`20` using the runnable-example template, labeled `example` + difficulty.
- **Wave 3:** one issue per lifecycle guide.
- **Wave 4:** one issue per input type.

Each issue lists: reader decision, data source plan, model-origin check,
acceptance criteria, and "comment before starting".

---

## 8. Explicitly out of scope

- A universal leaderboard or "best extraction model" ranking
- Hosting a SaaS, API, or annotation platform
- Redistributing datasets with unclear licenses
- Live web scraping examples, and especially competitor pricing/assortment scrapers
- Chinese-origin models or derivatives (rule 3.5)
- GPU-only examples without a CPU path or a clear "manual only" label
- Auto-generating the awesome-list README (revisit only if `catalog/entries.yaml` covers every section and stays current for 3+ months)

---

## 9. Success signals (not star counts)

| Signal | Target by end of Wave 2 |
|---|---|
| Independent reproductions/corrections merged | ≥ 3 |
| Outside contributors with merged PRs | ≥ 5 |
| Documented real reader decisions (Discussions/#7) | ≥ 5 |
| Task cards with at least one recorded run | ≥ 3 |
| Catalog entries with `last_checked` < 180 days | ≥ 50% |
| Examples with documented failure cases | 100% |

If these stall, shrink scope back to what readers actually use.

---

## 10. Next 10 actions

1. Verify NuExtract 2.0's base model; remove or flag it per rule 3.5.
2. Merge `field_guide/tasks/index.json` into `decision_matrix.json`; update chooser + tests.
3. Define `example.json` schema; add it to examples 01–10.
4. Rewrite `scripts/check-examples.py` to discover folders and validate `example.json`.
5. Generate `examples/README.md` index from metadata; add freshness check to CI.
6. Refactor `field_guide/evaluate.py` into metric plugins without changing results.
7. Create `catalog/schema.json` + first `entries.yaml` slice (Document & Layout).
8. Open Wave 0 issues (4–6, mostly good-first).
9. Push contributors toward #9 (first recorded run) as the top-priority Wave 1 item.
10. Review Gate 1 in ~3 weeks; decide whether Wave 2 starts or the focus shifts to quality.
