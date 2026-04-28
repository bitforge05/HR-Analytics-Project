# 📊 Capstone Presentation Outline
## HR Analytics: Job Change of Data Scientists

**Target Audience:** HR Leadership & Technical Evaluators
**Duration:** 10–12 Minutes
**Goal:** Demonstrate business value, technical rigor, and actionable results.

---

### Slide 1: Title Slide
- **Title:** Predictive HR Analytics: Tackling Data Scientist Attrition
- **Subtitle:** An End-to-End Analytics Framework for Talent Retention
- **Presented by:** [Your Name/Team]
- **Key Visual:** High-quality background image of a modern workplace or a network graph.

---

### Slide 2: The Business Challenge (Phase 1)
- **Problem:** Data Science training programs face high "non-conversion" rates.
- **Impact:** Wasted training budget, recruitment delays, and unstable workforce planning.
- **Objective:** Identify "opportunistic" candidates vs. genuine hires.
- **Key Metric:** Job Change Rate (JCR) - Currently at 24.9%.

---

### Slide 3: Analytical Framework & KPIs
- **The Approach:** ETL → Statistical Validation → Predictive Modeling → Tableau Visualization.
- **Core KPIs:**
  - **Retention Risk Score (RRS):** Our custom 0-10 index.
  - **City Development Index (CDI):** The primary geographic driver.
  - **Experience-Churn Index:** Segmented risk by career stage.

---

### Slide 4: Data Quality & ETL Pipeline (Phase 2)
- **Raw State:** Messy data, 30%+ missingness in company fields, imbalanced targets.
- **Transformation:** 
  - Mode & Contextual Imputation (Major Discipline vs. Education).
  - Feature Engineering: City Tiers, Experience Bands, Risk Tiers.
  - Outlier Capping: Training hours (3x IQR).
- **Quality Audit:** Zero nulls, 31 feature columns, Tableau-optimized.

---

### Slide 5: Exploratory Insights — The "Why" Behind the Switch (Phase 3)
- **Visual 1:** JCR by City Tier (Tier 3 is 3x higher risk).
- **Visual 2:** The Experience U-Curve (Freshers and Mid-Career peak risk).
- **Insight:** STEM background provides a "stability buffer" but CDI is the dominant force.

---

### Slide 6: Statistical Validation — Proving our Hypotheses (Phase 4)
- **Key Test:** Chi-Square showed City Tier and Experience are highly significant (p < 0.001).
- **Effect Sizes:** Cramér's V confirmed City Tier as the strongest categorical predictor (0.315).
- **The "A-ha" Moment:** Training hours are *not* a statistically significant differentiator (p=0.051). *Engagement does not equal loyalty.*

---

### Slide 7: Predictive Modeling Performance
- **Models:** Logistic Regression vs. Random Forest.
- **Champion:** Random Forest (AUC-ROC: 0.814).
- **Performance:** 79% recall on switchers (identifying the risk before it happens).
- **Feature Importance:** CDI, Risk Score, and Experience are the "Big Three".

---

### Slide 8: Tableau Executive Dashboard (Phase 4)
- **Sections:**
  - Risk Overview (KPIs).
  - Driver Analysis (Drill-downs).
  - Talent Segmentation (Targeting).
- **Interactivity:** Demonstrate how filters allow HR to zoom into specific departments or cities.

---

### Slide 9: Strategic Recommendations (Phase 5)
- **Recommendation 1:** Geo-Targeted Relocation for Tier 3 City Talent.
- **Recommendation 2:** Custom Engagement for the "4-7 Year" Mid-Career Segment.
- **Recommendation 3:** Pre-training commitment contracts for unemployed candidates.
- **Recommendation 4:** Continuous Risk Monitoring using the RF Model.

---

### Slide 10: Business Impact & ROI
- **Projected Savings:** ~$4.8M per cohort cycle by reducing JCR by 6.9%.
- **Intangible Value:** Improved cohort quality, better workforce morale, and data-driven HR culture.

---

### Slide 11: Future Roadmap & Limitations
- **Limitations:** Lack of salary/comp data; cross-sectional nature.
- **Next Steps:** Survival Analysis (predicting *when* they will leave); SHAP value integration for individual candidate explanations.

---

### Slide 12: Q&A / Conclusion
- **Final Thought:** Data science isn't just about code; it's about people.
- **Call to Action:** Implement the Risk Scoring model in the next recruitment cycle.

---
