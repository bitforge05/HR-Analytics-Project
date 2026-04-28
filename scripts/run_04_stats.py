import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, seaborn as sns, warnings
from scipy.stats import chi2_contingency, mannwhitneyu, pointbiserialr
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, f1_score, confusion_matrix
warnings.filterwarnings('ignore')

matplotlib.use('Agg')
C = {'p':'#1B3A6B','a':'#E84855','s':'#2ECC71','w':'#F39C12'}
plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False})

df     = pd.read_csv('../data/processed/hr_cleaned.csv')
df_eng = pd.read_csv('../data/processed/hr_engineered.csv')
print(f"Analytical df: {df.shape} | Engineered: {df_eng.shape}")


def cramers_v(x,y):
    ct = pd.crosstab(x,y)
    chi2,_,_,_ = chi2_contingency(ct)
    n = ct.sum().sum()
    phi2 = chi2/n
    r,k = ct.shape
    phi2c = max(0, phi2-(k-1)*(r-1)/(n-1))
    rc = r-(r-1)**2/(n-1); kc = k-(k-1)**2/(n-1)
    return np.sqrt(phi2c/min(kc-1,rc-1))

results = []
ct1 = pd.crosstab(df['city_tier'], df['target'])
chi2,p,dof,_ = chi2_contingency(ct1)
cv = cramers_v(df['city_tier'], df['target'])
results.append(('H1: City Tier ↔ Job Change','Chi-Square',f'χ²={chi2:.2f}',f'p={p:.3e}',f"V={cv:.3f}",'✅ REJECT' if p<0.05 else '❌ FAIL'))

ct2 = pd.crosstab(df['experience_band'], df['target'])
chi2b,p2,_,_ = chi2_contingency(ct2)
cv2 = cramers_v(df['experience_band'], df['target'])
results.append(('H2: Experience Band ↔ Job Change','Chi-Square',f'χ²={chi2b:.2f}',f'p={p2:.3e}',f"V={cv2:.3f}",'✅ REJECT' if p2<0.05 else '❌ FAIL'))

ct3 = pd.crosstab(df['is_stem'], df['target'])
chi2c,p3,_,_ = chi2_contingency(ct3)
cv3 = cramers_v(df['is_stem'], df['target'])
results.append(('H3: STEM Major ↔ Job Change','Chi-Square',f'χ²={chi2c:.2f}',f'p={p3:.3e}',f"V={cv3:.3f}",'✅ REJECT' if p3<0.05 else '❌ FAIL'))

sw  = df[df['target']==1]['training_hours_capped']
nsw = df[df['target']==0]['training_hours_capped']
u,p4 = mannwhitneyu(sw, nsw, alternative='two-sided')
results.append(('H4: Training Hours diff by Target','Mann-Whitney U',f'U={u:.0f}',f'p={p4:.3e}','—','✅ REJECT' if p4<0.05 else '❌ FAIL'))

rpb,p5 = pointbiserialr(df['target'], df['city_development_index'])
results.append(('H5: CDI correlation with Target','Point-Biserial r',f'r={rpb:.4f}',f'p={p5:.3e}','—','✅ REJECT' if p5<0.05 else '❌ FAIL'))

ct6 = pd.crosstab(df['company_size'], df['target'])
chi2d,p6,_,_ = chi2_contingency(ct6)
cv6 = cramers_v(df['company_size'], df['target'])
results.append(('H6: Company Size ↔ Job Change','Chi-Square',f'χ²={chi2d:.2f}',f'p={p6:.3e}',f"V={cv6:.3f}",'✅ REJECT' if p6<0.05 else '❌ FAIL'))

print("\n" + "="*90)
print("  HYPOTHESIS TEST RESULTS")
print("="*90)
res_df = pd.DataFrame(results, columns=['Hypothesis','Test','Statistic','P-Value','Effect Size','Decision'])
print(res_df.to_string(index=False))
res_df.to_csv('../data/processed/04_hypothesis_results.csv', index=False)


cat_features = ['city_tier','experience_band','education_level','company_type',
                'company_size','enrolled_university','major_discipline','gender']
es = {col: cramers_v(df[col], df['target']) for col in cat_features}
es_df = pd.Series(es).sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(11,5))
colors = [C['a'] if v>0.1 else C['p'] for v in es_df.values]
ax.barh(es_df.index, es_df.values, color=colors, alpha=0.88)
ax.axvline(0.1, color=C['w'], ls='--', lw=1.5, label='Weak (0.1)')
ax.axvline(0.3, color=C['a'], ls='--', lw=1.5, label='Moderate (0.3)')
for i,v in enumerate(es_df.values): ax.text(v+0.003, i, f'{v:.3f}', va='center', fontsize=9)
ax.set_xlabel("Cramér's V"); ax.set_title("Effect Size: Cramér's V for Categorical Features vs Target", fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('../data/processed/04_cramers_v.png', dpi=150, bbox_inches='tight')
plt.close()
print("Cramér's V chart saved")


X = df_eng.drop(columns=['target'])
y = df_eng['target']
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

scaler = StandardScaler()
Xtr_sc = scaler.fit_transform(X_train)
Xte_sc = scaler.transform(X_test)


lr = LogisticRegression(class_weight='balanced', max_iter=500, random_state=42, C=0.5)
lr.fit(Xtr_sc, y_train)
y_pred_lr = lr.predict(Xte_sc)
y_prob_lr = lr.predict_proba(Xte_sc)[:,1]
print("\nLogistic Regression:")
print(classification_report(y_test, y_pred_lr, target_names=['Not Switching','Switching']))
print(f"AUC-ROC: {roc_auc_score(y_test, y_prob_lr):.4f}")


coef_df = pd.DataFrame({'Feature':X.columns,'Coef':lr.coef_[0]}).sort_values('Coef',key=abs,ascending=False).head(15)
fig, ax = plt.subplots(figsize=(12,7))
ax.barh(coef_df['Feature'], coef_df['Coef'], color=[C['a'] if c>0 else C['p'] for c in coef_df['Coef']], alpha=0.88)
ax.axvline(0, color='black', lw=0.8)
ax.set_xlabel('Coefficient'); ax.set_title('Top 15 Logistic Regression Coefficients\n(Red = increases job-change probability)', fontweight='bold')
plt.tight_layout()
plt.savefig('../data/processed/04_lr_coefficients.png', dpi=150, bbox_inches='tight')
plt.close()


rf = RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42, max_depth=10, min_samples_leaf=20, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
y_prob_rf  = rf.predict_proba(X_test)[:,1]
print("\nRandom Forest:")
print(classification_report(y_test, y_pred_rf, target_names=['Not Switching','Switching']))
print(f"AUC-ROC: {roc_auc_score(y_test, y_prob_rf):.4f}")


fi_df = pd.DataFrame({'Feature':X.columns,'Importance':rf.feature_importances_}).sort_values('Importance',ascending=False).head(15)
fig, ax = plt.subplots(figsize=(12,7))
ax.barh(fi_df['Feature'][::-1], fi_df['Importance'][::-1], color=C['p'], alpha=0.88)
ax.set_xlabel('Feature Importance (Gini)'); ax.set_title('Top 15 Feature Importances — Random Forest', fontweight='bold')
plt.tight_layout()
plt.savefig('../data/processed/04_rf_feature_importance.png', dpi=150, bbox_inches='tight')
plt.close()


fig, ax = plt.subplots(figsize=(8,7))
for name, yp in [('Logistic Regression',y_prob_lr),('Random Forest',y_prob_rf)]:
    fpr,tpr,_ = roc_curve(y_test,yp)
    ax.plot(fpr,tpr,lw=2,label=f'{name} (AUC={roc_auc_score(y_test,yp):.3f})')
ax.plot([0,1],[0,1],color='grey',ls='--'); ax.set_xlabel('FPR'); ax.set_ylabel('TPR')
ax.set_title('ROC Curve — Model Comparison', fontweight='bold'); ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig('../data/processed/04_roc_comparison.png', dpi=150, bbox_inches='tight')
plt.close()


fig, axes = plt.subplots(1,2, figsize=(14,5))
for ax,(name,yp) in zip(axes,[('Logistic Regression',y_pred_lr),('Random Forest',y_pred_rf)]):
    cm = confusion_matrix(y_test,yp)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['Not Switch','Switch'], yticklabels=['Not Switch','Switch'])
    ax.set_title(f'{name}'); ax.set_ylabel('Actual'); ax.set_xlabel('Predicted')
plt.suptitle('Confusion Matrices', fontweight='bold')
plt.tight_layout()
plt.savefig('../data/processed/04_confusion_matrices.png', dpi=150, bbox_inches='tight')
plt.close()

print("\n" + "="*60)
print("  MODEL SUMMARY")
print("="*60)
print(f"  {'Model':<22} {'F1':>8} {'AUC-ROC':>10}")
print(f"  {'Logistic Regression':<22} {f1_score(y_test,y_pred_lr):>8.4f} {roc_auc_score(y_test,y_prob_lr):>10.4f}")
print(f"  {'Random Forest':<22} {f1_score(y_test,y_pred_rf):>8.4f} {roc_auc_score(y_test,y_prob_rf):>10.4f}")
print("NB04 COMPLETE - 5 charts + hypothesis CSV saved")
