# Workforce-Gap-Analyzer — Feature Upgrade Plan

**Snapshot:** 2026-11-13

## Objective

A web prototype that compares example job opportunities with skill information and can parse a resume to explore possible skill gaps.

## P0 — correctness, scope and safety

- [ ] Bound and validate resume uploads before parsing; handle empty, oversized, unsupported and malformed files.
- [ ] Document the bundled dataset's source, age, geography and representativeness; do not present it as current live market data.

## P1 — complete user workflow

- [ ] Add deterministic parsing tests for PDF, DOCX, TXT and malformed documents.
- [ ] Separate skill extraction from matching/scoring and show evidence for each suggested gap.

## P2 — evaluation and scale

- [ ] Evaluate matching quality with a consented, de-identified and documented test set.
- [ ] Add data freshness and regional coverage reporting before integrating external job feeds.

## Contributor work packages

1. Input contracts and validation with fixture-based tests.
2. Deterministic core workflow and auditable outputs.
3. User-facing explanations, accessibility and error handling.
4. Reproducible evaluation with a baseline and documented limitations.

## Definition of done

- [ ] Setup works from a clean environment.
- [ ] Tests cover normal, missing, malformed and boundary inputs.
- [ ] Demo/sample data and real external data are clearly distinguished.
- [ ] README, tests and activity log agree on actual behavior.
