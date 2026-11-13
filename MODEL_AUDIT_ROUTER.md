# Independent Model Audit Router — Workforce-Gap-Analyzer

**Revision date:** 2026-11-13

## Mandatory data and evidence policy
- Never replace real or maintainer-provided data with invented, generated, synthetic or placeholder records.
- Inspect Git history and trace the source, licence, collection time and provenance before touching a dataset.
- If evidence is missing, preserve the current data and mark it unknown/unverified. Do not guess or fill gaps.
- Synthetic fixtures are allowed only when clearly labelled and isolated from runtime/production records.
- Never invent official records, IDs, licences, inspection results, people, companies, citations, metrics, benchmark results, deployments or endorsements.
- Test claims require exact commands and results on the exact commit being reviewed.

## README preservation
Recover the last maintainer-authored README from history. Preserve it intact. Never rewrite or replace the original. Put any useful AI-generated explanation in a dated, clearly labelled addendum at the very bottom only. Do not silently remove original sections, links, wording or claims.

## Independent audit roles
1. Data provenance and synthetic-data separation.
2. Architecture, implementation and documented-command correctness.
3. Security, privacy, dependency and trust-boundary review.
4. Test, CI, build and reproducibility verification.
5. README history, licensing, attribution and link review.
6. Career/research claims and public-evidence review.

## Review workflow
1. Record exact HEAD SHA, branch, upstream/fork status and repository URL.
2. Classify all relevant changes as merged, open, closed-unmerged, reverted or unverified.
3. Inventory runtime datasets, generated files, fixtures, APIs and provenance.
4. Compare README against its pre-AI Git-history baseline.
5. Run install/build/lint/test checks on the exact commit; inspect CI for suppressed failures.
6. Audit security, privacy, accessibility, errors, edge cases and performance.
7. Verify public-facing claims and links; company matches are skill-fit hypotheses, not customer or partner claims.
8. Publish evidence-based findings before changing anything.

## Required finding format
Severity (**P0/P1/P2/P3**), exact file/line, reproduction, expected vs actual behaviour, evidence and commit SHA, confirmed/suspected/unverifiable status, minimal fix, regression test, and whether data or README history is affected.

## Merge gate
- [ ] No fabricated data shown as real or official.
- [ ] Real/user-provided data preserved.
- [ ] Synthetic examples visibly labelled and separated.
- [ ] README original preserved; AI addendum only at bottom.
- [ ] Exact-head tests and CI checked; failures disclosed.
- [ ] No secrets, private personal details, classified or confidential information.
- [ ] Licensing and upstream attribution retained.
- [ ] Independent second review and maintainer approval completed.

Repository: **Workforce-Gap-Analyzer**. Do not infer a feature from its name or roadmap. Do not merge, delete, force-push, replace datasets or alter the original README during an audit. The repository owner has final approval.
