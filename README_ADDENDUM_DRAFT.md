# Workforce-Gap-Analyzer — README Explanation Draft

> Proposed copy. Check against the default-branch source before merging into README.md.

## In plain language

A web prototype that compares example job opportunities with skill information and can parse a resume to explore possible skill gaps.

## What the current implementation does

Flask application using bundled example job data and PDF/DOCX parsing dependencies. It is not a live labour-market feed or a validated hiring assessment. The existing audit opened issue #3 because the resume upload route reads all bytes without a configured size limit or robust format/content checks.

## Technical explanation

Document the data model, input validation, selection or query logic, API boundaries, dependencies and error paths. Provide one concrete input/output example.

## How to run

Use the exact commands in README.md. List prerequisites, expected output and common failure cases. State clearly that sample records are not live service data.

## Limitations and safety

Explain unsupported integrations, approximate calculations and failure behavior. Do not present a prototype as a real emergency dispatch or hiring decision system.

## Contributing

Start with FEATURE_UPGRADE_PLAN.md and CONTRIBUTING.md. Record verified changes in ACTIVITY_LOG.md.
