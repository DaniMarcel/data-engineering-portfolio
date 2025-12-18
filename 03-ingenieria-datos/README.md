# 🔧 Ingeniería de Datos

Proyectos de procesamiento, transformación y almacenamiento de datos. Desde ETL básico hasta data warehouses.

## 📚 Contenido

### 01 - ETL Python Puro

Pipelines de Extract-Transform-Load sin frameworks:

- **proyecto-01-csv-to-json**: Conversión de formatos
- **proyecto-02-api-to-database**: Ingesta desde APIs
- **proyecto-03-file-processor**: Procesamiento de archivos batch

### 02 - Bases de Datos

#### MySQL

- **proyecto-01-ecommerce-db**: Schema de e-commerce
- **proyecto-02-analytics-warehouse**: Data warehouse básico

#### PostgreSQL

- **proyecto-01-geoespacial**: Datos geoespaciales con PostGIS
- **proyecto-02-json-storage**: Almacenamiento JSON con JSONB

#### DuckDB

- **proyecto-01-analytics-local**: Analytics sin servidor
- **proyecto-02-parquet-query**: Consultas en Parquet

### 03 - Data Warehouse

Modelado dimensional:

- **proyecto-01-star-schema**: Esquema estrella
- **proyecto-02-snowflake-schema**: Esquema copo de nieve
- **proyecto-03-fact-dimension**: Tablas de hechos y dimensiones

### 04 - Calidad de Datos

Validación y limpieza:

- **proyecto-01-data-validation**: Validación con Pydantic
- **proyecto-02-data-cleaning**: Limpieza automatizada
- **proyecto-03-data-profiling**: Perfilado de datos

## 🎯 Objetivos

- ✅ Construir pipelines ETL/ELT robustos
- ✅ Diseñar esquemas de bases de datos eficientes
- ✅ Implementar data warehouses
- ✅ Garantizar calidad de datos
- ✅ Optimizar consultas y rendimiento

## 🛠️ Tecnologías

```
# Bases de datos
mysql-connector-python >= 8.2.0
psycopg2-binary >= 2.9.9
duckdb >= 0.10.0

# ETL/ELT
sqlalchemy >= 2.0.0
pydantic >= 2.5.0
great-expectations >= 0.18.0

# Utilidades
python-dotenv >= 1.0.0
```

## 📖 Orden Recomendado

1. **ETL Python Puro** - Fundamentos sin librerías
2. **Bases de Datos** - Almacenamiento y consultas
3. **Data Warehouse** - Modelado dimensional
4. **Calidad de Datos** - Validación y limpieza

## 💡 Conceptos Clave

- Extract-Transform-Load (ETL)
- Extract-Load-Transform (ELT)
- Modelado dimensional
- Normalización vs desnormalización
- Data quality frameworks
- Batch vs streaming processing

---

**🔧 Build reliable data pipelines**
