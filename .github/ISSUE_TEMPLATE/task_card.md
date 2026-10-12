---
name: Propose a Field Guide task card
description: Suggest a bounded extraction task, fixture, or fair comparison.
title: "[Task card]: "
labels:
  - task-card
body:
  - type: markdown
    attributes:
      value: |
        Thanks for improving the Field Guide. Keep the task small, reproducible, and synthetic. Do not include private/customer/health text, API keys, or non-redistributable data. A PR is welcome without opening an issue first.
  - type: textarea
    id: decision
    attributes:
      label: What decision would this card help someone make?
      placeholder: "For this input and constraints, help me choose between…"
    validations:
      required: true
  - type: textarea
    id: fixture
    attributes:
      label: Proposed synthetic cases and expected output
      description: Include normal and meaningful failure/edge cases. Explain annotation rules.
    validations:
      required: true
  - type: textarea
    id: candidates
    attributes:
      label: Candidate approaches
      description: List approaches that can fairly be evaluated on the same task and constraints.
    validations:
      required: true
  - type: textarea
    id: risks
    attributes:
      label: Dependencies, licensing, privacy, and runtime
      description: Mention model/API requirements, cost, hardware, data restrictions, and limits.
    validations:
      required: true
  - type: checkboxes
    id: readiness
    attributes:
      label: Contribution readiness
      options:
        - label: I checked existing catalog entries and Field Guide cards for duplicates.
          required: true
        - label: Any proposed text/data is synthetic or clearly redistributable.
          required: true
