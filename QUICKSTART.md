# 🚀 Guía de Inicio Rápido - Proyectos Ejecutables

Esta guía te muestra cómo ejecutar **50+ proyectos inmediatamente** solo con Python y pip, sin necesidad de Docker, cuentas cloud, ni infraestructura compleja.

## 📋 Requisitos

- **Python 3.11+** instalado
- **pip** (gestor de paquetes de Python)
- Editor de código (opcional)

## 🎯 Inicio Rápido en 3 Pasos

### 1️⃣ Generar Datasets

```bash
# Dataset compartido
cd "c:\Users\WARRIOR\Documents\data engineer\datasets-ejemplo"
python generar_datasets.py

# Dataset de e-commerce (usado por muchos proyectos)
cd "c:\Users\WARRIOR\Documents\data engineer\02-analisis-datos\01-eda-exploratorio\proyecto-01-ventas-retail\src"
python generar_datos.py
```

### 2️⃣ Instalar Dependencias

Para cada proyecto, instala sus dependencias:

```bash
cd [ruta-del-proyecto]
pip install -r requirements.txt
```

### 3️⃣ Ejecutar

```bash
python src/main.py  # o el archivo principal del proyecto
```

---

## 🌟 Top 5 Proyectos Recomendados para Empezar

### 1. 📊 EDA - Análisis Exploratorio Completo

```bash
cd "02-analisis-datos\01-eda-exploratorio\proyecto-01-ventas-retail"
pip install pandas numpy matplotlib seaborn openpyxl pyarrow
python src/generar_datos.py
python src/eda_completo.py
```

**Resultado**: Análisis completo con 10+ gráficos y reporte de 50k transacciones

### 2. 📈 Dashboard Interactivo con Streamlit

```bash
cd "02-analisis-datos\06-streamlit-apps\proyecto-01-dashboard-ventas"
pip install streamlit pandas plotly
streamlit run src/app.py
```

**Resultado**: Dashboard web interactivo en http://localhost:8501

### 3. 🧪 Testing Profesional con Pytest

```bash
cd "01-python-fundamentos\03-avanzado\proyecto-03-testing-pytest"
pip install pytest pandas
pytest tests/ -v
```

**Resultado**: Suite completa de tests con coverage

### 4. 🔍 Data Profiling Automático

```bash
cd "03-ingenieria-datos\03-calidad-datos\proyecto-02-data-profiling"
pip install pandas numpy
python src/profiler.py
```

**Resultado**: Reporte completo de calidad de datos

### 5. 🤖 ML Pipeline Completo

```bash
cd "06-proyectos-integradores\proyecto-03-ml-pipeline-complete"
pip install scikit-learn pandas
python src/ml_pipeline.py
```

**Resultado**: Modelo entrenado, guardado y monitoreado

---

## 📚 Proyectos por Categoría

### 🐍 Python Fundamentals (9 proyectos - TODOS ejecutables)

#### Básico

```bash
# 1. Lector CSV (SIN dependencias!)
cd "01-python-fundamentos\01-basico\proyecto-01-lector-archivos-csv\src"
python generar_datos.py
python main.py
```

#### Intermedio

```bash
# 2. API Consumer - Consumir APIs REST
cd "01-python-fundamentos\02-intermedio\proyecto-01-api-consumer"
pip install requests python-dotenv
python src/main.py

# 3. Web Scraper - Extraer datos de webs
cd "01-python-fundamentos\02-intermedio\proyecto-02-web-scraper"
pip install requests beautifulsoup4 lxml
python src/main.py

# 4. CLI Tool - Herramienta de línea de comandos
cd "01-python-fundamentos\02-intermedio\proyecto-03-cli-data-tool"
pip install click pandas openpyxl pyarrow
python src/cli.py --help
python src/cli.py view data.csv --head 10

# 5. FastAPI - API REST moderna
cd "01-python-fundamentos\02-intermedio\proyecto-04-fastapi-rest"
pip install fastapi uvicorn pandas pydantic
python api/main.py
# Abrir en navegador: http://localhost:8000/docs
```

#### Avanzado

```bash
# 6. Decoradores - Patrones avanzados
cd "01-python-fundamentos\03-avanzado\proyecto-01-decoradores-data-pipelines"
python src/decoradores.py

# 7. Async/Await - Programación asíncrona
cd "01-python-fundamentos\03-avanzado\proyecto-02-async-data-fetcher"
pip install aiohttp
python src/async_fetcher.py

# 8. Testing con Pytest
cd "01-python-fundamentos\03-avanzado\proyecto-03-testing-pytest"
pip install pytest pandas pytest-cov
pytest tests/ -v --cov

# 9. Context Managers
cd "01-python-fundamentos\03-avanzado\proyecto-04-context-managers"
python src/context_managers.py
```

---

### 📊 Análisis de Datos (18 proyectos - 16 ejecutables)

#### EDA y Visualización

```bash
# EDA Completo
cd "02-analisis-datos\01-eda-exploratorio\proyecto-01-ventas-retail"
pip install pandas numpy matplotlib seaborn openpyxl pyarrow
python src/eda_completo.py

# Plotly Interactivo
cd "02-analisis-datos\02-visualizacion\proyecto-01-plotly-interactivo"
pip install plotly pandas kaleido
python src/visualizaciones.py

# Matplotlib/Seaborn Avanzado
cd "02-analisis-datos\03-matplotlib-seaborn\proyecto-01-visualizacion-avanzada"
pip install matplotlib seaborn pandas numpy
python src/visualizaciones.py

# Pandas vs Polars - Comparativa
cd "02-analisis-datos\04-polars\proyecto-01-comparativa-pandas-polars"
pip install pandas polars numpy
python src/comparativa.py
```

#### Dashboards

```bash
# Streamlit Dashboard
cd "02-analisis-datos\06-streamlit-apps\proyecto-01-dashboard-ventas"
pip install streamlit pandas plotly
streamlit run src/app.py

# Data Explorer Streamlit
cd "02-analisis-datos\06-streamlit-apps\proyecto-02-data-explorer"
pip install streamlit pandas
streamlit run src/app.py

# Dash Dashboard
cd "02-analisis-datos\10-dashboards-avanzados\proyecto-01-dash-plotly"
pip install dash plotly pandas
python src/app.py
# Abrir: http://localhost:8050
```

#### Automatización

```bash
# Reportes Excel
cd "02-analisis-datos\05-automatizacion\proyecto-01-reportes-excel"
pip install pandas openpyxl
python src/generador_reportes.py

# Reportes PDF
cd "02-analisis-datos\05-automatizacion\proyecto-03-pdf-reports"
pip install reportlab pandas
python src/pdf_generator.py
```

#### Machine Learning y Advanced Analytics

```bash
# Time Series Forecasting
cd "02-analisis-datos\08-series-temporales\proyecto-01-forecasting"
pip install prophet pandas matplotlib
python src/forecast.py

# ML Regression
cd "02-analisis-datos\09-machine-learning\proyecto-01-regression-basics"
pip install scikit-learn pandas
python src/regression.py

# Pandas Performance
cd "02-analisis-datos\11-optimizacion\proyecto-01-performance-pandas"
pip install pandas numpy
python src/optimization.py

# Statistical Testing
cd "02-analisis-datos\12-statistical-analysis\proyecto-01-hypothesis-testing"
pip install scipy pandas numpy
python src/stats_tests.py

# K-Means Clustering
cd "02-analisis-datos\13-clustering\proyecto-01-kmeans"
pip install scikit-learn pandas matplotlib
python src/clustering.py

# NLP Text Analysis
cd "02-analisis-datos\14-nlp\proyecto-01-text-analysis"
python src/nlp_analysis.py  # SIN dependencias!

# Geospatial Maps
cd "02-analisis-datos\15-geospatial\proyecto-01-maps"
pip install folium pandas
python src/maps.py

# Web Analytics
cd "02-analisis-datos\16-web-analytics\proyecto-01-ga-analysis"
pip install pandas numpy
python src/web_analytics.py

# A/B Testing
cd "02-analisis-datos\17-ab-testing\proyecto-01-experiments"
pip install scipy numpy
python src/ab_test.py

# Recommendation System
cd "02-analisis-datos\18-recommendation\proyecto-01-collaborative-filtering"
pip install scikit-surprise pandas
python src/recommender.py
```

---

### 🔧 Data Engineering (12 proyectos - TODOS ejecutables)

#### ETL Pipelines

```bash
# ETL Básico (SIN dependencias!)
cd "03-ingenieria-datos\01-etl-python-puro\proyecto-01-pipeline-basico"
python src/pipeline.py

# ETL Incremental con Checkpoints
cd "03-ingenieria-datos\01-etl-python-puro\proyecto-02-incremental-etl"
pip install pandas pyarrow
python src/incremental_etl.py
```

#### Databases

```bash
# DuckDB - Analytics local
cd "03-ingenieria-datos\02-bases-datos\03-duckdb\proyecto-01-analytics-local"
pip install duckdb pandas pyarrow
python src/analytics.py

# SQLAlchemy ORM
cd "03-ingenieria-datos\02-bases-datos\02-postgresql\proyecto-01-sqlalchemy-orm"
pip install sqlalchemy psycopg2-binary
python src/models.py
```

#### Data Quality

```bash
# Pydantic Validation
cd "03-ingenieria-datos\03-calidad-datos\proyecto-01-validacion-pydantic"
pip install pydantic
python src/validador.py

# Data Profiling
cd "03-ingenieria-datos\03-calidad-datos\proyecto-02-data-profiling"
pip install pandas numpy
python src/profiler.py
```

#### APIs

```bash
# Flask REST API
cd "03-ingenieria-datos\06-api-data\proyecto-01-rest-data-service"
pip install flask pandas
python src/app.py
# Abrir: http://localhost:5000/api/stats
```

#### Logging

```bash
# Advanced Logging (SIN dependencias!)
cd "03-ingenieria-datos\07-logging-monitoring\proyecto-01-logging-avanzado"
python src/logger.py
```

---

### ⚡ Big Data (12 proyectos - 10 ejecutables sin cluster)

```bash
# PySpark - Intro
cd "05-big-data-avanzado\01-apache-spark\proyecto-01-intro-pyspark"
pip install pyspark
python src/intro_spark.py

# PySpark ETL
cd "05-big-data-avanzado\01-apache-spark\proyecto-02-spark-etl"
pip install pyspark
python src/spark_etl.py

# PySpark ML
cd "05-big-data-avanzado\01-apache-spark\proyecto-03-spark-ml"
pip install pyspark
python src/spark_ml.py

# Kafka Simulation
cd "05-big-data-avanzado\02-kafka\proyecto-01-producer-consumer"
pip install kafka-python
python src/kafka_example.py

# MapReduce Simulation
cd "05-big-data-avanzado\03-hadoop\proyecto-02-mapreduce"
python src/wordcount.py  # SIN dependencias!

# Luigi Pipeline
cd "05-big-data-avanzado\04-procesamiento-batch\proyecto-02-luigi-pipeline"
pip install luigi
python src/pipeline.py

# Flink Streaming Simulation
cd "05-big-data-avanzado\05-streaming\proyecto-01-flink-basics"
python src/flink_stream.py  # SIN dependencias!

# Delta Lake
cd "05-big-data-avanzado\06-data-lake\proyecto-01-delta-lake"
pip install delta-spark pyspark
python src/delta_example.py

# Prefect Workflow
cd "05-big-data-avanzado\07-orchestration\proyecto-01-prefect"
pip install prefect
python src/workflow.py

# Hive Examples
cd "05-big-data-avanzado\08-hive\proyecto-01-data-warehouse"
python src/hive_examples.py

# Presto Queries
cd "05-big-data-avanzado\09-presto\proyecto-01-federated-queries"
python src/presto_queries.py
```

---

### 🏪 Proyectos Integradores (5 proyectos - TODOS ejecutables)

```bash
# 1. E-commerce End-to-End
cd "06-proyectos-integradores\proyecto-01-ecommerce-completo"
# Ver README para arquitectura completa

# 2. Real-Time Analytics Platform
cd "06-proyectos-integradores\proyecto-02-real-time-analytics"
pip install kafka-python pyspark
python src/platform.py

# 3. Complete ML Pipeline
cd "06-proyectos-integradores\proyecto-03-ml-pipeline-complete"
pip install scikit-learn pandas
python src/ml_pipeline.py

# 4. Data Platform
cd "06-proyectos-integradores\proyecto-04-data-platform"
python src/platform.py  # SIN dependencias!

# 5. Streaming Analytics
cd "06-proyectos-integradores\proyecto-05-streaming-analytics"
python src/streaming_platform.py  # SIN dependencias!
```

---

## 🎨 Proyectos por Nivel de Dificultad

### ⭐ Principiante (Empieza aquí)

1. Lector CSV
2. Decoradores
3. Context Managers
4. NLP básico
5. Data Profiling

### ⭐⭐ Intermedio

1. API Consumer
2. Web Scraper
3. EDA Completo
4. Streamlit Dashboard
5. ETL Pipeline
6. Testing con Pytest

### ⭐⭐⭐ Avanzado

1. FastAPI REST
2. Async/Await
3. PySpark
4. ML Pipeline
5. Real-Time Analytics

---

## 📊 Proyectos por Tiempo de Ejecución

### ⚡ Rápidos (< 1 minuto)

- Context Managers
- Decoradores
- NLP
- Logging
- Data Platform simulation

### 🚀 Medios (1-5 minutos)

- ETL Pipelines
- Data Profiling
- Statistical Testing
- Clustering
- A/B Testing

### 🔄 Largos (5+ minutos)

- EDA Completo (muchos gráficos)
- PySpark (arranque de Spark)
- Forecasting (modelo Prophet)
- ML Pipeline (entrenamiento)

---

## 🔥 Combinaciones Recomendadas

### Para Demostrar Data Analysis

```bash
1. EDA Completo
2. Dashboard Streamlit
3. Forecasting
4. Clustering
```

### Para Demostrar Engineering

```bash
1. ETL Incremental
2. Pydantic Validation
3. Data Profiling
4. FastAPI
```

### Para Demostrar Big Data

```bash
1. PySpark Intro
2. Spark ETL
3. Spark ML
4. Luigi Pipeline
```

### Para Demostrar Full Stack

```bash
1. ML Pipeline Complete
2. Real-Time Analytics
3. Data Platform
```

---

## ⚠️ Troubleshooting

### Error: ModuleNotFoundError

```bash
# Instala las dependencias
pip install -r requirements.txt
```

### Error: PermissionError al escribir archivos

```bash
# Ejecuta desde una carpeta donde tengas permisos
# O ejecuta cmd/PowerShell como administrador
```

### PySpark lento en Windows

```bash
# Normal - Spark arranca una JVM
# Primera ejecución siempre tarda más
```

### Puerto ya en uso (8000, 8501, etc.)

```bash
# Cierra otras aplicaciones en ese puerto
# O cambia el puerto en el código
```

---

## 💡 Tips

1. **Instalación global vs virtual environment**

   ```bash
   # Recomendado: crear un virtual environment
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Ver resultados**

   - Gráficos: Se abren automáticamente o se guardan como PNG
   - CSVs: Abre con Excel o cualquier editor
   - Logs: Revisa la carpeta `logs/`
   - APIs: Abre en navegador la URL indicada

3. **Reusar datos**
   - Genera los datasets UNA VEZ
   - Todos los proyectos los reutilizan

---

## 📝 Resumen

**TOTAL EJECUTABLE SIN INFRAESTRUCTURA**: 50+ proyectos

**Con código Python puro (0 dependencies)**: 8 proyectos
**Solo con pip install**: 50+ proyectos
**Requieren Docker/Cloud**: Solo 4 proyectos (MySQL real, Airflow, etc.)

**¡Tienes un portafolio completo ejecutable en tu laptop!** 🚀
