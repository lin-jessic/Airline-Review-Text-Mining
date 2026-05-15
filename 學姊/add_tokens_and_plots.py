import pandas as pd, re, os
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('sampled_20k_dataset.csv')

# ── 加 tokens 欄位 ────────────────────────────────────────
stemmer = PorterStemmer()

def to_tokens(text):
    words = str(text).lower().split()
    return [stemmer.stem(w) for w in words if len(w) > 1]

df['tokens'] = df['review_cleaned'].apply(to_tokens)
df['token_count'] = df['tokens'].apply(len)

df_save = df.copy()
df_save['tokens'] = df_save['tokens'].apply('|'.join)
df_save.to_csv('sampled_20k_with_tokens.csv', index=False, encoding='utf-8-sig')
print("✓ sampled_20k_with_tokens.csv 存好了")

# ── 5 張圖 ────────────────────────────────────────────────
os.makedirs('figures', exist_ok=True)
sns.set_style("whitegrid")
palette = {"yes": "#4CAF50", "no": "#E53935"}

# Fig 1
fig, ax = plt.subplots(figsize=(7, 4))
counts = df['Recommended'].value_counts().reindex(['yes','no'])
bars = ax.bar(['Recommended (yes)', 'Not Recommended (no)'],
              counts.values, color=[palette['yes'], palette['no']],
              edgecolor='white', width=0.5)
ax.set_title('Recommended Distribution (Sampled 20k)', fontsize=13, fontweight='bold')
ax.set_ylabel('Number of Reviews')
ax.spines[['top','right']].set_visible(False)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.01,
            f"{int(bar.get_height()):,}", ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('figures/fig1_recommended_distribution.png', dpi=150)
plt.close()
print("✓ fig1")

# Fig 2
fig, ax = plt.subplots(figsize=(9, 4))
for label in ['yes','no']:
    vals = df[df['Recommended']==label]['OverallScore'].dropna()
    ax.hist(vals, bins=10, alpha=0.6, color=palette[label],
            label=f'Recommended={label}', edgecolor='white')
ax.set_title('Overall Score Distribution (Sampled 20k)', fontsize=12, fontweight='bold')
ax.set_xlabel('Overall Score (1–10)'); ax.set_ylabel('Count')
ax.legend(); ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig('figures/fig2_rating_distribution.png', dpi=150)
plt.close()
print("✓ fig2")

# Fig 3
fig, ax = plt.subplots(figsize=(9, 4))
for label in ['yes','no']:
    vals = df[df['Recommended']==label]['token_count']
    sns.kdeplot(vals, ax=ax, label=f'Recommended={label}',
                color=palette[label], fill=True, alpha=0.3, linewidth=1.5)
ax.set_title('Token Count Distribution After Preprocessing (Sampled 20k)', fontsize=12, fontweight='bold')
ax.set_xlabel('Tokens per Review'); ax.set_ylabel('Density')
ax.legend(); ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig('figures/fig3_token_count_distribution.png', dpi=150)
plt.close()
print("✓ fig3")

# Fig 4
top15 = df['AirlineName'].value_counts().head(15)
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(top15.index[::-1], top15.values[::-1], color='#1565C0', edgecolor='white')
ax.set_title('Top 15 Airlines (Sampled 20k)', fontsize=12, fontweight='bold')
ax.set_xlabel('Review Count'); ax.spines[['top','right']].set_visible(False)
for bar in bars:
    ax.text(bar.get_width()+5, bar.get_y()+bar.get_height()/2,
            f"{int(bar.get_width()):,}", va='center', fontsize=9)
plt.tight_layout()
plt.savefig('figures/fig4_top_airlines.png', dpi=150)
plt.close()
print("✓ fig4")

# Fig 5
cabin = (df.groupby(['CabinType','Recommended'])
          .size().unstack(fill_value=0)
          .reindex(columns=['yes','no']))
fig, ax = plt.subplots(figsize=(9, 4))
cabin.plot(kind='bar', ax=ax, color=[palette['yes'], palette['no']],
           edgecolor='white', rot=20)
ax.set_title('Cabin Type vs Recommended (Sampled 20k)', fontsize=12, fontweight='bold')
ax.set_xlabel('Cabin Type'); ax.set_ylabel('Count')
ax.legend(title='Recommended'); ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig('figures/fig5_cabin_type_distribution.png', dpi=150)
plt.close()
print("✓ fig5")

print("\n全部完成！")