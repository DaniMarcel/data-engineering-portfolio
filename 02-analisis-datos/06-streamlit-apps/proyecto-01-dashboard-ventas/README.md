# 📊 Dashboard Interactivo de Ventas - Streamlit

## 🎯 Objetivos de Aprendizaje

- ✅ Crear aplicaciones web interactivas con **Streamlit**
- ✅ Visualizaciones dinámicas con **Plotly**
- ✅ Implementar filtros interactivos
- ✅ Calcular métricas en tiempo real
- ✅ Diseñar dashboards profesionales

## 🎓 Nivel

**Intermedio-Avanzado** - Requiere conocimientos de Python, pandas y visualización

## 📋 Conceptos Clave

### Streamlit

- Layout (columnas, sidebar, expander)
- Widgets interactivos (selectbox, date_input, slider)
- Caché de datos (`@st.cache_data`)
- Métricas y KPIs
- Configuración de página

### Plotly

- Gráficos interactivos
- Line charts, bar charts, pie charts
- Heatmaps
- Personalización de estilos

## 🚀 Quick Start

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

```bash
cd src
streamlit run app.py
```

La app se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📊 Características del Dashboard

### 🎛️ Filtros Interactivos (Sidebar)

- **Rango de Fechas**: Selecciona período de análisis
- **Categoría**: Filtra por categoría de producto
- **Canal**: Web, Móvil, Tienda Física, Marketplace

### 📈 Métricas Clave (KPIs)

1. **💰 Ingresos Totales**: Suma de todas las ventas
2. **🛒 Transacciones**: Número de ventas
3. **📊 Ticket Promedio**: Ingreso promedio por venta
4. **📦 Productos Vendidos**: Total de unidades

### 📉 Visualizaciones

**1. Tendencia de Ventas Diarias**

- Gráfico de línea mostrando evolución temporal
- Ideal para identificar patrones y estacionalidad

**2. Ingresos por Categoría**

- Gráfico de barras con código de colores
- Identifica categorías más rentables

**3. Distribución por Canal**

- Gráfico de dona (pie chart)
- Muestra porcentaje de ventas por canal

**4. Top 10 Productos**

- Gráfico de barras horizontal
- Los productos con más ingresos

**5. Mapa de Calor**

- Ventas por día de la semana y hora
- Identifica picos de venta

### 📋 Tabla de Datos

- Ver detalles de transacciones
- Exportable y filtrable

## 💡 Explicación del Código

### Estructura de la App

```python
# 1. Configuración
st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide"
)

# 2. Cargar datos (con caché)
@st.cache_data
def cargar_datos():
    return pd.read_csv('datos.csv')

# 3. Sidebar con filtros
fecha = st.sidebar.date_input("Fecha")
categoria = st.sidebar.selectbox("Categoría", opciones)

# 4. Aplicar filtros
df_filtrado = df[df['categoria'] == categoria]

# 5. Mostrar métricas
st.metric("Ingresos", f"€{total:,.0f}")

# 6. Crear visualizaciones
fig = px.line(df, x='fecha', y='ventas')
st.plotly_chart(fig)
```

### Caché de Datos

```python
@st.cache_data
def cargar_datos():
    # Esta función solo se ejecuta una vez
    # Los datos se cachean para mejorar performance
    return pd.read_csv('datos.csv')
```

### Layouts Responsivos

```python
# Crear 4 columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Métrica 1", "valor")

with col2:
    st.metric("Métrica 2", "valor")
```

### Gráficos con Plotly

```python
fig = px.line(
    df,
    x='fecha',
    y='total',
    title='Tendencia'
)

fig.update_layout(
    hovermode='x unified',
    plot_bgcolor='white'
)

st.plotly_chart(fig, use_container_width=True)
```

## 🎨 Personalización

### Cambiar tema

Crear archivo `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Añadir más gráficos

```python
def crear_grafico_personalizado(df):
    fig = px.scatter(df, x='fecha', y='total')
    return fig

# En main()
st.plotly_chart(crear_grafico_personalizado(df_filtrado))
```

### Añadir más filtros

```python
# En sidebar
precio_min, precio_max = st.sidebar.slider(
    "Rango de Precio",
    min_value=0,
    max_value=1000,
    value=(0, 1000)
)

df_filtrado = df_filtrado[
    (df_filtrado['precio'] >= precio_min) &
    (df_filtrado['precio'] <= precio_max)
]
```

## 📈 Salida Esperada

Al ejecutar la app verás:

```
📊 Dashboard de Ventas E-commerce
────────────────────────────────────

[Sidebar con filtros]
🔍 Filtros
  Rango de Fechas: [selector]
  Categoría: [dropdown]
  Canal: [dropdown]

[Métricas principales]
💰 Ingresos      🛒 Transacciones  📊 Ticket      📦 Productos
€412,589         980               €421.01        2,456

[Gráficos interactivos]
📈 Tendencia | 📦 Categorías
💻 Canales   | 🏆 Top Productos
🔥 Mapa de Calor
```

## 🔧 Troubleshooting

**App no se abre en el navegador**

```bash
streamlit run app.py --server.headless=true
```

**Error: No se encuentran los datos**

- Primero ejecuta el generador de datos del proyecto EDA
- O modifica la ruta en `cargar_datos()`

**Gráficos no se muestran**

- Verifica que plotly esté instalado
- Actualiza streamlit: `pip install --upgrade streamlit`

**App muy lenta**

- Los datos ya están cacheados con `@st.cache_data`
- Reduce el rango de fechas filtrado
- Filtra por categoría específica

## 📚 Próximos Pasos

1. **Mejorar el dashboard**:

   - Añadir predicciones con ML
   - Exportar reportes en PDF
   - Añadir comparativas (mes actual vs anterior)

2. **Funcionalidades avanzadas**:

   - Subida de archivos para analizar propios datos
   - Autenticación de usuarios
   - Conexión a base de datos en tiempo real

3. **Deployment**:

   - Desplegar en Streamlit Cloud (gratis)
   - O en Heroku/Railway

4. **Siguiente proyecto**:
   - Dashboard con ML predictor
   - Data explorer interactivo
   - App de análisis de sentiment

## 🌐 Deployment (Streamlit Cloud)

### 1. Crear repositorio GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tu-usuario/dashboard-ventas.git
git push -u origin main
```

### 2. Desplegar en Streamlit Cloud

1. Ir a https://streamlit.io/cloud
2. Conectar con GitHub
3. Seleccionar repositorio
4. Main file: `src/app.py`
5. ¡Deploy!

Tu app estará disponible en: `https://tu-app.streamlit.app`

## 💻 Comandos Útiles

```bash
# Ejecutar app
streamlit run src/app.py

# Ejecutar con puerto específico
streamlit run src/app.py --server.port 8502

# Ver configuración
streamlit config show

# Limpiar caché
streamlit cache clear
```

## 📝 Notas

- Streamlit recarga automáticamente cuando guardas cambios
- Use `st.cache_data` para operaciones costosas
- Los gráficos Plotly son interactivos (zoom, pan, hover)
- El dashboard es responsive (funciona en móvil)

---

**🚀 Build amazing data apps with Streamlit!**
