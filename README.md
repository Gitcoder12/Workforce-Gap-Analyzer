# Workforce Gap Analyzer

A web-based system that identifies workforce shortages across different regions by analyzing job demand and availability. The platform helps users discover high-opportunity professions based on local workforce gaps.

---

## Overview

Workforce Gap Analyzer focuses on detecting areas where specific jobs are lacking. By comparing demand for services with available workforce data, the system highlights professions that are in shortage within a region.

This enables users to identify opportunities and make informed career or business decisions.

---

## Features

* Search by location
* Identify job shortages in a region
* View high-demand professions
* Opportunity level classification (High / Medium / Low)
* Simple and intuitive interface

---

## How It Works

1. User enters a location
2. The system analyzes job demand and workforce availability
3. Outputs:

   * Jobs with shortages
   * Opportunity levels
   * Suggested high-demand professions

---

## Example

Input:
Hyderabad

Output:

* High Demand:

  * Electricians
  * Plumbers
  * Gardeners

* Medium Demand:

  * Delivery workers

* Low Demand:

  * Software engineers

---

## Tech Stack

* Frontend: HTML, CSS, JavaScript
* Backend (planned): Node.js / Python
* Data Source (planned): Public datasets / APIs

---

## Future Enhancements

* Real-time job data integration
* Map-based visualization
* Predictive demand analysis
* User-specific recommendations
* Data-driven dashboards

---

## Research Potential

This project can be extended into research focusing on:

* Labor market demand-supply analysis
* Workforce shortage prediction models
* Regional employment optimization

---

## Deployment (Render.com — free hosting)

1. Fork this repository on GitHub.
2. Go to [https://render.com](https://render.com) and sign in with GitHub.
3. Click **New → Web Service** and connect your forked repository.
4. Render will auto-detect the `render.yaml` configuration.
5. Click **Deploy** — your app will be live at a public URL within minutes.

---

## Local Installation

```bash
git clone https://github.com/Gitcoder12/Workforce-Gap-Analyzer.git
cd Workforce-Gap-Analyzer
```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask server:

```bash
python app.py
```

Then open your browser and go to:

```
http://localhost:5000
```

> **Note:** Do **not** open `index.html` directly in your browser. The app requires the Flask server to be running because all job data and the Resume AI feature are served through Python API endpoints.

---

## Author

Dharavath Satvik

---

## License

MIT License


---

## AI-maintained project notes (secondary — 2026-11-13)

This section supplements the maintainer-authored README above. The original text has been restored verbatim from Git-history baseline `c3d5042902e4eb62d1d7bac15543f46f686a919f`; this addendum does not replace or certify the original claims.

- The source tree, runtime data and tests are the implementation source of truth. Roadmap items, draft PRs and AI-generated descriptions are not shipped features by themselves.
- Preserve existing maintainer-provided data. Never replace real data with synthetic or placeholder records. Clearly label and isolate test fixtures.
- Mark unverified sources, IDs, records, metrics and external claims as unknown/unverified instead of guessing.
- Verify setup, execution, test commands and public claims against the exact current commit before using this project in a job, research or academic application.
- See [MODEL_AUDIT_ROUTER.md](MODEL_AUDIT_ROUTER.md) for the independent model review and merge gate.

---

## Engineering Audit & Handover — 2026-11-17

**Review scope:** default branch `main`; static inspection of `app.py`. Runtime tests were not executed.

### Confirmed findings
- `JOBS_DATA` is an in-code dataset in `app.py`, with sample roles, salary bands, opening counts, growth scores, and generic company labels such as `Various` / `Various Tech`.
- The inspected data is not evidence of live job-market retrieval. Do not present its openings, salaries, growth scores, or rankings as current market facts.
- `KNOWN_SKILLS` is also a static list; it is not a live skills taxonomy.

### Next actions
1. Clearly label the current records as illustrative/demo data in the UI and API.
2. Add source, retrieval date, geography, currency, and provenance fields before presenting real market metrics.
3. Add tests for location lookup, empty results, malformed inputs, and the resume/skills analysis routes.

**Verification status:** static source inspection only; API behavior, deployment, and tests remain unverified.


---

## Branch Activity & Development History

**Audit date:** 2026-11-18 · **Comparison base:** `main`

| Branch | Difference from `main` | Observed work / changed paths |
|---|---:|---|
| `chore/remove-emoji-glyphs-2026-11-13` | Comparison unavailable | GitHub comparison service disconnected; retry required |
| `copilot/complete-workforce-analyzer` | 0 ahead / 7 behind | No unique commits relative to current `main`; branch is behind |
| `copilot/is-the-code-over` | 0 / 16 | No unique commits relative to current `main`; branch is behind |
| `docs/portfolio-operating-kit-2026-11-13` | 4 / 3 | Activity log, agent guidance, company-fit notes, feature plan, README support docs and skills |
| `docs/project-status-audit20261116` | Comparison unavailable | GitHub returned 404 for the comparison; recheck branch existence |

### Open pull requests observed during this audit

- [PR #5 — project status snapshot](https://github.com/Gitcoder12/Workforce-Gap-Analyzer/pull/5)
- [PR #4 — project handbook and contributor workflow](https://github.com/Gitcoder12/Workforce-Gap-Analyzer/pull/4)
- [PR #2 — remove emoji glyphs](https://github.com/Gitcoder12/Workforce-Gap-Analyzer/pull/2)

**Verification boundary:** Branch comparisons are metadata only. Recheck unavailable comparisons and inspect PR head/base plus CI before merging. No branches have been merged or deleted by this documentation update.
