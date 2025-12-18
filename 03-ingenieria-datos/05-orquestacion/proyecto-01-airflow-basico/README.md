# 🌬️ Apache Airflow - Orquestación

DAG básico para ETL orchestration.

**Setup:**

```bash
pip install apache-airflow
airflow db init
airflow webserver
```

**DAG:** daily_etl - Runs daily at 2 AM

**Features:**

- Python operators
- Task dependencies
- Retry logic
- Scheduling

Airflow UI: http://localhost:8080
