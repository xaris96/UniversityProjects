# clustering_more_clusters_and_examples.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os

# ----------------------------
# Ρυθμίσεις (προσαρμόζεις εδώ)
# ----------------------------
csv_path = r"C:\Users\xaris\OneDrive\Υπολογιστής\data science\baskets.csv"
sep = ';'                      # αν χρειαστεί άλλαξε σε ',' ή '\t'
numeric_features = ['Total_Basket_Value', 'Total_Items', 'DistinctSKUs',
                    'UniqueCategories', 'AvgPricePerItem', 'CategoryTopShare']

# Πώς θα επιλέξουμε k
min_k = 2
max_k = 12                    # άλλαξε εδώ για να δοκιμάσεις έως π.χ. 12 clusters
sample_for_k = 5000           # μέγεθος δείγματος για γρήγορη εκτίμηση Silhouette (μικρό→γρήγορο)
# Πόσα παραδείγματα ανά cluster εξάγουμε
examples_per_cluster = 30     # άλλαξε εδώ (π.χ. 30, 50)
# Τρόπος επιλογής παραδειγμάτων: 'random' ή 'representative'
examples_mode = 'representative'  # 'random' ή 'representative'

# Αρχεία εξόδου
out_examples_csv = r"C:\Users\xaris\OneDrive\Υπολογιστής\data science\cluster_examples.csv"
out_full_csv = r"C:\Users\xaris\OneDrive\Υπολογιστής\data science\baskets_with_clusters.csv"
out_report_csv = r"C:\Users\xaris\OneDrive\Υπολογιστής\data science\cluster_report.csv"

# ----------------------------
# 1) Φόρτωση CSV
# ----------------------------
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Το αρχείο δεν βρέθηκε: {csv_path}")

print("Reading CSV:", csv_path)
df = pd.read_csv(csv_path, sep=sep)
print("Loaded shape:", df.shape)
print("Columns:", df.columns.tolist())

# ----------------------------
# 2) Ensure numeric columns are floats (ελληνικά decimals -> dot)
# ----------------------------
for col in numeric_features:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")
    df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')

df[numeric_features] = df[numeric_features].fillna(0)

# ----------------------------
# 3) Normalization
# ----------------------------
X = df[numeric_features].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Normalization done.")

# ----------------------------
# 4) Επιλογή k (Silhouette) σε δείγμα
# ----------------------------
sample_size = min(sample_for_k, len(df))
if sample_size < 1000:
    print(f"Using sample size {sample_size} for silhouette (dataset small).")
else:
    print(f"Using sample size {sample_size} for silhouette (speedup).")

# build sample indices (keep alignment with X_scaled)
rng = np.random.default_rng(42)
sample_idx = rng.choice(len(df), size=sample_size, replace=False)
X_sample = X_scaled[sample_idx]

best_k = None
best_score = -1.0
sil_scores = {}

print("Estimating best k by Silhouette (k in [{}, {}])...".format(min_k, max_k))
for k in range(min_k, max_k + 1):
    try:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_sample)
        score = silhouette_score(X_sample, labels)
        sil_scores[k] = score
        print(f"  k={k} -> silhouette={score:.4f}")
        if score > best_score:
            best_score = score
            best_k = k
    except Exception as e:
        print(f"  k={k} failed: {e}")
        continue

if best_k is None:
    # fallback
    best_k = min_k
    print("Silhouette failed for all k: fallback to k=", best_k)
else:
    print(f"Selected best_k={best_k} with silhouette={best_score:.4f}")

# ----------------------------
# 5) KMeans στο full dataset
# ----------------------------
print("Fitting KMeans on FULL dataset with k =", best_k)
kmeans_full = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df['cluster'] = kmeans_full.fit_predict(X_scaled)
print("Clustering finished. Cluster counts:")
print(df['cluster'].value_counts())

# Αποθήκευση πλήρους dataset με cluster labels
df.to_csv(out_full_csv, index=False)
print("Saved full dataset with clusters to:", out_full_csv)

# ----------------------------
# 6) Rule-based περιγραφή clusters
# ----------------------------
cluster_summary = df.groupby('cluster')[numeric_features].agg(['mean','median','std','count']).round(3)
cluster_summary_flat = df.groupby('cluster')[numeric_features].mean().round(3)
cluster_summary.to_csv(out_report_csv)
print("Saved cluster summary report to:", out_report_csv)
print("\nCluster means (short):")
print(cluster_summary_flat)

overall_mean = df[numeric_features].mean()

cluster_rules = {}
for cluster_id, row in cluster_summary_flat.iterrows():
    rules = []
    for feature in numeric_features:
        if row[feature] > overall_mean[feature]:
            rules.append(f"{feature} υψηλό")
        else:
            rules.append(f"{feature} χαμηλό")
    cluster_rules[cluster_id] = ", ".join(rules)

print("\nRule-based descriptions:")
for cid, rule in cluster_rules.items():
    print(f" Cluster {cid}: {rule}")

# ----------------------------
# 7) Παραδείγματα ανά cluster
# ----------------------------
def safe_random_sample(group, n):
    return group.sample(n=min(len(group), n), random_state=42)

def representative_sample(group, n, cluster_id, X_scaled_local, centroids):
    # υποθέτουμε group.indices αντιστοιχούν σε df.index
    idxs = group.index.to_numpy()
    # compute distances of these indices to centroid
    dists = np.linalg.norm(X_scaled_local[idxs] - centroids[cluster_id], axis=1)
    order = np.argsort(dists)
    chosen = idxs[order[:min(len(order), n)]]
    return df.loc[chosen]

examples_list = []
centroids = kmeans_full.cluster_centers_

for cid in sorted(df['cluster'].unique()):
    group = df[df['cluster'] == cid]
    if examples_mode == 'random':
        sample = safe_random_sample(group, examples_per_cluster)
    else:  # representative
        sample = representative_sample(group, examples_per_cluster, cid, X_scaled, centroids)
    sample = sample.copy()
    sample['cluster'] = cid
    examples_list.append(sample)

examples_df = pd.concat(examples_list, ignore_index=True)
examples_df.to_csv(out_examples_csv, index=False)
print(f"\nSaved {len(examples_df)} example rows to: {out_examples_csv}")
print("Examples per cluster (counts):")
print(examples_df['cluster'].value_counts())

print("\nDone.")
