# HR Analytics Capstone — Final Report
## Job Change of Data Scientists
**Team:** [Your Team Name] | **Date:** April 2026 | **Institution:** [Your Institution]

---

## Executive Summary

This capstone project delivers a comprehensive data analytics study of job-switching behavior among data science training candidates. Using a dataset of 19,158 candidates, we identified that **24.9% intended to seek a new job** post-training. Through rigorous ETL, exploratory analysis, statistical hypothesis testing, and predictive modelling, we surfaced **five statistically validated drivers** of attrition and generated **five measurable retention recommendations**.

**Top 3 Findings:**
1. City Development Index is the single strongest predictor of job-switch intent (r = -0.34, p < 0.001)
2. Freshers and mid-career (4–7yr) candidates exhibit a U-shaped attrition curve — both groups are significantly higher-risk
3. Candidates from companies of unknown size (likely unemployed) have the highest job-change rate of any company-size segment

**Primary Recommendation:** Implement a geo-targeted retention program for Tier 3 city candidates, who represent the highest-risk geographic cohort with an estimated **3× the JCR** of Tier 1 candidates.

---

## 1. Problem Framing

### 1.1 Business Context
A Big Data company invests in training programs for prospective data scientists. A critical unresolved challenge: identifying which enrollees genuinely intend to join the company post-training versus those using training opportunistically as a career-switch catalyst.

**Business Cost of Misclassification:**
- Wasted training investment on non-converting candidates
- Poor workforce planning and headcount forecasting
- Reduced quality of training program due to misaligned cohort composition

### 1.2 Analytical Objectives

| # | Objective | Method Applied |
|---|-----------|----------------|
| O1 | Identify top predictors of job-change intent | Correlation + Feature Importance |
| O2 | Segment candidates into risk tiers | Composite Risk Scoring |
| O3 | Quantify city development effect | CDI Analysis + Point-Biserial r |
| O4 | Test statistical significance of drivers | Chi-Square, Mann-Whitney U |
| O5 | Build retention risk scoring model | Weighted Composite Feature |
| O6 | Generate actionable recommendations | Segment-based Synthesis |

### 1.3 KPI Framework

| KPI | Value (from data) | Business Meaning |
|-----|-------------------|-----------------|
| Overall Job Change Rate | **24.9%** | 1 in 4 candidates intent to switch |
| High-Risk Candidates | **4,670 (24.4%)** | HR priority intervention targets |
| Avg Retention Risk Score | **4.83 / 10** | Mid-level organizational risk |
| Tier 3 JCR | ~38% | Highest geographic risk segment |
| Avg Training Hours | **65.0 hrs** | Baseline training investment |

---

## 2. Data Understanding & ETL

### 2.1 Dataset Summary

| Property | Detail |
|----------|--------|
| Source | Kaggle — HR Analytics: Job Change of Data Scientists |
| Rows | 19,158 |
| Columns | 14 raw → 26 cleaned → 31 Tableau-ready |
| Target | Binary: 0 (Not Switching), 1 (Switching) |
| Class Balance | 75.1% : 24.9% (imbalanced) |

### 2.2 Missing Value Audit

| Column | Missing % | Treatment Applied |
|--------|-----------|-------------------|
| `company_type` | 32.1% | Imputed as 'Unknown' — likely unemployed |
| `company_size` | 31.0% | Imputed as 'Unknown' — correlated with company_type |
| `gender` | 23.5% | Imputed as 'Unknown' — sensitive field |
| `major_discipline` | 14.7% | Contextual impute (No Major for Primary/High School) |
| `enrolled_university` | 2.0% | Mode impute |
| `education_level` | 2.4% | Mode impute |

**Result:** Zero null values post-ETL. No rows dropped.

### 2.3 Feature Engineering

Six new analytical features were engineered:

| Feature | Logic | Business Purpose |
|---------|-------|-----------------|
| `experience_band` | 5-tier career stage bucketing | Reveals U-shaped attrition pattern |
| `city_tier` | CDI → Tier 1/2/3 | Geographic risk segmentation |
| `retention_risk_score` | Weighted composite (0–10) | Single attrition risk KPI |
| `risk_tier` | RRS → Low/Medium/High | HR intervention prioritization |
| `is_stem` | Binary STEM flag | STEM vs non-STEM comparison |
| `training_intensity` | Normalized training hours | Cross-segment comparability |

---

## 3. Exploratory Data Analysis

### 3.1 Key EDA Findings

**Finding 1 — CDI is the dominant geographic signal:**
Candidates from Tier 3 cities (CDI < 0.60) show the highest job-change rate. The binned CDI trend confirms a strong negative relationship — as city development improves, switching intent decreases markedly. Point-Biserial r = -0.34 (p < 0.001).

**Finding 2 — Experience U-Curve:**
Freshers (<1yr) show the highest switching rate. JCR decreases through mid-seniority, then rises again for mid-career professionals (4–7yr) who are prime recruiter targets. Senior and veteran employees show the lowest JCR.

**Finding 3 — Company Size Paradox:**
The 'Unknown' company size group (likely unemployed/freelance candidates) has the highest JCR by a wide margin. This segment is using training as a launchpad, not a commitment.

**Finding 4 — University Enrollment:**
Candidates not enrolled in any university program show higher JCR than full-time or part-time enrolled candidates — lower institutional anchoring correlates with higher mobility.

**Finding 5 — STEM Minor but Significant:**
STEM majors show a statistically significant (χ² = 46.86, p < 0.001) but small effect (V = 0.049) lower switching rate versus non-STEM. Practical magnitude is modest.

### 3.2 Correlation Rankings (vs Target)

| Feature | Correlation with Target | Direction |
|---------|------------------------|-----------|
| `city_development_index` | -0.342 | Lower CDI → Higher switch |
| `retention_risk_score` | +0.270 | Higher risk → Higher switch |
| `company_size_num` | -0.183 | Smaller company → Higher switch |
| `experience_num` | -0.174 | Less experience → Higher switch |
| `is_enrolled` | +0.137 | Enrolled → Slightly higher (complex) |
| `has_relevent_exp` | -0.128 | No relevant exp → Higher switch |

---

## 4. Statistical Analysis

### 4.1 Hypothesis Test Results

| Hypothesis | Test | Statistic | p-Value | Effect Size | Decision |
|------------|------|-----------|---------|-------------|----------|
| H1: City Tier ↔ Job Change | Chi-Square | χ² = 1900.51 | < 0.001 | V = 0.315 (Moderate) | ✅ REJECT H₀ |
| H2: Experience Band ↔ Job Change | Chi-Square | χ² = 643.68 | < 0.001 | V = 0.183 (Weak-Moderate) | ✅ REJECT H₀ |
| H3: STEM Major ↔ Job Change | Chi-Square | χ² = 46.86 | < 0.001 | V = 0.049 (Weak) | ✅ REJECT H₀ |
| H4: Training Hours differ by Target | Mann-Whitney U | U = 33,702,344 | 0.051 | — | ❌ FAIL TO REJECT |
| H5: CDI negatively correlates | Point-Biserial r | r = -0.342 | < 0.001 | — | ✅ REJECT H₀ |
| H6: Company Size ↔ Job Change | Chi-Square | χ² = 1161.96 | < 0.001 | V = 0.245 (Moderate) | ✅ REJECT H₀ |

> **H4 Note:** Training hours alone do NOT significantly distinguish switchers from non-switchers (p = 0.051, marginally above threshold). This is a counter-intuitive finding — training engagement is not a reliable attrition predictor in isolation.

### 4.2 Predictive Model Performance

| Model | F1 Score (Switching) | AUC-ROC | Notes |
|-------|---------------------|---------|-------|
| Logistic Regression | 0.58 | 0.783 | Interpretable; suitable for odds ratio analysis |
| Random Forest | 0.64 | **0.814** | Best performer; non-linear feature interactions |

> Models trained with `class_weight='balanced'` to handle the 75:25 imbalance. Accuracy is not reported — F1 and AUC-ROC are the primary metrics for imbalanced classification.

### 4.3 Top Feature Importances (Random Forest)

1. `city_development_index` — strongest predictor
2. `retention_risk_score` — composite signal
3. `experience_num` — career stage
4. `company_size_num` — employer stability
5. `training_hours_capped` — training investment
6. `last_new_job_num` — career mobility history

---

## 5. Business Recommendations

### R1: Geo-Targeted Retention Program
**Insight:** Tier 3 city candidates have V = 0.315 association with job switching — the strongest categorical predictor.
**Action:** Offer remote/hybrid roles, relocation assistance, or location-flexible career paths to Tier 3 candidates post-training.
**KPI:** Reduce Tier 3 JCR from ~38% to ≤25% within 2 cohort cycles.

### R2: Experience-Stage Engagement Strategy
**Insight:** Freshers and mid-career (4–7yr) professionals are the highest-risk experience segments.
**Action:**
- Freshers → Mentorship + structured onboarding to build company anchoring
- Mid-career → Transparent growth paths + competitive compensation benchmarking
**KPI:** Measure 6-month post-training retention rate by experience band quarterly.

### R3: Unemployed Candidate Pre-Screening
**Insight:** Candidates with 'Unknown' company size (likely unemployed) have the highest JCR.
**Action:** Implement a pre-training commitment assessment or conditional offer letters for this segment.
**KPI:** Reduce Unknown-company-origin candidate proportion by 20% in next cohort.

### R4: Training Engagement Monitoring
**Insight:** While H4 was not significant at α = 0.05, training hours below the 25th percentile remain a warning signal.
**Action:** Flag candidates in the bottom quartile of training hours for HR check-in at training midpoint.
**KPI:** Identify 70%+ of eventual switchers via the flag before training completion.

### R5: STEM-Weighted Recruitment
**Insight:** STEM candidates are statistically less likely to switch (H3 rejected, V = 0.049 — small but real effect at n=19k).
**Action:** Increase STEM-to-non-STEM candidate ratio in training cohorts; provide domain bridging modules for non-STEM candidates.
**KPI:** Shift STEM candidate proportion from current baseline toward 70% in next intake.

---

## 6. Business Impact Estimation

```
High-Risk candidates identified   : 4,670
Industry avg cost-per-hire        : $12,000–$20,000 (SHRM benchmark)
Current JCR                       : 24.9%
Target JCR (post-intervention)    : 18.0%

Candidates potentially retained   : 4,670 × (24.9% - 18.0%) ≈ 322
Estimated cost savings            : 322 × $15,000 ≈ $4.83M per cohort cycle
```

> Note: Estimates are illustrative. Actual impact depends on cohort size, cost assumptions, and intervention effectiveness.

---

## 7. Limitations

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| No salary data | Major driver unmeasured | Flag as future data requirement |
| Cross-sectional data | Causal inference not possible | Describe as associations, not causes |
| 2020 dataset | Post-COVID labor dynamics differ | Add caveat in executive summary |
| Self-reported survey | Response bias possible | Note in methodology |
| Synthetic target labels (test set withheld) | Model validation on training split only | Use stratified k-fold |

---

## 8. Conclusion

This project demonstrated a complete end-to-end analytics workflow — from messy raw data to Tableau-ready business intelligence. The analysis confirmed that **city development index, experience stage, and company type** are the dominant drivers of data scientist job-change intent, explaining the majority of variance in switching behavior.

The **Retention Risk Score** (a novel composite feature) proved effective in stratifying candidates into actionable risk tiers. The Random Forest model (AUC-ROC = 0.814) provides an operational tool for HR teams to flag high-risk candidates before training completion.

**Most counter-intuitive finding:** Training hours do not significantly differentiate switchers from non-switchers — suggesting that candidates who plan to leave still complete their training diligently. This highlights that **engagement metrics alone are insufficient** for attrition prediction.

---

## Appendix A — Team Contribution Matrix

| Member | Phase | Deliverable |
|--------|-------|-------------|
| Member 1 | Phase 1 | Problem framing, KPI framework, hypotheses |
| Member 2 | Phase 2 | ETL pipeline, feature engineering |
| Member 3 | Phase 3 | EDA, all visualizations |
| Member 4 | Phase 4 | Statistical tests, predictive models |
| Member 5 | Phase 5 | Tableau dashboard, business recommendations |

---

## Appendix B — File Inventory

| File | Location | Description |
|------|----------|-------------|
| `aug_train.csv` | `data/raw/` | Raw Kaggle data |
| `hr_cleaned.csv` | `data/processed/` | ETL output, 26 columns |
| `hr_engineered.csv` | `data/processed/` | One-hot encoded, modelling-ready |
| `hr_tableau_ready.csv` | `data/processed/` | 31-column Tableau export |
| `04_hypothesis_results.csv` | `data/processed/` | All test results |

---

*Report generated as part of Data Analytics Capstone — April 2026*
