# Task card: synthetic contact-text PII redaction

## Decision this card supports

When a short English contact note must be processed locally, does the configured
Presidio analyzer/anonymizer remove the synthetic email, phone, and person
values in this fixture without printing the raw input?

## Fixture and policy

`fixture.json` is synthetic and contains six cases: common contact data,
Unicode name, repeated email, harmless digit strings, partial identifiers, and
an empty/no-PII case. It is a teaching fixture, not a realistic prevalence
sample. The expected `sensitive_values` are exact strings to check for residual
leakage; `expected_types` describe entities expected to be recognized. See
`annotation.md` for policy and limitations.

## Candidate

- **Microsoft Presidio Analyzer + Anonymizer:** configurable local PII detection
  and replacement; the example pins its Python packages and spaCy model
  requirements.

`prediction.schema.json` defines the safe output envelope. To add a run, place a
schema-conforming `predictions.json` under
`field_guide/results/pii-redaction/<tool>-<version>/`; only redacted output is
recorded, never original source. The `run` object is the manifest and records
tool/model version, fixture version, UTC date, environment, and status.

## Metrics

- **Sensitive-value residual rate:** number of expected sensitive strings that
  remain after redaction divided by all expected sensitive strings in cases
  where the recognizer should find them. Lower is better, but six synthetic
  cases are not a privacy guarantee.
- **Expected type coverage:** expected entity types observed in the supplied
  recorded output. This does not measure false positives on a representative
  distribution.
- **False-redaction review:** inspect the digit-only negative and no-PII case.
  A redacted output can be safe from one exact string and still be unusable.

## Recorded runs

| Run | Residual values | Notes |
|---|---|---|
| [Presidio 2.2.358 defaults, `en_core_web_lg` 3.8.0](../../results/pii-redaction/presidio-2.2.358-en_core_web_lg-3.8.0/NOTES.md) | 3 of 6 | Missed `.test` emails because of TLD validation (checked: the same text with `.com` is detected). One email partially leaked through a `URL` hit. One false `DATE_TIME` redaction. |

Record new runs with an adapter in [`field_guide/adapters/`](../../adapters/README.md).
A task with no recorded run must show as `not_run`, never as zero or a pass.

## Reproduce and safety

Run the field-guide offline validation from repo root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/run_field_guide.py validate --runs
```

Never replace synthetic fixture values with personal, customer, or health data.
A passing exact-string check does not establish regulatory compliance, complete
PII detection, or safety for production use.
