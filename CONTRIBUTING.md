# Contributing to Awesome Entity Extraction

Thanks for helping make entity extraction easier to learn and use. Contributions
are welcome from first-timers, practitioners, researchers, and project maintainers.
You can start small: fix a broken link, improve an explanation, add a useful
resource, or contribute a standalone example. No need to ask permission first.

**Good first contribution:** [report a broken or stale item](https://github.com/shivamnegi92/awesome-entity-extraction/issues/new/choose),
[propose an example](https://github.com/shivamnegi92/awesome-entity-extraction/issues/new?template=example_idea.md),
or [open a pull request](https://github.com/shivamnegi92/awesome-entity-extraction/compare).

## What belongs here

This is a practitioner-first map of maintained tools, models, datasets, and
learning material for extracting entities, relations, and structured data from
text and documents. The main README is the catalog; `examples/` contains
independent runnable demonstrations, not a shared library.

## Resource entry checklist

Before proposing an item, check that it is not already listed and that it:

1. **Is real, relevant, and maintained.** Link to a working project, model,
   dataset, or learning resource. Prefer usable software and maintained resources;
   don't add paper-only entries unless the resource itself is a benchmark/dataset.
2. **Deserves this list.** It must materially support entity, relation, or
   structured-data extraction from text/documents. General LLM frameworks belong
   only when extraction is a first-class use case.
3. **Has a factual one-line description.** Say what it does, not how amazing it
   is. Use: `- [Name](https://link) - What it does.`
4. **Is under the right heading.** Choose the primary use case; a maintainer can
   tidy ordering and placement.
5. **Has a verified source.** Use the canonical project/model/dataset page where
   possible. Do not claim performance without linking evidence.

## Add or improve a runnable example

Examples live in independent folders under `examples/`. Each example should have
its own `README.md`, `main.py`, and `requirements.txt`, and should work without
installing another example's dependencies. Keep input synthetic; never commit
personal, customer, or health data, API keys, or credentials.

An example contribution should include:

- A distinct use case represented in this catalog (not another generic NER
  wrapper).
- Copyable setup/run commands, dependency versions, model/API requirements, and
  clear notes on cost, downloads, and limitations.
- A complete small path from sample input to inspectable output and a useful
  assertion/check where practical.
- A note on expected output and how the demo can fail or be wrong.

If you want to contribute an idea before coding, use the [example idea form](https://github.com/shivamnegi92/awesome-entity-extraction/issues/new?template=example_idea.md).

## Send a pull request

1. Fork this repository and create a focused branch.
2. Make the smallest complete change; update the index/docs when needed.
3. Run the applicable checks from the repository root:

   ```bash
   python3 scripts/check-examples.py
   python3 -m compileall -q examples scripts
   npx --yes awesome-lint README.md
   python3 scripts/check-links.py
   ```

   Link checks require network access; CI also runs them. Model inference/API
   checks may require downloads, credentials, or paid services—document when you
   could not run them. Never paste credentials into issues, PRs, or logs.
4. Open a PR with a short summary, motivation/use case, test results, and any
   limitations or follow-up. The PR template is a checklist, not a gatekeeping
   quiz. Maintainers may suggest edits or ask for evidence before merging.

You can contribute directly with a PR; opening an issue first is optional.

## Review principles

We review for relevance, maintainability, accurate descriptions, working links,
reproducible instructions, safe synthetic data, and a distinct user benefit.
Quality beats entry count. A respectful correction is welcome even if the
suggested change is ultimately not accepted.

## What we usually cannot accept

- Dead links, unsupported claims, or projects with no evidence of continued
  maintenance (unless historical context is the point).
- Pure promotion, duplicate entries, or generic tools without a clear extraction
  use case.
- Credentials, private/customer data, or examples that misrepresent model output.
