# B2B SaaS Marketing Attribution Analysis

An interactive marketing analytics case study for a B2B SaaS company. The project measures channel performance across the funnel—from sessions and first-touch leads to won revenue—and surfaces CAC, LTV, ROI, and multi-touch attribution in an executive Streamlit dashboard.

<img width="1440" height="777" alt="Screenshot 2026-05-25 at 01 33 56" src="https://github.com/user-attachments/assets/a1addf2e-b8c9-4da8-ba83-7be9ab115015" />

## Overview

Marketing teams often over-index on traffic and last-touch attribution when making budget decisions. This project demonstrates why channel evaluation should combine volume, conversion quality, attribution context, and financial efficiency.

**What you get**

- A multi-page **Streamlit dashboard** (`app_new.py`) with filters by industry, region, and channel
- A modular **Python analytics layer** (`src/`) for loading data, building the funnel, computing KPIs, and comparing attribution paths
- **Mock CSV datasets** representing a realistic B2B buyer journey
- **Static chart exports** and a **pytest** suite for core logic

## Business problem

Surface-level reporting (sessions alone, or last-touch only) can misallocate budget. The analysis separates demand creation from demand capture and compares channels on funnel quality and unit economics—not just top-of-funnel volume.

## Project goals

- Measure top-of-funnel traffic by source
- Compare first-touch lead generation across channels
- Evaluate funnel conversion from lead → opportunity → won deal
- Compare first-touch and last-touch attribution paths
- Estimate CAC, LTV, and ROI by channel
- Turn findings into actionable budget recommendations

## Tech stack

| Layer | Tools |
|-------|--------|
| App | [Streamlit](https://streamlit.io/), Plotly |
| Analytics | Python, pandas, NumPy |
| Data | CSV files in `data/` |
| Tests | pytest |

`duckdb` is listed in `requirements.txt` for optional SQL-style exploration; the committed app and `src/` modules use pandas.

## Project structure

```text
marketing_attribution_project/
├── app_new.py              # Streamlit dashboard (entry point)
├── requirements.txt
├── data/                   # Mock marketing & revenue datasets
│   ├── marketing_sessions.csv
│   ├── leads.csv
│   ├── opportunities.csv
│   ├── revenue.csv
│   └── ad_spend.csv
├── src/
│   ├── load_data.py        # CSV loading & funnel build
│   ├── metrics.py          # KPIs, channel summary, LTV/CAC, ad efficiency
│   ├── attribution.py      # Last-touch & first/last path analysis
│   └── charts.py           # Plotly chart builders
├── tests/                  # Unit tests for src modules
├── visuals/
│   ├── charts/             # Exported analysis charts (README embeds)
│   └── screenshots/        # Dashboard screenshot
└── notes/
    └── insights.md         # Working notes & takeaways
```

## Dataset

Mock data simulates journeys across **Google**, **Organic**, **LinkedIn**, **Webinar**, **Partner**, and **Brand**.

| File | Description |
|------|-------------|
| `marketing_sessions.csv` | Session-level UTM, geo, device |
| `leads.csv` | Lead creation & firmographics |
| `opportunities.csv` | Pipeline stages and outcomes |
| `revenue.csv` | Won ARR by account |
| `ad_spend.csv` | Channel spend for CAC/ROI |

## Dashboard pages

The sidebar navigates eight views (with industry, region, and channel filters):

| Page | Focus |
|------|--------|
| Executive Summary | KPIs, channel overview, key insights |
| Funnel | Sessions → leads → opportunities → won |
| Channel Attribution | First-touch vs last-touch paths |
| Revenue & ARR | Won revenue by channel |
| Segmentation | Industry and region breakdowns |
| Ad Spend ROI | Spend, CAC, LTV:CAC, ROI |
| Retention | Customer retention views |
| Region & Device | Geo and device mix from sessions |

## Getting started

### Prerequisites

- Python 3.9+ (3.9 used in local development)

### Install

```bash
git clone https://github.com/ouzcankirazci/b2b-marketing-attribution-dashboard.git
cd b2b-marketing-attribution-dashboard

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the dashboard

```bash
streamlit run app_new.py
```

Open the URL shown in the terminal (typically `http://localhost:8501`).

### Run tests

```bash
pytest
```

## Analysis modules

| Module | Responsibility |
|--------|----------------|
| `load_data.load_all_data()` | Load all CSVs from `data/` |
| `load_data.build_funnel()` | Join sessions, leads, opportunities, revenue; derive first-touch |
| `metrics.calculate_kpis()` | Sessions, leads, won deals, revenue, spend, ROI |
| `metrics.channel_summary()` | Per-channel funnel and efficiency metrics |
| `metrics.calculate_ltv_cac()` | LTV, CAC, LTV:CAC by channel |
| `attribution.last_touch()` | Last UTM source before lead creation |
| `attribution.attribution_paths()` | Won deals by first-touch × last-touch pairs |

## Key findings

### Traffic

Google and Organic led top-of-funnel session volume. Traffic alone does not explain which channels generated quality pipeline or efficient revenue.


<img width="1440" height="777" alt="Screenshot 2026-05-25 at 01 34 31" src="https://github.com/user-attachments/assets/d5139659-533a-4105-b941-756ef222ba25" />

### First-touch leads

Organic and Google tied for the highest first-touch lead volume. Webinar performed well relative to its traffic, suggesting some channels outperform on lead efficiency despite lower raw sessions.

### Funnel quality

Organic and Partner generated the most won deals. Partner had the strongest lead-to-opportunity conversion rate—channel quality can differ meaningfully from top-of-funnel volume.

<img width="1440" height="771" alt="Screenshot 2026-05-25 at 01 35 08" src="https://github.com/user-attachments/assets/ffb29ae6-58e1-4c7e-b156-4505bd335eb0" />


### Attribution

Google captured the highest same-source first-touch → last-touch won revenue path. Organic often acted as a demand-creation channel whose journeys closed through other sources. Partner stood out on revenue efficiency despite lower volume—first-touch and last-touch should be analyzed together, not treated as interchangeable.

### Efficiency

Partner was the most efficient channel on LTV:CAC and ROI. Google remained the strongest scalable paid channel. Webinar showed attractive average LTV but too few won customers to scale confidently. Brand underperformed as a first-touch acquisition driver in this sample.

<img width="1440" height="774" alt="Screenshot 2026-05-25 at 01 35 33" src="https://github.com/user-attachments/assets/08d4397a-fd94-4b1b-886b-59deab6c3ceb" />


### Recommendations

- Increase investment in **Partner** (strongest efficiency and revenue quality)
- Keep **Google** as a core growth channel; optimize for downstream conversion, not traffic alone
- Continue testing **Webinar** before scaling (high LTV, low won volume)
- Avoid budget decisions from traffic or last-touch attribution in isolation
- Use multiple attribution views to separate demand creation from demand capture

## Additional notes

Working analysis notes and attribution path commentary live in [`notes/insights.md`](./notes/insights.md).

## Why this project

The case study shows marketing analytics beyond surface reporting: combining funnel conversion, multi-touch attribution, and financial metrics into practical channel recommendations—suitable for a portfolio, interview discussion, or stakeholder demo.

## License

This repository is shared as a portfolio / case-study project. Add a license file if you plan to open-source it formally.
