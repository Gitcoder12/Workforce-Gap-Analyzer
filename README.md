# Workforce Gap Analyzer

**A web prototype for exploring job-demand and skills data by location.**

[![License](https://img.shields.io/badge/license-see%20LICENSE-lightgrey)](LICENSE)

Workforce Gap Analyzer is a Flask application that presents job-opportunity and skills information. The current implementation uses bundled example data and includes resume-document parsing dependencies for its analysis workflow.

## Features

- Location-based browsing of the bundled job dataset.
- Role, skills, salary-range, and opportunity indicators.
- Resume-file parsing support for PDF and DOCX inputs.
- Flask routes for serving the interface and processing requests.

## Tech Stack

Python · Flask · Gunicorn · pdfplumber · python-docx · HTML · CSS · JavaScript

## Quick Start

```bash
git clone https://github.com/Gitcoder12/Workforce-Gap-Analyzer.git
cd Workforce-Gap-Analyzer

python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS / Linux: source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## Deployment

A Render service definition is included in `render.yaml`. It installs `requirements.txt` and starts the Flask app with Gunicorn.

## Scope and Limitations

The current job listings are bundled sample data, not a live feed of vacancies or a statistically representative labor-market dataset. Salary and demand labels should not be used as current employment forecasts. Resume parsing is not a hiring decision or a substitute for human review.

## License

See [LICENSE](LICENSE).

---

## Project handbook

- [Activity log](ACTIVITY_LOG.md)
- [Feature upgrade plan](FEATURE_UPGRADE_PLAN.md)
- [Company and team fit](COMPANY_FIT.md)
- [Beginner and technical README draft](README_ADDENDUM_DRAFT.md)
- [README quality checklist](README_QUALITY_CHECKLIST.md)
- [Contributing](CONTRIBUTING.md)
- [Agent instructions](AGENTS.md) · [Agent skills](SKILLS.md)
