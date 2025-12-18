"""Time Series Forecasting with Prophet"""
from prophet import Prophet
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

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
df['fecha'] = pd.to_datetime(df['fecha'])

# Aggregate by date
daily = df.groupby('fecha')['total'].sum().reset_index()
daily.columns = ['ds', 'y']

# Fit model
model = Prophet()
model.fit(daily)

# Forecast
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Plot
fig = model.plot(forecast)
plt.title('Sales Forecast - Next 30 Days')
plt.tight_layout()
plt.savefig('forecast.png', dpi=300)
print("✅ Forecast completed!")
print(f"Last actual: €{daily['y'].iloc[-1]:.2f}")
print(f"Next 30d avg forecast: €{forecast['yhat'].tail(30).mean():.2f}")
