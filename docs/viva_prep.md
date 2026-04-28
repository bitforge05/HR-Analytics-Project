# 🎤 Viva Voce & Interview Preparation
## HR Analytics Capstone

### 🎯 The "Evaluator's Favorite" Questions

#### 1. "How did you handle the significant class imbalance in the target variable?"
- **Bad Answer:** "I just used accuracy."
- **Strong Answer:** "I recognized that accuracy would be misleading on a 75/25 split. I prioritized F1-Score and AUC-ROC. During modeling, I used `class_weight='balanced'` in both Logistic Regression and Random Forest to ensure the model learned patterns from the minority 'Switching' class without being overwhelmed by the majority."

#### 2. "Why did you create a custom 'Retention Risk Score' instead of just using the model's probability?"
- **Strong Answer:** "While model probabilities are great for machines, business stakeholders need a transparent, rule-based metric. Our RRS is a weighted composite of CDI, experience, and company size. It provides an immediate 'Tier' (Low/Med/High) that HR can use for policy decisions without needing to run a Python script every time."

#### 3. "What was the most surprising finding in your EDA?"
- **Strong Answer:** "That training hours were not a statistically significant predictor of job change (p=0.051). We expected switchers to be less engaged, but they actually complete similar training hours. This suggests they are using the company's training resources to build skills *for* their next move, emphasizing the need for retention contracts."

#### 4. "How would you deploy this model in a real company?"
- **Strong Answer:** "I would integrate the Random Forest model into the recruitment portal. As candidates apply and progress through training, their risk score would update in real-time on a Tableau dashboard. High-risk candidates could then be flagged for 'Stay Interviews' or mentorship programs mid-training."

---

### 🏛️ Evaluator Critique (Self-Assessment)

**Strengths:**
- **Robust ETL:** Handling missing values contextually (Major vs. Education) instead of just dropping them.
- **Statistical Rigor:** Moving beyond charts to use Chi-Square and Cramér's V.
- **Business Focus:** The final deliverable isn't just a model; it's a dollar-valued recommendation ($4.8M savings).

**Areas for Improvement (Be ready to admit these):**
- **Feature Sparsity:** We lacked salary data, which is often the #1 driver of job change.
- **Temporal Dynamics:** The dataset is a snapshot; we don't see how behavior changes over a 2-year period (Time-series/Survival analysis).

---

### 💡 Pro-Tips for the Viva
- **Know your numbers:** Remember 24.9% (Overall JCR) and 0.814 (RF AUC).
- **The "Business Scientist" Persona:** Don't just talk about hyperparameters; talk about "recruitment cost avoidance."
- **Visual Evidence:** When asked a technical question, point to the specific chart in your report or the Tableau wireframe.
