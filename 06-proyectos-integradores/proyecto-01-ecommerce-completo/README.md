# 🏪 Proyecto Integrador: E-commerce Completo

## Descripción

Proyecto end-to-end que integra:

- **Backend API** (FastAPI)
- **ETL Pipeline** (Python/Spark)
- **Base de Datos** (PostgreSQL)
- **Analytics** (DuckDB)
- **Visualización** (Streamlit Dashboard)
- **Orquestación** (Airflow)
- **Infraestructura** (Docker Compose)

## Arquitectura

```
[Data Sources] → [ETL Pipeline] → [PostgreSQL] → [Analytics] → [Dashboard]
       ↓               ↓              ↓              ↓             ↓
   Raw Data      Airflow DAG    Transactional   DuckDB OLAP   Streamlit
                                   Database
```

## Componentes

### 1. Backend API

- FastAPI REST endpoints
- CRUD operations
- Authentication
- Data validation (Pydantic)

### 2. ETL Pipeline

- Extract from multiple sources
- Transform with Spark
- Load to PostgreSQL
- Scheduled with Airflow

### 3. Analytics Layer

- DuckDB for OLAP queries
- Pre-aggregated views
- Fast reporting

### 4. Dashboard

- Streamlit interactive UI
- Real-time metrics
- Plotly visualizations

### 5. Infrastructure

- Docker Compose orchestration
- PostgreSQL container
- Redis for caching
- All services dockerized

## Quick Start

```bash
# 1. Start infrastructure
cd backend
docker-compose up -d

# 2. Run ETL
cd ../etl
python run_pipeline.py

# 3. Start API
cd ../backend
uvicorn main:app --reload

# 4. Start Dashboard
cd ../dashboard
streamlit run app.py
```

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **ETL**: Python, PySpark, Pandas
- **Databases**: PostgreSQL, DuckDB, Redis
- **Orchestration**: Apache Airflow
- **Visualization**: Streamlit, Plotly
- **Infrastructure**: Docker, Docker Compose

## Features

✅ Complete data pipeline  
✅ REST API for data access  
✅ Real-time analytics  
✅ Automated orchestration  
✅ Containerized deployment  
✅ Scalable architecture

---

Este proyecto demuestra un stack completo de ingeniería de datos production-ready.
