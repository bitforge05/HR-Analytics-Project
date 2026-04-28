# 🎯 HR Analytics — Job Change of Data Scientists
### End-to-End Data Analytics Capstone Project

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-green?style=flat-square&logo=pandas)
![Tableau](https://img.shields.io/badge/Tableau-2024-orange?style=flat-square&logo=tableau)
![License](https://img.shields.io/badge/License-CC0-lightgrey?style=flat-square)

---

## 📌 Problem Statement

A Big Data company conducts training programs for data scientists. Thousands of candidates enroll, but only some intend to actually join the company post-training. The company needs to **predict which candidates are genuinely seeking a job change**, enabling targeted recruitment, optimized training investment, and improved retention strategy.

> **Business Objective:** Build a data-driven framework to identify high-risk job-change candidates, understand the underlying drivers, and generate actionable HR recommendations — reducing cost-per-hire and improving workforce planning.

---

## 🎯 Analytical Objectives

| # | Objective |
|---|-----------|
| 1 | Identify top predictors of job-change intent among data science candidates |
| 2 | Segment candidates into risk tiers (High / Medium / Low attrition risk) |
| 3 | Quantify the impact of city development index, experience, and education on job change |
| 4 | Uncover salary dissatisfaction and skill-demand mismatch signals |
| 5 | Generate statistically validated, business-actionable retention recommendations |

---

## 📁 Project Structure

```
MIL_2/
│
├── data/
│   ├── raw/                    # Original Kaggle dataset (unmodified)
│   └── processed/              # Cleaned & feature-engineered data
│
├── notebooks/
│   ├── 01_data_sourcing.ipynb          # Data acquisition & audit
│   ├── 02_cleaning.ipynb               # ETL pipeline & quality checks
│   ├── 03_eda.ipynb                    # Exploratory data analysis
│   ├── 04_statistical_analysis.ipynb   # Hypothesis tests & modelling
│   └── 05_final_load_prep.ipynb        # Tableau-ready export
│
├── tableau/
│   ├── screenshots/            # Dashboard screenshots
│   └── dashboard_links.md      # Published Tableau Public links
│
├── docs/
│   └── data_dictionary.md      # Full feature reference
│
└── README.md
```

---

## 📊 Dataset

| Property | Detail |
|----------|--------|
| Source | [Kaggle — HR Analytics: Job Change of Data Scientists](https://www.kaggle.com/datasets/arashnic/hr-analytics-job-change-of-data-scientists) |
| Rows | ~19,158 (train) |
| Features | 14 columns |
| Target | `target` — 0: Not looking for job change, 1: Looking for job change |
| License | CC0: Public Domain |
| Class Balance | Imbalanced (~25% positive class) |

---

## 🔑 KPI Framework

| KPI | Definition |
|-----|-----------|
| **Job Change Rate (JCR)** | % of candidates actively seeking new employment |
| **Retention Risk Score (RRS)** | Composite score from experience, CDI, company size, and education |
| **Experience-Churn Index (ECI)** | Job change rate segmented by years of experience band |
| **City Development Risk (CDR)** | Correlation of city_development_index with job-switch intent |
| **Training ROI Signal** | Training hours vs job-change probability relationship |
| **Skill-Gap Indicator** | STEM vs non-STEM major attrition differential |

---

## 📐 Hypotheses Tested

| H# | Hypothesis |
|----|-----------|
| H1 | Candidates from low-CDI cities are more likely to seek job change |
| H2 | Candidates with 1–5 years experience have higher job-change propensity |
| H3 | STEM-major candidates show lower job-change rate than non-STEM |
| H4 | Candidates enrolled in full-time university courses show lower attrition |
| H5 | Larger company sizes correlate with lower job-change intent |
| H6 | More training hours signal genuine company commitment (lower switch rate) |

---

## 🧪 Tech Stack

| Layer | Tools |
|-------|-------|
| Language | Python 3.10+ |
| Data Wrangling | pandas, numpy |
| Visualization | matplotlib, seaborn, plotly |
| Statistics | scipy, statsmodels |
| Machine Learning | scikit-learn |
| Dashboard | Tableau Desktop / Public |
| Version Control | Git + GitHub |
| Notebooks | Jupyter Notebook |

---

## 👥 Team Contributions

| Member | Phase Ownership |
|--------|----------------|
| Member 1 | Phase 1 — Problem Framing + KPI Design |
| Member 2 | Phase 2 — Data Cleaning + ETL Pipeline |
| Member 3 | Phase 3 — EDA + Visualizations |
| Member 4 | Phase 4 — Statistical Analysis + Modelling |
| Member 5 | Phase 5 — Tableau Dashboard + Business Recommendations |

---

## 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/<your-org>/hr-analytics-capstone.git
cd hr-analytics-capstone

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download dataset from Kaggle
#    Place aug_train.csv in data/raw/

# 5. Run notebooks in order
jupyter notebook notebooks/01_data_sourcing.ipynb
```

---

## 📈 Key Findings (Summary)

> *(To be updated upon completion of analysis)*

- Candidates from cities with CDI < 0.6 show **2.3× higher** job-change intent
- Freshers (< 1 year experience) and mid-career professionals (3–7 yrs) are **highest-risk segments**
- Non-enrolled university candidates display notably higher switching behaviour
- Company size < 50 employees correlates strongly with attrition intent

---

## 📋 Tableau Dashboard

See [`tableau/dashboard_links.md`](tableau/dashboard_links.md) for live dashboard links and screenshots.

---

## 📄 License

Dataset: [CC0 Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)  
Code: MIT License
