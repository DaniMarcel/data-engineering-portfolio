"""FastAPI REST API - Data Engineering"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from pathlib import Path

app = FastAPI(title="Data Engineering API", version="1.0.0")

# Models
class DataQuery(BaseModel):
    limit: Optional[int] = 100
    categoria: Optional[str] = None

class DataResponse(BaseModel):
    total: int
    data: List[dict]

# Load data
def load_data():
    # Buscar carpeta base \'data engineer\'

    current_path = Path(__file__).resolve()

    base_path = None

    for parent in current_path.parents:

        if parent.name == \'data engineer\':

            base_path = parent

            break

    if base_path is None:

        raise FileNotFoundError("No se pudo encontrar la carpeta base \'data engineer\'")
    path = base_path / '02-analisis-datos/01-eda-exploratorio/proyecto-01-ventas-retail/data/raw/transacciones.csv'
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

@app.get("/")
def root():
    return {"message": "Data Engineering API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/transactions", response_model=DataResponse)
def get_transactions(limit: int = 100, categoria: str = None):
    df = load_data()
    
    if categoria:
        df = df[df['categoria'] == categoria]
    
    df_limited = df.head(limit)
    
    return {
        "total": len(df),
        "data": df_limited.to_dict('records')
    }

@app.get("/api/stats")
def get_stats():
    df = load_data()
    
    return {
        "total_transactions": len(df),
        "total_revenue": float(df['total'].sum()),
        "avg_ticket": float(df['total'].mean()),
        "categories": df['categoria'].nunique()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
