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

## Installation

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
http://127.0.0.1:5000
```

> **Note:** Do **not** open `index.html` directly in your browser. The app requires the Flask server to be running because all job data and the Resume AI feature are served through Python API endpoints.

---

## Author

Dharavath Satvik

---

## License

MIT License
