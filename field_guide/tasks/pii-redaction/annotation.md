# Annotation policy: PII redaction fixture v1.0.0

All values are fictional test strings. `sensitive_values` records exact substrings
that must not appear in redacted output. It does not claim these are all possible
PII forms. `expected_types` captures the recognizer types expected from the
selected Presidio configuration; types can change with recognizer/model versions
and should be reviewed rather than silently treated as universal truth.

Cases include standard email/phone/person, Unicode names, repeated email,
non-sensitive digit sequences, a partial identifier that is intentionally
ambiguous, and no-PII text. Do not score case 5 as a definite PII miss: it exists
to prompt a documented human review. A fixture update requires a version bump,
reason for each gold change, and corresponding test update.
