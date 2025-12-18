"""Basic Regression with scikit-learn"""
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from pathlib import Path

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

# Prepare data
X = df[['cantidad', 'precio_unitario']]
y = df['total']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"✅ Model trained!")
print(f"R²: {r2_score(y_test, y_pred):.4f}")
print(f"RMSE: {mean_squared_error(y_test, y_pred, squared=False):.2f}")
