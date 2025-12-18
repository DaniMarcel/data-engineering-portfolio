"""K-Means Clustering for Customer Segmentation"""
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load data
# Buscar carpeta base \'data engineer\'

current_path = Path(__file__).resolve()

base_path = None

for parent in current_path.parents:

    if parent.name == \'data engineer\':

        base_path = parent

        break

if base_path is None:

    raise FileNotFoundError("No se pudo encontrar la carpeta base \'data engineer\'")
df = pd.read_csv(base_path / '02-analisis-datos/01-eda-exploratorio/proyecto-01-ventas-retail/data/raw/transacciones.csv')

# Prepare features: aggregate by customer
customer_features = df.groupby('cliente_id').agg({
    'total': ['sum', 'mean', 'count'],
    'cantidad': 'sum'
}).reset_index()

customer_features.columns = ['cliente_id', 'total_spent', 'avg_purchase', 'num_purchases', 'total_items']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(customer_features[['total_spent', 'avg_purchase', 'num_purchases']])

# K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
customer_features['cluster'] = kmeans.fit_predict(X_scaled)

# Results
print("✅ Clustering completed!")
print(f"\nCluster distribution:")
print(customer_features['cluster'].value_counts().sort_index())

print(f"\nCluster statistics:")
for cluster in range(3):
    cluster_data = customer_features[customer_features['cluster'] == cluster]
    print(f"\nCluster {cluster}:")
    print(f"  Customers: {len(cluster_data)}")
    print(f"  Avg spent: €{cluster_data['total_spent'].mean():.2f}")
    print(f"  Avg purchases: {cluster_data['num_purchases'].mean():.1f}")

# Save results
customer_features.to_csv('customer_segments.csv', index=False)
print(f"\n💾 Results saved to customer_segments.csv")
