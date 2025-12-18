"""REST Data Service with Flask"""
from flask import Flask, jsonify, request
import pandas as pd
from pathlib import Path

app = Flask(__name__)

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

@app.route('/api/data')
def get_data():
    limit = request.args.get('limit', 100, type=int)
    return jsonify(df.head(limit).to_dict('records'))

@app.route('/api/stats')
def get_stats():
    return jsonify({
        'total': len(df),
        'revenue': float(df['total'].sum()),
        'avg': float(df['total'].mean())
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
