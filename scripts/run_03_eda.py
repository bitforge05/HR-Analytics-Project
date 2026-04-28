import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, seaborn as sns, warnings
warnings.filterwarnings('ignore')

C = {'p':'#1B3A6B','a':'#E84855','s':'#2ECC71','w':'#F39C12'}
plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold'})

df = pd.read_csv('../data/processed/hr_cleaned.csv')
overall_jcr = df['target'].mean()*100
print(f"Loaded {df.shape} | Overall JCR: {overall_jcr:.1f}%")

def jcr_bar(ax, col, title, order=None):
    rates = df.groupby(col)['target'].mean().mul(100).round(1)
    cnts  = df.groupby(col)['target'].count()
    if order:
        rates = rates.reindex([o for o in order if o in rates.index])
        cnts  = cnts.reindex(rates.index)
    colors = [C['a'] if v>overall_jcr else C['p'] for v in rates.values]
    bars = ax.barh(rates.index.astype(str), rates.values, color=colors, alpha=0.88)
    ax.axvline(overall_jcr, color=C['w'], ls='--', lw=1.5, label=f'Overall={overall_jcr:.1f}%')
    ax.set_xlabel('Job Change Rate (%)'); ax.set_title(title)
    for bar,(n,v) in zip(bars, zip(cnts.values, rates.values)):
        ax.text(v+0.3, bar.get_y()+bar.get_height()/2, f'{v:.1f}% (n={n:,})', va='center', fontsize=7)
    ax.legend(fontsize=7)

# Chart 1 - JCR by key segments
exp_order = ['Fresher (<1yr)','Junior (1-3yr)','Mid (4-7yr)','Senior (8-15yr)','Veteran (>15yr)']
edu_order = ['Primary School','High School','Graduate','Masters','Phd']
fig, axes = plt.subplots(2,3, figsize=(22,12))
axes = axes.flatten()
jcr_bar(axes[0],'experience_band','JCR by Experience Band', exp_order)
jcr_bar(axes[1],'city_tier','JCR by City Tier')
jcr_bar(axes[2],'education_level','JCR by Education Level', edu_order)
jcr_bar(axes[3],'company_size','JCR by Company Size')
jcr_bar(axes[4],'company_type','JCR by Company Type')
jcr_bar(axes[5],'enrolled_university','JCR by University Enrollment')
plt.suptitle('Job Change Rate by Key HR Features', fontsize=16, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('../data/processed/03_jcr_by_category.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 1 saved")

# Chart 2 - CDI analysis
fig, axes = plt.subplots(1,2, figsize=(16,5))
for t,color,label in zip([0,1],[C['s'],C['a']],['Not Switching','Switching']):
    sub = df[df['target']==t]
    axes[0].scatter(sub['city_development_index'], sub['training_hours_capped'],
                    alpha=0.12, color=color, s=10, label=label)
axes[0].set_xlabel('City Development Index'); axes[0].set_ylabel('Training Hours')
axes[0].set_title('CDI vs Training Hours by Switch Intent'); axes[0].legend()

df['cdi_bin'] = pd.cut(df['city_development_index'], bins=10)
cdi_jcr = df.groupby('cdi_bin', observed=True)['target'].mean().mul(100)
cdi_mid = [i.mid for i in cdi_jcr.index]
axes[1].plot(cdi_mid, cdi_jcr.values, color=C['a'], lw=2.5, marker='o')
axes[1].fill_between(cdi_mid, cdi_jcr.values, alpha=0.15, color=C['a'])
axes[1].axhline(overall_jcr, color=C['w'], ls='--', label='Overall JCR')
axes[1].set_xlabel('CDI'); axes[1].set_ylabel('JCR (%)'); axes[1].set_title('CDI vs JCR Trend'); axes[1].legend()
plt.suptitle('City Development Index Analysis', fontweight='bold')
plt.tight_layout()
plt.savefig('../data/processed/03_cdi_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 2 saved")

# Chart 3 - Experience deep-dive
fig, axes = plt.subplots(1,2, figsize=(16,5))
exp_jcr = df.groupby('experience_num', observed=True)['target'].mean().mul(100)
axes[0].bar(exp_jcr.index, exp_jcr.values, color=C['p'], alpha=0.8, width=0.7)
axes[0].axhline(overall_jcr, color=C['a'], ls='--', label='Overall JCR')
axes[0].set_xlabel('Years of Experience'); axes[0].set_ylabel('JCR (%)'); axes[0].set_title('Granular JCR by Experience Years'); axes[0].legend()

eb_ct = df.groupby(['experience_band','target'], observed=True).size().unstack(fill_value=0)
eb_ct = eb_ct.reindex([o for o in exp_order if o in eb_ct.index])
eb_pct = eb_ct.div(eb_ct.sum(axis=1), axis=0)*100
eb_pct[[0,1]].plot(kind='bar', stacked=True, ax=axes[1], color=[C['s'],C['a']], edgecolor='white')
axes[1].set_title('Switch Composition by Experience Band')
axes[1].set_ylabel('% of Candidates'); axes[1].legend(['Not Switching','Switching']); axes[1].tick_params(axis='x', rotation=25)
plt.suptitle('Experience-Based Analysis', fontweight='bold')
plt.tight_layout()
plt.savefig('../data/processed/03_experience_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 3 saved")

# Chart 4 - Risk score
fig, axes = plt.subplots(1,3, figsize=(18,5))
for t,color,label in zip([0,1],[C['s'],C['a']],['Not Switching','Switching']):
    axes[0].hist(df[df['target']==t]['retention_risk_score'], bins=30, alpha=0.6, color=color, label=label, density=True)
axes[0].set_xlabel('Retention Risk Score (0-10)'); axes[0].set_ylabel('Density'); axes[0].set_title('Risk Score by Intent'); axes[0].legend()

tier_jcr = df.groupby('risk_tier', observed=True)['target'].mean().mul(100)
tier_cnt = df.groupby('risk_tier', observed=True)['target'].count()
tier_colors = [C['s'],C['w'],C['a']]
bars = axes[1].bar(tier_jcr.index.astype(str), tier_jcr.values, color=tier_colors, edgecolor='white')
for bar,v,n in zip(bars, tier_jcr.values, tier_cnt.values):
    axes[1].text(bar.get_x()+bar.get_width()/2, v+0.5, f'{v:.1f}%\n(n={n:,})', ha='center', fontsize=8, fontweight='bold')
axes[1].set_title('JCR by Risk Tier'); axes[1].set_ylabel('JCR (%)')

tc = df['risk_tier'].value_counts().reindex(['Low Risk','Medium Risk','High Risk'])
axes[2].pie(tc.values, labels=tc.index, colors=tier_colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor':'white'})
axes[2].set_title('Candidate Distribution by Risk Tier')
plt.suptitle('Retention Risk Score Analysis', fontweight='bold')
plt.tight_layout()
plt.savefig('../data/processed/03_risk_score_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 4 saved")

# Chart 5 - Correlation heatmap
num_features = ['city_development_index','training_hours_capped','experience_num','education_ordinal',
                'last_new_job_num','company_size_num','has_relevent_exp','is_stem','is_enrolled',
                'retention_risk_score','target']
corr = df[num_features].corr()
fig, ax = plt.subplots(figsize=(12,9))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            linewidths=0.5, ax=ax, annot_kws={'size':8})
ax.set_title('Correlation Heatmap — All Features vs Target', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('../data/processed/03_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 5 saved")
print("\nTop correlations with target:")
print(corr['target'].drop('target').sort_values(key=abs, ascending=False))

# Chart 6 - Demographics
fig, axes = plt.subplots(1,3, figsize=(20,6))
disc_jcr = df.groupby('major_discipline')['target'].mean().mul(100).sort_values()
axes[0].barh(disc_jcr.index, disc_jcr.values, color=[C['a'] if v>overall_jcr else C['p'] for v in disc_jcr.values], alpha=0.88)
axes[0].axvline(overall_jcr, color=C['w'], ls='--'); axes[0].set_title('JCR by Major Discipline'); axes[0].set_xlabel('JCR (%)')

gender_jcr = df.groupby('gender')['target'].mean().mul(100)
axes[1].bar(gender_jcr.index, gender_jcr.values, color=C['p'], alpha=0.85, edgecolor='white')
axes[1].axhline(overall_jcr, color=C['a'], ls='--', label='Overall JCR')
for i,(g,v) in enumerate(gender_jcr.items()): axes[1].text(i, v+0.3, f'{v:.1f}%', ha='center', fontweight='bold')
axes[1].set_title('JCR by Gender'); axes[1].set_ylabel('JCR (%)'); axes[1].legend()

ct2 = df.groupby(['company_type','target']).size().unstack(fill_value=0)
ct2_pct = ct2.div(ct2.sum(axis=1), axis=0)*100
ct2_pct[[0,1]].plot(kind='bar', stacked=True, ax=axes[2], color=[C['s'],C['a']], edgecolor='white')
axes[2].set_title('Switch Intent by Company Type'); axes[2].set_ylabel('%'); axes[2].legend(['Not Switching','Switching']); axes[2].tick_params(axis='x', rotation=30)
plt.suptitle('Demographics & Background Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('../data/processed/03_demographics_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 6 saved")
print("NB03 COMPLETE - 6 charts saved")
