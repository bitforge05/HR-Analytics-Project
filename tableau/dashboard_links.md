# 📊 Tableau Dashboard — HR Analytics: Job Change of Data Scientists

---

## 🔗 Published Dashboard Links

| Dashboard | Status | Link |
|-----------|--------|------|
| Executive Risk Overview | 🔄 In Progress | — |
| Job Change Drivers | 🔄 In Progress | — |
| Talent Segmentation | 🔄 In Progress | — |
| Retention Recommendations | 🔄 In Progress | — |

> Links will be updated upon Tableau Public publication.

---

## 🗂️ Dashboard Architecture

### Sheet 1 — Executive Risk Overview (KPI Banner)
**Purpose:** Top-level summary for HR leadership  
**Visuals:**
- KPI tiles: Overall Job Change Rate, High-Risk Candidate Count, Avg Training Hours (Switchers vs Non-Switchers)
- Donut chart: Target class distribution
- Map / Bubble chart: City-level job change rate by CDI

**Filters:** City Tier, Gender, Education Level

---

### Sheet 2 — Job Change Drivers
**Purpose:** Identify the strongest predictors of attrition intent  
**Visuals:**
- Horizontal bar chart: Feature importance (from logistic regression / random forest)
- Diverging bar: Job change rate by experience band (Fresher → Veteran)
- Heatmap: Education level × Company type job change rate
- Line chart: CDI vs Job change probability (scatter with trend line)

**Filters:** Major discipline, University enrollment status

---

### Sheet 3 — Talent Segmentation
**Purpose:** Cluster-based HR risk profiling  
**Visuals:**
- Treemap: Candidate segments by experience × company size × job change rate
- Stacked bar: Risk tier (High/Med/Low) by experience band
- Box plots: Training hours distribution across risk tiers
- Scatter: CDI vs Training hours, colored by target

**Filters:** Company type, Relevant experience

---

### Sheet 4 — Retention Recommendations
**Purpose:** Action-oriented insights for HR strategy  
**Visuals:**
- Decision tree summary visual (exported from Python)
- Funnel: Candidate journey — Enrolled → Trained → Retained
- Bar: Top 3 retention levers with estimated impact %
- Text table: Segment-specific retention playbook

---

## 📸 Screenshots

| File | Description |
|------|-------------|
| `screenshots/01_risk_overview.png` | Executive KPI dashboard |
| `screenshots/02_job_change_drivers.png` | Driver analysis sheet |
| `screenshots/03_talent_segmentation.png` | Segmentation treemap |
| `screenshots/04_retention_recommendations.png` | Strategic recommendations |

---

## 🎨 Design System

| Element | Specification |
|---------|--------------|
| Primary Color | `#1B3A6B` (Deep Navy) |
| Accent Color | `#E84855` (Risk Red) |
| Safe Color | `#2ECC71` (Retention Green) |
| Neutral | `#F4F6F9` (Background) |
| Font | Tableau Book / Roboto |
| Layout | 1200 × 800px fixed |
| Interactivity | Filters, Highlight Actions, URL Actions |
