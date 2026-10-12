# Annotation policy: custom-label NER fixture v1.0.0

## Scope

Annotate explicit named spans, not inferred facts. Labels are `PERSON`, `ORG`,
`GPE`, and custom `PRODUCT`. Do not annotate generic roles, pronouns, or
unanchored descriptions.

## Span convention

Offsets are Python Unicode code-point indexes into the exact `text` string.
Use half-open intervals `[start, end)`. The span must satisfy
`text[start:end] == surface`. Include internal whitespace in multi-token names;
exclude surrounding punctuation and possessive suffixes where separable.

## Disambiguation

- Label an organization only when the sentence context names the organization.
- The word `Apple` in a fruit context is not an organization.
- Annotate `PRODUCT` only for an explicitly named product in this fixture; do
  not infer product category from a generic noun.
- Annotate the written entity type, not a downstream canonical identity.

## Change control

Fixture changes require incrementing `version` in `fixture.json`, documenting
why each gold label/offset changed, and updating tests. Keep prior released
fixture versions available when results reference them.
