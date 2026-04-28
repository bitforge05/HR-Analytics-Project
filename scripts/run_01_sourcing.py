import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, seaborn as sns, warnings, os
warnings.filterwarnings('ignore')

plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False})
C = {'p':'#1B3A6B','a':'#E84855','s':'#2ECC71','w':'#F39C12'}

os.makedirs('../data/raw', exist_ok=True)
os.makedirs('../data/processed', exist_ok=True)

df = pd.read_csv('../data/raw/aug_train.csv')
print(f"Shape: {df.shape}")

# Missing audit
audit = pd.DataFrame({
    'dtype': df.dtypes,
    'non_null': df.notnull().sum(),
    'null': df.isnull().sum(),
    'null_pct': (df.isnull().mean()*100).round(2),
    'unique': df.nunique()
})
print(audit.to_string())

# Missing bar chart
fig, ax = plt.subplots(figsize=(10,5))
missing = df.isnull().mean()*100
missing = missing[missing>0].sort_values(ascending=False)
ax.barh(missing.index, missing.values, color=C['a'])
for i,v in enumerate(missing.values):
    ax.text(v+0.3, i, f'{v:.1f}%', va='center', fontsize=9)
ax.set_xlabel('Missing %'); ax.set_title('Missing Values by Column')
plt.tight_layout()
plt.savefig('../data/raw/01_missing_audit.png', dpi=150, bbox_inches='tight')
plt.close()

# Target distribution
tc = df['target'].value_counts()
fig, ax = plt.subplots(1,2, figsize=(12,4))
labels = ['Not Switching','Switching']
ax[0].bar(labels, tc.values, color=[C['s'],C['a']], edgecolor='white')
for i,v in enumerate(tc.values):
    ax[0].text(i, v+100, f'{v:,} ({v/len(df)*100:.1f}%)', ha='center', fontweight='bold')
ax[0].set_title('Target Counts')
ax[1].pie(tc.values, labels=labels, colors=[C['s'],C['a']],
          autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor':'white'})
ax[1].set_title('Target Split')
plt.suptitle('Job Change Intent Distribution', fontweight='bold')
plt.tight_layout()
plt.savefig('../data/raw/01_target_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# Categorical distributions — skip 'city' (123 unique, use CDI proxy)
cat_cols = [c for c in df.select_dtypes('object').columns if c != 'city']
fig, axes = plt.subplots(3,3, figsize=(20,15))
axes = axes.flatten()
for i, col in enumerate(cat_cols):
    vc = df[col].fillna('Missing').value_counts()
    axes[i].barh(vc.index.astype(str), vc.values, color=C['p'], alpha=0.85)
    axes[i].set_title(f'{col} | missing={df[col].isnull().mean()*100:.1f}%')
for j in range(len(cat_cols), len(axes)):
    axes[j].set_visible(False)
plt.suptitle('Categorical Distributions (Raw)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('../data/raw/01_categorical_dist.png', dpi=150, bbox_inches='tight')
plt.close()

# Numeric distributions
fig, axes = plt.subplots(1,2, figsize=(14,5))
for i, col in enumerate(['city_development_index','training_hours']):
    axes[i].hist(df[col].dropna(), bins=40, color=C['p'], alpha=0.85, edgecolor='white')
    axes[i].axvline(df[col].median(), color=C['a'], ls='--', label=f'Median={df[col].median():.2f}')
    axes[i].axvline(df[col].mean(), color=C['s'], ls='-', label=f'Mean={df[col].mean():.2f}')
    axes[i].set_title(col); axes[i].legend()
plt.tight_layout()
plt.savefig('../data/raw/01_numeric_dist.png', dpi=150, bbox_inches='tight')
plt.close()

print("NB01 COMPLETE - 4 charts saved to data/raw/")
