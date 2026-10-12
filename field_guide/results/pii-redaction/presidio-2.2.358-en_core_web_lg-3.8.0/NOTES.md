# Run notes: Presidio 2.2.358 defaults on pii-redaction v1.0.0

Recorded 2026-10-12 · Darwin arm64 · Python 3.12 · CPU · offline inference ·
`en_core_web_lg` 3.8.0 on spaCy 3.8.7. Reproduce with
[`field_guide/adapters/README.md`](../../../adapters/README.md).

## Result

| Metric | Value |
|---|---|
| Sensitive values expected | 6 |
| Still present after redaction | **3 (residual rate 0.5)** |
| False redactions on no-PII cases | 1 ("this morning" became `<DATE_TIME>`) |

**Six synthetic cases. This is not a privacy assessment** of Presidio or of
any real deployment.

## What happened

| Case | Redacted output | Notes |
|---|---|---|
| contact-001 | `<PERSON> at <URL>e@example.test or call <PHONE_NUMBER>.` | Name and phone removed. The email was **mangled, not detected**: a `URL` hit on `alex.do` replaced part of it. The exact-string check passes, but `e@example.test` still leaks most of the address. |
| unicode-002 | *(unchanged)* | Missed both `Zoë Example` and `zoe@example.test`. |
| repeat-003 | *(unchanged)* | Missed both copies of `repeat@example.test`. |
| digits-negative-004 | *(unchanged)* | Correct: no false redaction of quantities. |
| ambiguous-005 | *(unchanged)* | Extension `2048` kept. Per the annotation policy this is a review case, not a miss. |
| empty-006 | `The delivery arrived <DATE_TIME>.` | **False redaction**: Presidio treats `DATE_TIME` as PII by default. |

## Root cause of the email misses (checked, not guessed)

Presidio's email recognizer validates the top-level domain, and `.test`
isn't a public suffix. The same sentences with `example.com` addresses are
detected (`EMAIL_ADDRESS`, score 1.0). So these misses are **mostly an
artifact of the fixture**: `.test` is reserved for testing (RFC 2606), which
is exactly why the fixture used it.

The finding still matters in practice: internal or non-public domains
(`.local`, `.corp`, `.internal`) aren't recognized as email addresses by
the default configuration.

## Follow-ups (not done in this run)

- The exact-string residual metric missed the partial leak in contact-001.
  A partial-overlap residual check would catch it. That's a metric change,
  so it needs its own PR and a note in the task card.
- Fixture v1.1 could add one public-suffix email so the card separates
  "email recognizer works" from "unusual TLD is rejected". That needs a
  version bump per `annotation.md`.
- A configured run (for example, removing `DATE_TIME` from the entities to
  redact) should be recorded as a **separate** run, not an edit to this one.
