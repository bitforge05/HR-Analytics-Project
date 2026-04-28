import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, warnings, os
warnings.filterwarnings('ignore')

C = {'p':'#1B3A6B','a':'#E84855','s':'#2ECC71','w':'#F39C12'}
os.makedirs('../data/processed', exist_ok=True)

df = pd.read_csv('../data/raw/aug_train.csv')
df.columns = df.columns.str.strip().str.lower().str.replace(' ','_')
for col in df.select_dtypes('object').columns:
    df[col] = df[col].str.strip()
df = df.drop_duplicates(subset='enrollee_id')
print(f"After dedup: {df.shape}")


df['company_size'] = df['company_size'].fillna('Unknown')
df['company_type'] = df['company_type'].fillna('Unknown')
df['gender'] = df['gender'].fillna('Unknown')
no_major = df['education_level'].isin(['Primary School','High School'])
df.loc[no_major & df['major_discipline'].isnull(), 'major_discipline'] = 'No Major'
df['major_discipline'] = df['major_discipline'].fillna(df['major_discipline'].mode()[0])
for col in ['enrolled_university','education_level','experience','last_new_job']:
    df[col] = df[col].fillna(df[col].mode()[0])
print(f"Nulls remaining: {df.isnull().sum().sum()}")

exp_map = {str(i):i for i in range(1,21)}
exp_map.update({'<1':0,'>20':21})
df['experience_num'] = df['experience'].map(exp_map).astype(float)

edu_map = {'Primary School':1,'High School':2,'Graduate':3,'Masters':4,'Phd':5}
df['education_ordinal'] = df['education_level'].map(edu_map)

lnj_map = {'never':0,'1':1,'2':2,'3':3,'4':4,'>4':5}
df['last_new_job_num'] = df['last_new_job'].map(lnj_map).astype(float)

cs_map = {'Unknown':0,'<10':1,'10/49':2,'50-99':3,'100-500':4,'500-999':5,'1000-4999':6,'5000-9999':7,'10000+':8}
df['company_size_num'] = df['company_size'].map(cs_map).fillna(0)

df['has_relevent_exp'] = (df['relevent_experience']=='Has relevent experience').astype(int)

Q1,Q3 = df['training_hours'].quantile(0.25), df['training_hours'].quantile(0.75)
df['training_hours_capped'] = df['training_hours'].clip(upper=Q3+3*(Q3-Q1))

def exp_band(x):
    if pd.isna(x): return 'Unknown'
    if x==0: return 'Fresher (<1yr)'
    if x<=3: return 'Junior (1-3yr)'
    if x<=7: return 'Mid (4-7yr)'
    if x<=15: return 'Senior (8-15yr)'
    return 'Veteran (>15yr)'
df['experience_band'] = df['experience_num'].apply(exp_band)

def city_tier(cdi):
    if cdi>=0.80: return 'Tier 1 (Developed)'
    if cdi>=0.60: return 'Tier 2 (Developing)'
    return 'Tier 3 (Underdeveloped)'
df['city_tier'] = df['city_development_index'].apply(city_tier)

df['is_stem'] = (df['major_discipline']=='STEM').astype(int)
df['is_enrolled'] = (df['enrolled_university']!='no_enrollment').astype(int)


df['retention_risk_score'] = (
    (1-df['city_development_index'])*3 +
    (8-df['company_size_num'].clip(0,8))*0.5 +
    (21-df['experience_num'].clip(0,21))*0.1 +
    (1-df['has_relevent_exp'])*1.0 +
    (1-df['is_stem'])*0.5
)
rmin,rmax = df['retention_risk_score'].min(), df['retention_risk_score'].max()
df['retention_risk_score'] = ((df['retention_risk_score']-rmin)/(rmax-rmin)*10).round(2)
df['risk_tier'] = pd.cut(df['retention_risk_score'], bins=[0,3.5,6.5,10],
    labels=['Low Risk','Medium Risk','High Risk'], include_lowest=True)

fig, axes = plt.subplots(1,2, figsize=(14,4))
for ax, col, title in zip(axes,['training_hours','training_hours_capped'],['Before','After 3×IQR']):
    ax.hist(df[col], bins=40, color=C['p'], alpha=0.85, edgecolor='white')
    ax.set_title(title); ax.set_xlabel('Training Hours')
plt.suptitle('Outlier Treatment', fontweight='bold')
plt.tight_layout()
plt.savefig('../data/processed/02_outlier_treatment.png', dpi=150, bbox_inches='tight')
plt.close()


df.to_csv('../data/processed/hr_cleaned.csv', index=False)
print(f"hr_cleaned.csv saved: {df.shape}")


ohe_cols = ['gender','enrolled_university','major_discipline','company_type','city_tier']
df_eng = pd.get_dummies(df.copy(), columns=ohe_cols, drop_first=True, dtype=int)
drop_cols = ['enrollee_id','city','relevent_experience','experience','education_level',
             'last_new_job','company_size','training_hours','experience_band','risk_tier']
df_eng = df_eng.drop(columns=[c for c in drop_cols if c in df_eng.columns])
df_eng.to_csv('../data/processed/hr_engineered.csv', index=False)
print(f"hr_engineered.csv saved: {df_eng.shape}")
print("NB02 COMPLETE")