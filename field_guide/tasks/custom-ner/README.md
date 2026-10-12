# Task card: custom-label NER on short text

## Decision this card supports

When you need person/company/location spans and want to add a custom type such
as `product`, which local approach should you try first?

## Fixture

Synthetic, hand-authored texts; no personal or customer data. Fixture version
`1.0.0` is in `fixture.json`. It contains:

- A straightforward person/company/location example.
- A custom product label and punctuation/offset case.
- A hard negative where `Apple` is a fruit, not a company.
- A Unicode span case to expose byte/character offset mistakes.
- An abbreviation and a case with no entities.

Expected spans use half-open Python character offsets (`start` inclusive,
`end` exclusive). Annotation policy is in `annotation.md`. This tiny fixture
illustrates behavior; it is not statistically representative and must not be
used as a benchmark claim.

## Candidates in this first card

- **spaCy `en_core_web_sm`:** common-label baseline. Not designed for arbitrary
  user labels.
- **GLiNER `urchade/gliner_multi-v2.1`:** caller supplies labels at inference
  time. Larger model download; scores are not calibrated probabilities.

`prediction.schema.json` defines the output envelope. To add a recorded run,
place a schema-conforming `predictions.json` under
`field_guide/results/custom-ner/<tool>-<version>/`. Its `run` object is the
manifest; include fixture version, tool/model version, UTC date, environment, and
status. The report builder validates and scores it; it never runs inference.

## Metrics

- **Strict span+type F1:** exact match on `(start, end, label)`.
- **Overlap span+type F1:** same label and non-empty character overlap. This is
  a diagnostic only; it does not replace strict exact-match scoring.
- Also report per-case predictions and misses/false positives in
  `results/latest.json`; do not collapse this into a universal model ranking.

## Run status

| Run | Strict F1 | Notes |
|---|---|---|
| [spaCy 3.8.7, `en_core_web_sm` 3.8.0](../../results/custom-ner/spacy-3.8.7-en_core_web_sm-3.8.0/NOTES.md) | 0.636 | Every boundary right; all 4 errors are types. Unseen company and product names became `PERSON`, and `PRODUCT` was never used. |
| GLiNER `urchade/gliner_multi-v2.1` | not run | Weights download blocked on the recording network; open in issue #9. |

Six sentences describe behaviour; they don't estimate accuracy. A candidate with
no recorded run shows as `not_run`, never as zero or a pass. Add runs with an
adapter in [`field_guide/adapters/`](../../adapters/README.md).

## Reproduce

From the repository root, run the offline unit tests and field-guide validation:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/run_field_guide.py validate --runs
```

To run an actual extractor, follow one candidate's isolated example README;
model installation/download and runtime are separate from the offline evaluator.

## Limitations

- Five synthetic cases cannot estimate real-world accuracy.
- Language and domain coverage are not inferred from one fixture.
- This card does not compare latency, memory, cost, privacy compliance, or
  production robustness.
- Review the model's license, access terms, and model card before adoption.
- Add edge cases through a versioned fixture change with an explanation; do not
  alter expected annotations after observing predictions without recording why.
