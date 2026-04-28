# 📖 Data Dictionary — HR Analytics: Job Change of Data Scientists

**Dataset Source:** [Kaggle](https://www.kaggle.com/datasets/arashnic/hr-analytics-job-change-of-data-scientists)  
**File:** `aug_train.csv`  
**Rows:** ~19,158 | **Columns:** 14  
**Last Updated:** 2026-04-28  

---

## 🔑 Feature Reference Table

| Column Name | Data Type | Role | Description | Unique Values / Range | Missing? | Notes |
|---|---|---|---|---|---|---|
| `enrollee_id` | int64 | Identifier | Unique candidate ID | 19,158 unique | No | Drop before modelling; keep for auditing |
| `city` | object | Categorical (Nominal) | City code where candidate resides | ~123 cities | No | High cardinality; use CDI as proxy |
| `city_development_index` | float64 | Continuous | Scaled economic development index of candidate's city | 0.448 – 0.949 | No | Key predictor; lower = less developed |
| `gender` | object | Categorical (Nominal) | Self-reported gender | Male, Female, Other | **~24%** | Impute with mode or 'Unknown' category |
| `relevent_experience` | object | Categorical (Binary) | Whether candidate has relevant experience | Has relevent experience, No relevent experience | No | Binary encode: 1 / 0 |
| `enrolled_university` | object | Categorical (Nominal) | Type of university course enrolled in | no_enrollment, Part time course, Full time course | **~2%** | Impute with 'no_enrollment' |
| `education_level` | object | Categorical (Ordinal) | Highest education level attained | Primary School < High School < Graduate < Masters < Phd | **~2.4%** | Ordinal encode |
| `major_discipline` | object | Categorical (Nominal) | Field of education | STEM, Business Degree, Humanities, Arts, No Major, Other | **~14.7%** | High missing for Primary/High School; impute contextually |
| `experience` | object | Categorical (Ordinal) | Total years of professional experience | <1, 1–20, >20 | **~0.3%** | Ordinal encode; treat <1 and >20 as boundaries |
| `company_size` | object | Categorical (Ordinal) | No. of employees at current employer | <10, 10–49, 50–99, 100–500, 500–999, 1000–4999, 5000–9999, 10000+ | **~31%** | High missing; likely unemployed/freelancer |
| `company_type` | object | Categorical (Nominal) | Type of employer organization | Pvt Ltd, Public Sector, Funded Startup, Early Stage Startup, NGO, Other | **~32%** | High missing; correlates with company_size missingness |
| `last_new_job` | object | Categorical (Ordinal) | Gap (years) between previous and current job | never, 1, 2, 3, 4, >4 | **~2.2%** | Ordinal encode; never = very stable |
| `training_hours` | int64 | Continuous | Total training hours completed | 1 – 336 | No | Potential right-skew; check outliers |
| `target` | int64 | **Target Variable** | Job change intent | 0 = Not looking, 1 = Looking | No (test set only) | Imbalanced: ~25% positive |

---

## 📊 Derived / Engineered Features

| Feature Name | Derivation Logic | Business Meaning |
|---|---|---|
| `experience_band` | Bucketed from `experience`: Fresher(<1), Early(1–5), Mid(6–10), Senior(11–20), Veteran(>20) | Risk segmentation by career stage |
| `retention_risk_score` | Weighted composite of CDI (−), experience_band, company_size, relevant_experience | Aggregate attrition risk signal |
| `city_tier` | CDI binned: Tier 1 (>0.8), Tier 2 (0.6–0.8), Tier 3 (<0.6) | Geographic opportunity segmentation |
| `is_stem` | 1 if major_discipline == 'STEM', else 0 | STEM vs non-STEM attrition comparison |
| `training_intensity` | training_hours / median(training_hours) — normalized | Commitment proxy |
| `job_gap_ordinal` | Ordinal encoding of last_new_job | Career stability indicator |
| `company_size_ordinal` | Ordinal encoding of company_size | Company stability signal |
| `education_ordinal` | Ordinal encoding of education_level | Human capital proxy |
| `gender_encoded` | Label encoding with 'Unknown' for missing | Demographics feature |
| `is_enrolled` | 0 if no_enrollment, 1 otherwise | University enrollment indicator |

---

## ⚠️ Data Quality Issues Identified

| Issue | Columns Affected | Severity | Treatment |
|---|---|---|---|
| High missingness | `company_size`, `company_type` (~31–32%) | 🔴 High | Impute as 'Unknown'/'Not Employed' category |
| Moderate missingness | `gender` (~24%) | 🟠 Medium | Mode imputation + 'Unknown' encoding |
| Low missingness | `enrolled_university`, `education_level`, `last_new_job` (<3%) | 🟡 Low | Mode or KNN imputation |
| Ordinal stored as string | `experience`, `company_size`, `last_new_job` | 🟠 Medium | Custom ordinal mapping |
| Class imbalance | `target` (~75/25 split) | 🟠 Medium | Note for modelling; report adjusted metrics (F1, AUC) |
| High cardinality | `city` (123 unique) | 🟡 Low | Use `city_development_index` as continuous proxy |
| Typo in column name | `relevent_experience` | 🟡 Low | Document as-is; do not rename in raw file |

---

## 🗂️ File Inventory

| File | Location | Description |
|---|---|---|
| `aug_train.csv` | `data/raw/` | Original training data from Kaggle |
| `aug_test.csv` | `data/raw/` | Original test data (no target column) |
| `sample_submission.csv` | `data/raw/` | Submission format reference |
| `hr_cleaned.csv` | `data/processed/` | Fully cleaned dataset after ETL |
| `hr_tableau_ready.csv` | `data/processed/` | Final export optimized for Tableau |
| `hr_engineered.csv` | `data/processed/` | Feature-engineered dataset for modelling |

---

## 📐 Target Variable Distribution

| Class | Label | Count | Percentage |
|---|---|---|---|
| 0 | Not looking for job change | ~14,381 | ~75.1% |
| 1 | Looking for job change | ~4,777 | ~24.9% |

> **Note:** Dataset is imbalanced. Report precision, recall, F1, and AUC-ROC over accuracy.
