"""Streamlit Data Explorer"""
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Data Explorer", layout="wide")

@st.cache_data
def load_data():
    # Buscar carpeta base 'data engineer'
    current_path = Path(__file__).resolve()
    base = None
    for parent in current_path.parents:
        if parent.name == 'data engineer':
            base = parent
            break
    if base is None:
        st.error("⚠️ No se pudo encontrar la carpeta base")
        st.stop()
    return pd.read_csv(base / '02-analisis-datos/01-eda-exploratorio/proyecto-01-ventas-retail/data/raw/transacciones.csv')

st.title("🔍 Data Explorer Interactivo")

df = load_data()

# Sidebar
st.sidebar.header("Filtros")
columnas = st.sidebar.multiselect("Columnas a mostrar", df.columns.tolist(), default=df.columns.tolist()[:5])

# Main
tab1, tab2, tab3 = st.tabs(["Vista", "Estadísticas", "Búsqueda"])

with tab1:
    st.dataframe(df[columnas], use_container_width=True)

with tab2:
    st.write(df[columnas].describe())

with tab3:
    search = st.text_input("Buscar")
    if search:
        mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        st.dataframe(df[mask])
