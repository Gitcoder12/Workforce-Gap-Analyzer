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

## Examples Used
- Comparing electrician demand and availability in Hyderabad
- Identifying regional shortages of healthcare workers
- Mapping skills demand against available candidates


---

## Comparison with Existing Projects and Data Sources

Workforce Gap Analyzer is documented as a regional demand-versus-availability concept for identifying occupations with possible shortages. Its closest comparators are labour-market data systems and skills-taxonomy projects rather than one identical open-source application.

| Project / resource | Established focus | Relationship to Workforce Gap Analyzer |
|---|---|---|
| [ESCO skills map](https://github.com/LigiaAdam/esco-skills-map) | Maps skills and occupations using the European Skills, Competences, Qualifications and Occupations classification | A skills/occupation taxonomy reference; Workforce Gap Analyzer's intended focus is regional demand-versus-supply analysis. |
| [ESCO CSV-to-Graph](https://github.com/Y4SSERk/ESCO-csv2Graph) | Converts ESCO classification data into graph form | A data-modelling reference for relationships among occupations and skills, not a live labour-market shortage detector. |
| [O*NET](https://www.onetonline.org/) | US occupational descriptions, skills, tasks and labour-market information | A major occupational-information reference; its US coverage is not a substitute for local Indian demand/supply data. |

### Where Workforce Gap Analyzer is different
- **Regional framing:** the product is intended to answer which occupations appear underserved in a selected location.
- **Demand-versus-availability model:** its central concept compares workforce supply with demand, rather than only listing job titles or skills.
- **Decision-oriented output:** the proposed high/medium/low opportunity bands aim to make the result understandable to job seekers and planners.

### Where established projects are stronger
ESCO and O*NET provide structured occupational taxonomies and richer metadata. The current README describes planned public data/API integration and an early implementation; it does not establish that its sample job counts, salary bands or opportunity labels represent current market conditions.

### Evidence and limitations
A defensible shortage estimate needs dated vacancies, deduplication, occupation mapping, geography, labour-force supply, source coverage and a published calculation method. Label sample records as illustrative. Do not equate job-posting counts with actual vacancies or infer a shortage from demand alone. This comparison is a positioning note, not a validation of the current estimates.
