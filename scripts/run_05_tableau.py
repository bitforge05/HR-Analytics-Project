import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, warnings
warnings.filterwarnings('ignore')

C = {'p':'#1B3A6B','a':'#E84855','s':'#2ECC71','w':'#F39C12'}
plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold'})

df = pd.read_csv('../data/processed/hr_cleaned.csv')

# ── Build Tableau dataset ───────────────────────────────────────────────
tableau = df[[
    'enrollee_id','city','city_development_index','city_tier',
    'gender','relevent_experience','has_relevent_exp',
    'enrolled_university','is_enrolled',
    'education_level','education_ordinal',
    'major_discipline','is_stem',
    'experience','experience_num','experience_band',
    'company_size','company_size_num','company_type',
    'last_new_job','last_new_job_num',
    'training_hours','training_hours_capped',
    'retention_risk_score','risk_tier','target'
]].copy()

rename_map = {
    'enrollee_id':'Candidate_ID','city':'City_Code',
    'city_development_index':'City_Development_Index','city_tier':'City_Tier',
    'gender':'Gender','relevent_experience':'Relevant_Experience_Raw',
    'has_relevent_exp':'Has_Relevant_Experience',
    'enrolled_university':'University_Enrollment','is_enrolled':'Is_Enrolled_University',
    'education_level':'Education_Level','education_ordinal':'Education_Score',
    'major_discipline':'Major_Discipline','is_stem':'Is_STEM',
    'experience':'Experience_Raw','experience_num':'Experience_Years',
    'experience_band':'Experience_Band','company_size':'Company_Size',
    'company_size_num':'Company_Size_Score','company_type':'Company_Type',
    'last_new_job':'Last_Job_Gap','last_new_job_num':'Last_Job_Gap_Years',
    'training_hours':'Training_Hours_Raw','training_hours_capped':'Training_Hours',
    'retention_risk_score':'Retention_Risk_Score','risk_tier':'Risk_Tier','target':'Job_Change_Intent'
}
tableau = tableau.rename(columns=rename_map)
tableau['Job_Change_Label'] = tableau['Job_Change_Intent'].map({0:'Not Switching',1:'Switching'})
tableau['Overall_JCR_Pct'] = round(tableau['Job_Change_Intent'].mean()*100, 2)
t_min,t_max = tableau['Training_Hours'].min(), tableau['Training_Hours'].max()
tableau['Training_Intensity'] = ((tableau['Training_Hours']-t_min)/(t_max-t_min)).round(4)
tableau['CDI_Band'] = pd.cut(tableau['City_Development_Index'],
    bins=[0,0.55,0.65,0.75,0.85,1.0],
    labels=['<0.55','0.55-0.65','0.65-0.75','0.75-0.85','>0.85']).astype(str)
tableau['Is_High_Risk'] = (tableau['Risk_Tier']=='High Risk').astype(int)

tableau.to_csv('../data/processed/hr_tableau_ready.csv', index=False)
print(f"hr_tableau_ready.csv saved: {tableau.shape}")

# ── KPI Validation Dashboard ────────────────────────────────────────────
exp_order = ['Fresher (<1yr)','Junior (1-3yr)','Mid (4-7yr)','Senior (8-15yr)','Veteran (>15yr)']
edu_order = ['Primary School','High School','Graduate','Masters','Phd']
overall   = tableau['Job_Change_Intent'].mean()*100

fig, axes = plt.subplots(2,3, figsize=(22,12))
axes = axes.flatten()

# KPI 1
ct_jcr = tableau.groupby('City_Tier')['Job_Change_Intent'].mean().mul(100).sort_values()
axes[0].bar(ct_jcr.index, ct_jcr.values, color=[C['s'],C['w'],C['a']], edgecolor='white')
for i,v in enumerate(ct_jcr.values): axes[0].text(i, v+0.5, f'{v:.1f}%', ha='center', fontweight='bold')
axes[0].set_title('KPI 1: JCR by City Tier'); axes[0].set_ylabel('JCR (%)')

# KPI 2
eb_jcr = tableau.groupby('Experience_Band')['Job_Change_Intent'].mean().mul(100)
eb_jcr = eb_jcr.reindex([o for o in exp_order if o in eb_jcr.index])
axes[1].bar(range(len(eb_jcr)), eb_jcr.values, color=C['p'], alpha=0.85, edgecolor='white')
axes[1].set_xticks(range(len(eb_jcr)))
axes[1].set_xticklabels(eb_jcr.index, rotation=25, fontsize=8)
for i,v in enumerate(eb_jcr.values): axes[1].text(i, v+0.3, f'{v:.1f}%', ha='center', fontsize=8)
axes[1].set_title('KPI 2: JCR by Experience Band'); axes[1].set_ylabel('JCR (%)')

# KPI 3
rt_c = tableau['Risk_Tier'].value_counts().reindex(['Low Risk','Medium Risk','High Risk'])
axes[2].pie(rt_c.values, labels=rt_c.index, colors=[C['s'],C['w'],C['a']],
            autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor':'white'})
axes[2].set_title('KPI 3: Risk Tier Distribution')

# KPI 4
rr_bins = pd.cut(tableau['Retention_Risk_Score'], bins=8)
rr_jcr = tableau.groupby(rr_bins, observed=True)['Job_Change_Intent'].mean().mul(100)
axes[3].plot(range(len(rr_jcr)), rr_jcr.values, color=C['a'], lw=2.5, marker='o')
axes[3].set_title('KPI 4: Risk Score vs JCR'); axes[3].set_ylabel('JCR (%)'); axes[3].set_xlabel('Risk Score Bin')

# KPI 5
comp_jcr = tableau.groupby('Company_Type')['Job_Change_Intent'].mean().mul(100).sort_values()
axes[4].barh(comp_jcr.index, comp_jcr.values, color=C['p'], alpha=0.85)
for i,v in enumerate(comp_jcr.values): axes[4].text(v+0.2, i, f'{v:.1f}%', va='center', fontsize=8)
axes[4].set_title('KPI 5: JCR by Company Type'); axes[4].set_xlabel('JCR (%)')

# KPI 6
edu_jcr = tableau.groupby('Education_Level')['Job_Change_Intent'].mean().mul(100)
edu_jcr = edu_jcr.reindex([o for o in edu_order if o in edu_jcr.index])
axes[5].bar(range(len(edu_jcr)), edu_jcr.values, color=C['p'], alpha=0.85, edgecolor='white')
axes[5].set_xticks(range(len(edu_jcr)))
axes[5].set_xticklabels(edu_jcr.index, rotation=20, fontsize=8)
for i,v in enumerate(edu_jcr.values):
    if not np.isnan(v): axes[5].text(i, v+0.3, f'{v:.1f}%', ha='center', fontsize=8)
axes[5].set_title('KPI 6: JCR by Education Level'); axes[5].set_ylabel('JCR (%)')

plt.suptitle('KPI Validation Dashboard — Pre-Tableau Check', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('../data/processed/05_kpi_validation_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()

print("\n" + "="*60)
print("  FINAL DATA QUALITY CHECK")
print("="*60)
print(f"  Rows             : {len(tableau):,}")
print(f"  Columns          : {len(tableau.columns)}")
print(f"  Null values      : {tableau.isnull().sum().sum()}")
print(f"  Duplicate IDs    : {tableau.duplicated('Candidate_ID').sum()}")
print(f"  Job Change Rate  : {tableau['Job_Change_Intent'].mean()*100:.2f}%")
print(f"  High-Risk Count  : {tableau['Is_High_Risk'].sum():,} ({tableau['Is_High_Risk'].mean()*100:.1f}%)")
print(f"  Avg Risk Score   : {tableau['Retention_Risk_Score'].mean():.2f}/10")
print(f"  Avg Train Hours  : {tableau['Training_Hours'].mean():.1f}")
print("="*60)
print("\nNB05 COMPLETE — hr_tableau_ready.csv exported!")
print("\nIMPORT INSTRUCTIONS:")
print("  Tableau Desktop → Connect → Text File → hr_tableau_ready.csv")
