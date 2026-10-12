# Run notes: spaCy `en_core_web_sm` 3.8.0 on custom-ner v1.0.0

Recorded 2026-10-12 · Darwin arm64 · Python 3.12 · CPU · offline inference.
Reproduce with [`field_guide/adapters/README.md`](../../../adapters/README.md).

## Result

| Metric | Value |
|---|---|
| Strict span+type F1 | 0.636 (7 TP, 4 FP, 4 FN) |
| Overlap span+type F1 | 0.636 (identical: every error is a **type** error, none are boundary errors) |
| Raw predictions dropped by label policy | 2 (`DATE` for "next week" and "yesterday") |

**Six synthetic sentences. This is a description of behaviour, not an accuracy
estimate.** Don't quote the F1 out of context.

## What went wrong, case by case

| Case | Gold | spaCy said | Kind of error |
|---|---|---|---|
| news-001 | Northstar Labs = `ORG` | `PERSON` | Unseen company name read as a person |
| product-002 | Aster Phone 4 = `PRODUCT` | `PERSON` | Unseen product read as a person |
| unicode-004 | Café North = `ORG` | `PERSON` | Unseen business name read as a person |
| abbrev-005 | J. Rivera = `PERSON` | `ORG` | Initial + surname read as an organization |

Correct: all three `GPE` cities, `Maya Chen` and `Zoë` as `PERSON`,
`U.N. House` as `ORG`, and **no false positives** on the two negative cases
(the fruit "apple", and the empty sentence once `DATE` is excluded). Every
predicted span boundary matched the gold boundary exactly, including
`J. Rivera`, whose only error was its type.

## What this tells a reader

- **Boundaries were fine; labels were the problem.** Unicode offsets
  (`Zoë`, `Café North`, `Montréal`) came out exactly right. The small model
  finds spans but guesses types for names it hasn't seen, defaulting to
  `PERSON`.
- **The custom `PRODUCT` label is the decision this card exists for.** spaCy's
  label set includes `PRODUCT`, but the small model didn't use it for a
  made-up product name. If you need reliable custom or rare types, this is the
  evidence for trying GLiNER or fine-tuning, not for assuming the label works.
- This run doesn't say how spaCy compares with GLiNER: there's no GLiNER run
  yet (see "Not recorded" below).

## Label policy

Fixed before running: keep a spaCy label only if it equals a fixture label
(`PERSON`, `ORG`, `GPE`, `PRODUCT`). No remapping (`LOC`, `FAC`, and `NORP`
aren't turned into `GPE`/`ORG`). Everything else is kept in
[`raw_predictions.json`](raw_predictions.json).

## Not recorded

The GLiNER candidate (`urchade/gliner_multi-v2.1`) wasn't run. From the
recording network, the Hugging Face API and small files download fine, but
the 1.16 GB weights file redirects to a CDN that the corporate proxy rejects
(HTTP 407). That's an environment limit, not a GLiNER result. Issue #9 stays
open for someone to record it.
