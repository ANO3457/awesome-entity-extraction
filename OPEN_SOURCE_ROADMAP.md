# Open-source roadmap and contributor board

This is the maintained scope for community work. Each item should have one
owner, acceptance criteria, and a verification path before it is marked `help
wanted` or `good first issue`. GitHub Issues are the live board; this document is
the roadmap, not a second queue.

**Status snapshot (2026-10-12):** the repository has 1 star, 0 forks, Issues and
Discussions enabled, and no open issues before this roadmap was seeded. This is
an early project, so the aim is to create clear entry points and collect useful
feedback—not manufacture activity or promise that opening issues will cause
stars.

## The product promise

Help practitioners move from **task → candidate → runnable example → visible
trade-offs**. Keep the catalog factual. Keep Field Guide claims modest: its task
cards currently contain synthetic fixtures and scoring code, but no published
model runs. Do not add benchmark scores until they are reproducibly run and
reviewed.

## This month's focus

1. **Reader fit:** test the chooser with practitioners and collect where its
   recommendations are confusing or missing a constraint.
2. **Reproducibility:** get the first task card run manifests reviewed; separate
   verified evidence from not-run editorial suggestions.
3. **Practical coverage:** fill the highest-demand task gap (document OCR/layout,
   relation extraction, or multilingual coverage) with one useful contribution.
4. **Curation:** correct stale catalog links/claims using primary sources and
   document the verification path.

## Live contributor tasks

Use these as starting points, not locked assignments. Before starting, comment
on the linked issue so maintainers can avoid duplicate work. Direct PRs are also
welcome. For new proposals, use the resource or task-card issue forms.

| Issue | Task | Level | Good contribution looks like |
|---|---|---|---|
| [#7](https://github.com/shivamnegi92/awesome-entity-extraction/issues/7) | Validate Field Guide chooser with real reader scenarios | First contribution | Add 3–5 anonymized scenarios/observations, identify confusing recommendations, and propose evidence-backed changes; do not invent research. |
| [#6](https://github.com/shivamnegi92/awesome-entity-extraction/issues/6) | Add a synthetic document OCR/layout task card | Intermediate | Synthetic fixture + annotation policy + source-backed candidate choices + limitations; no giant dependencies or unrun claims. |
| [#8](https://github.com/shivamnegi92/awesome-entity-extraction/issues/8) | Expand multilingual NER examples with documented support | First contribution | Add scoped languages, synthetic examples, reviewed gold offsets, Unicode tests, and realistic caveats. |
| [#9](https://github.com/shivamnegi92/awesome-entity-extraction/issues/9) | Record one reproducible local NER run | Intermediate | Use the prediction schema, record environment/model/commit/date, validate outputs, preserve misses; no cross-hardware ranking. |
| [#10](https://github.com/shivamnegi92/awesome-entity-extraction/issues/10) | Audit Document/Layout catalog freshness | First contribution | Review 5–8 entries against canonical sources; distinguish dead URLs from bot blocks; propose evidence-backed edits. |


## How contributors can help

### Good first contributions

- Fix a confirmed broken link or stale factual description.
- Improve a confusing example README or add expected-output documentation.
- Add a single synthetic edge case with annotation rationale and tests.
- Test the decision matrix against a real scenario and report what did not fit.

### Larger contributions

- Propose a task card with fixture, annotation policy, schema, methodology, and
  safe test data.
- Add an extractor adapter only when its setup, licensing, outputs, and
  comparison conditions can be documented.
- Add an evaluator metric with unit tests and a short explanation of failure
  modes; do not call JSON validity factual accuracy.
- Expand a catalog section after checking project maintenance and canonical URLs.

## Contribution and review contract

1. Check existing issues/cards to prevent duplicate effort.
2. Make the smallest complete change and link to primary evidence.
3. For examples/cards, use synthetic or redistributable data only; never include
   secrets, personal data, customer material, or health information.
4. Label result status honestly: passed / failed / partial / not run. State
   model/API versions, network/credential needs, costs if known, and limitations.
5. Run the checks in `CONTRIBUTING.md`. Full model downloads and paid calls are
   not required for a docs/fixture PR.
6. Maintainers review for relevance, evidence, safe data, reproducibility, and
   readability. Review is collaborative; an issue is a starting point, not a
   promise that every proposal will be merged.

## Community spaces

- [Open contribution issues](https://github.com/shivamnegi92/awesome-entity-extraction/issues)
- [Good first issues](https://github.com/shivamnegi92/awesome-entity-extraction/issues?q=is%3Aissue+is%3Aopen+label%3Agood-first-issue)
- [Task-card proposals](https://github.com/shivamnegi92/awesome-entity-extraction/issues?q=is%3Aissue+is%3Aopen+label%3Atask-card)
- [Discussions](https://github.com/shivamnegi92/awesome-entity-extraction/discussions)
- [Contributor guide](CONTRIBUTING.md)

## How we will know this is improving

Review monthly: substantive external PRs, useful corrections, first-time
contributor experience, successful example/task-card reproductions, and reader
feedback. Track stars/forks as secondary context only. If issues receive no
responses, ask whether the tasks are compelling and clearly scoped before
opening more.
