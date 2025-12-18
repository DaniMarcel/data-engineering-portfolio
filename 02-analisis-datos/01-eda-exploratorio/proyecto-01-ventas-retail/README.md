# 📊 Proyecto 01: Análisis Exploratorio de Datos (EDA) - E-commerce

## 🎯 Objetivos de Aprendizaje

- ✅ Cargar y explorar datasets con **pandas**
- ✅ Realizar análisis estadístico descriptivo
- ✅ Identificar problemas de calidad de datos
- ✅ Crear visualizaciones profesionales con **matplotlib** y **seaborn**
- ✅ Generar reportes automatizados
- ✅ Análisis temporal, categórico y de clientes

## 🎓 Nivel

**Intermedio** - Requiere conocimientos básicos de Python y pandas

## 📋 Conceptos Clave

### Pandas

- DataFrames y Series
- Groupby y agregaciones
- Merge y joins
- Funciones de fecha/tiempo
- Manejo de valores faltantes

### Visualización

- Matplotlib: gráficos de líneas, barras, histogramas
- Seaborn: visualizaciones estadísticas
- Configuración de estilos y temas
- Guardar gráficos de alta calidad

### Análisis Estadístico

- Medidas de tendencia central
- Distribuciones
- Detección de outliers (IQR)
- Análisis de correlación

## 🚀 Quick Start

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Generar datasets

```bash
cd src
python generar_datos.py
```

Esto generará:

- `productos.csv` - Catálogo de 100 productos
- `clientes.csv` - Base de 5,000 clientes
- `transacciones.csv` - 50,000 transacciones
- `transacciones.json` - Mismo en formato JSONL
- `transacciones.parquet` - Mismo en formato Parquet

### 3. Ejecutar análisis EDA

```bash
python eda_completo.py
```

## 📊 Estructura de Datos

### Transacciones (50k registros)

| Campo           | Tipo   | Descripción                   |
| --------------- | ------ | ----------------------------- |
| transaccion_id  | string | ID único (T000001)            |
| fecha           | date   | Fecha de transacción          |
| mes             | int    | Mes (1-12)                    |
| trimestre       | string | Trimestre (Q1-Q4)             |
| cliente_id      | int    | ID del cliente                |
| producto_id     | int    | ID del producto               |
| categoria       | string | Categoría del producto        |
| cantidad        | int    | Unidades vendidas             |
| precio_unitario | float  | Precio por unidad             |
| total           | float  | Total de la venta             |
| canal           | string | Web/Móvil/Tienda/Marketplace  |
| metodo_pago     | string | Método de pago                |
| estado_pedido   | string | Completado/Cancelado/Devuelto |
| ciudad_envio    | string | Ciudad de envío               |

### Clientes (5k registros)

| Campo          | Tipo   | Descripción               |
| -------------- | ------ | ------------------------- |
| cliente_id     | int    | ID único                  |
| nombre         | string | Nombre del cliente        |
| email          | string | Email                     |
| ciudad         | string | Ciudad                    |
| edad           | int    | Edad (18-75)              |
| segmento       | string | Premium/Regular/Ocasional |
| fecha_registro | date   | Fecha de registro         |

### Productos (100 registros)

| Campo           | Tipo   | Descripción         |
| --------------- | ------ | ------------------- |
| producto_id     | int    | ID único            |
| nombre_producto | string | Nombre completo     |
| categoria       | string | Categoría principal |
| subcategoria    | string | Subcategoría        |
| precio_base     | float  | Precio estándar     |
| costo           | float  | Costo del producto  |
| stock           | int    | Unidades en stock   |

## 💡 Análisis Realizados

### 1. Calidad de Datos

- ✅ Detección de valores faltantes
- ✅ Identificación de duplicados
- ✅ Detección de outliers (método IQR)
- ✅ Reporte de problemas

### 2. Análisis Temporal

- 📈 Ingresos por mes
- 📈 Número de transacciones mensuales
- 📈 Ventas por día de la semana
- 📈 Tendencia diaria de ingresos

### 3. Análisis por Categorías

- 📦 Ingresos por categoría
- 📦 Top 10 productos más vendidos
- 📦 Descuento promedio por categoría
- 📦 Distribución de ventas (pie chart)

### 4. Análisis de Clientes

- 👥 Top 10 clientes por gasto
- 👥 Ventas por segmento (Premium/Regular/Ocasional)
- 👥 Ventas por ciudad
- 👥 Distribución de edad

## 📈 Gráficos Generados

El análisis genera automáticamente:

1. **01_ventas_tiempo.png** - 4 gráficos de análisis temporal
2. **02_categorias.png** - 4 gráficos de análisis de productos
3. **03_clientes.png** - 3 gráficos de análisis de clientes

Todos en alta resolución (300 DPI) para presentaciones profesionales.

## 📝 Reportes Generados

- `calidad_datos.txt` - Reporte de problemas de calidad
- `reporte_eda.txt` - Reporte completo del análisis

## 🔧 Personalización

### Cambiar parámetros de generación

En `generar_datos.py`:

```python
NUM_CLIENTES = 10000  # Más clientes
NUM_TRANSACCIONES = 100000  # Más transacciones
```

### Añadir nuevos análisis

En `eda_completo.py`:

```python
def analisis_personalizado(self):
    # Tu código aquí
    pass

# En ejecutar_analisis_completo():
self.analisis_personalizado()
```

### Cambiar estilo de gráficos

```python
plt.style.use('seaborn-v0_8-whitegrid')  # Diferentes estilos
sns.set_palette("Set2")  # Diferentes paletas
```

## 🐛 Troubleshooting

**ModuleNotFoundError: No module named 'pandas'**

```bash
pip install -r requirements.txt
```

**Los gráficos no se muestran**

- Los gráficos se guardan automáticamente en `output/graficos/`
- No usan `plt.show()` para facilitar ejecución automática

**Problema con fechas**

- Las fechas usan formato ISO (YYYY-MM-DD)
- Pandas las convierte automáticamente con `pd.to_datetime()`

## 📚 Próximos Pasos

1. **Análisis Avanzado**:

   - Análisis de cohortes
   - RFM (Recency, Frequency, Monetary)
   - Análisis de cesta de compra
   - Predicción de churn

2. **Visualización Interactiva**:

   - Proyecto con Plotly
   - Dashboard con Streamlit
   - Gráficos interactivos con widgets

3. **Machine Learning**:
   - Segmentación de clientes (clustering)
   - Predicción de ventas
   - Sistema de recomendación

## 💻 Código Destacado

### Detección de Outliers con IQR

```python
Q1 = df['cantidad'].quantile(0.25)
Q3 = df['cantidad'].quantile(0.75)
IQR = Q3 - Q1
outliers = ((df['cantidad'] < Q1 - 1.5 * IQR) |
           (df['cantidad'] > Q3 + 1.5 * IQR))
```

### Agregaciones Complejas

```python
ventas_cat = df.groupby('categoria').agg({
    'total': ['sum', 'count'],
    'cantidad': 'sum',
    'descuento_porcentaje': 'mean'
}).round(2)
```

### Joins Eficientes

```python
df = transacciones.merge(clientes, on='cliente_id', how='left')
```

## 📊 Datos de Ejemplo

Todos los datos son sintéticos pero realistas:

- ✅ Distribución Pareto (20% clientes generan 80% ventas)
- ✅ Estacionalidad en ventas
- ✅ Problemas de calidad intencionales (~2%)
- ✅ Múltiples categorías y segmentos

## 🎓 Conceptos Aprendidos

Después de este proyecto comprenderás:

- 📊 Cómo explorar datasets desconocidos
- 📈 Identificar patrones y tendencias
- 🔍 Detectar problemas de calidad
- 📉 Crear visualizaciones efectivas
- 📝 Generar reportes profesionales

---

**¡Explora los datos y encuentra insights valiosos! 📊✨**
