"""
Dashboard Interactivo de Ventas con Streamlit
==============================================

Dashboard profesional para visualizar y analizar datos de ventas en tiempo real.
Incluye filtros interactivos, métricas clave y múltiples visualizaciones.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def cargar_datos():
    """Carga los datos de ventas."""
    # Buscar la carpeta base 'data engineer' en el path
    current_path = Path(__file__).resolve()
    base_path = None
    
    # Buscar hacia arriba hasta encontrar 'data engineer'
    for parent in current_path.parents:
        if parent.name == 'data engineer':
            base_path = parent
            break
    
    if base_path is None:
        st.error("⚠️ No se pudo encontrar la carpeta base 'data engineer'")
        st.stop()
    
    data_path = base_path / '02-analisis-datos' / '01-eda-exploratorio' / 'proyecto-01-ventas-retail' / 'data' / 'raw'
    
    try:
        transacciones = pd.read_csv(data_path / 'transacciones.csv')
        clientes = pd.read_csv(data_path / 'clientes.csv')
        productos = pd.read_csv(data_path / 'productos.csv')
        
        # Convertir fechas
        transacciones['fecha'] = pd.to_datetime(transacciones['fecha'])
        
        return transacciones, clientes, productos
    except FileNotFoundError:
        st.error("⚠️ No se encontraron los datos. Ejecuta primero el generador de datos del proyecto EDA.")
        st.stop()


def calcular_metricas(df):
    """Calcula métricas clave del negocio."""
    total_ingresos = df['total'].sum()
    total_transacciones = len(df)
    ticket_promedio = df['total'].mean()
    total_productos = df['cantidad'].sum()
    
    return {
        'ingresos': total_ingresos,
        'transacciones': total_transacciones,
        'ticket_promedio': ticket_promedio,
        'productos': total_productos
    }


def crear_grafico_tendencia(df):
    """Crea gráfico de tendencia de ventas."""
    ventas_diarias = df.groupby('fecha')['total'].sum().reset_index()
    
    fig = px.line(
        ventas_diarias,
        x='fecha',
        y='total',
        title='📈 Tendencia de Ventas Diarias',
        labels={'fecha': 'Fecha', 'total': 'Ingresos (€)'}
    )
    
    fig.update_traces(line_color='#1f77b4', line_width=2)
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='white',
        height=400
    )
    
    return fig


def crear_grafico_categorias(df):
    """Crea gráfico de ventas por categoría."""
    ventas_cat = df.groupby('categoria')['total'].sum().reset_index()
    ventas_cat = ventas_cat.sort_values('total', ascending=False)
    
    fig = px.bar(
        ventas_cat,
        x='categoria',
        y='total',
        title='📦 Ingresos por Categoría',
        labels={'categoria': 'Categoría', 'total': 'Ingresos (€)'},
        color='total',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        height=400
    )
    
    return fig


def crear_grafico_top_productos(df, n=10):
    """Crea gráfico de top productos."""
    top_productos = df.groupby('producto_nombre')['total'].sum().nlargest(n).reset_index()
    
    fig = px.bar(
        top_productos,
        y='producto_nombre',
        x='total',
        orientation='h',
        title=f'🏆 Top {n} Productos Más Vendidos',
        labels={'producto_nombre': 'Producto', 'total': 'Ingresos (€)'},
        color='total',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


def crear_grafico_pie_canales(df):
    """Crea gráfico pie de canales de venta."""
    ventas_canal = df.groupby('canal')['total'].sum().reset_index()
    
    fig = px.pie(
        ventas_canal,
        values='total',
        names='canal',
        title='💻 Distribución por Canal de Venta',
        hole=0.4
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    return fig


def crear_mapa_calor_ventas(df):
    """Crea mapa de calor de ventas por día y hora."""
    # Extraer día de semana y hora
    df['dia'] = df['fecha'].dt.day_name()
    df['hora'] = df['hora'].str[:2].astype(int)
    
    # Crear pivot table
    heatmap_data = df.groupby(['dia', 'hora'])['total'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='dia', columns='hora', values='total')
    
    # Ordenar días de la semana
    dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_pivot = heatmap_pivot.reindex(dias_orden)
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
        colorscale='RdYlGn',
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='🔥 Mapa de Calor: Ventas por Día y Hora',
        xaxis_title='Hora del Día',
        yaxis_title='Día de la Semana',
        height=400
    )
    
    return fig


def main():
    """Función principal de la aplicación."""
    
    # Header
    st.title("📊 Dashboard de Ventas E-commerce")
    st.markdown("---")
    
    # Cargar datos
    with st.spinner('Cargando datos...'):
        transacciones, clientes, productos = cargar_datos()
    
    # Sidebar - Filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro de fechas
    fecha_min = transacciones['fecha'].min().date()
    fecha_max = transacciones['fecha'].max().date()
    
    fecha_inicio, fecha_fin = st.sidebar.date_input(
        "Rango de Fechas",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max
    )
    
    # Filtro de categorías
    categorias = ['Todas'] + sorted(transacciones['categoria'].unique().tolist())
    categoria_seleccionada = st.sidebar.selectbox("Categoría", categorias)
    
    # Filtro de canal
    canales = ['Todos'] + sorted(transacciones['canal'].unique().tolist())
    canal_seleccionado = st.sidebar.selectbox("Canal de Venta", canales)
    
    # Aplicar filtros
    df_filtrado = transacciones.copy()
    df_filtrado = df_filtrado[
        (df_filtrado['fecha'].dt.date >= fecha_inicio) &
        (df_filtrado['fecha'].dt.date <= fecha_fin)
    ]
    
    if categoria_seleccionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_seleccionada]
    
    if canal_seleccionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['canal'] == canal_seleccionado]
    
    # Calcular métricas
    metricas = calcular_metricas(df_filtrado)
    
    # Mostrar métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Ingresos Totales",
            value=f"€{metricas['ingresos']:,.0f}",
            delta=f"{len(df_filtrado)} transacciones"
        )
    
    with col2:
        st.metric(
            label="🛒 Transacciones",
            value=f"{metricas['transacciones']:,}",
            delta=f"{(metricas['transacciones']/len(transacciones)*100):.1f}% del total"
        )
    
    with col3:
        st.metric(
            label="📊 Ticket Promedio",
            value=f"€{metricas['ticket_promedio']:.2f}"
        )
    
    with col4:
        st.metric(
            label="📦 Productos Vendidos",
            value=f"{metricas['productos']:,}"
        )
    
    st.markdown("---")
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(crear_grafico_tendencia(df_filtrado), use_container_width=True)
    
    with col2:
        st.plotly_chart(crear_grafico_categorias(df_filtrado), use_container_width=True)
    
    # Segunda fila de gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(crear_grafico_pie_canales(df_filtrado), use_container_width=True)
    
    with col2:
        st.plotly_chart(crear_grafico_top_productos(df_filtrado), use_container_width=True)
    
    # Mapa de calor
    st.plotly_chart(crear_mapa_calor_ventas(df_filtrado), use_container_width=True)
    
    # Tabla de datos
    with st.expander("📋 Ver Datos Detallados"):
        st.dataframe(
            df_filtrado[['fecha', 'producto_nombre', 'categoria', 'cantidad', 
                        'precio_unitario', 'total', 'canal', 'ciudad_envio']].head(100),
            use_container_width=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"**Última actualización**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"**Total registros**: {len(df_filtrado):,} de {len(transacciones):,}"
    )


if __name__ == "__main__":
    main()
