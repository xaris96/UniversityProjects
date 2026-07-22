import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

data = pd.read_csv("POS_data_python.csv")

X = data[["total_value", "total_units", "unique_products", "unique_categories", "used_loyalty_card", "avg_value_per_product"]].dropna()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42)
data["Cluster"] = kmeans.fit_predict(X_scaled)

# Αποθήκευση πίσω στο CSV
data.to_csv("Basket_Summary_withClusters.csv", index=False)
