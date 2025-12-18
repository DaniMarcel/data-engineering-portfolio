"""Airflow DAG - Daily ETL"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_task():
    print("📥 Extracting data...")
    # Extract logic here
    return "Data extracted"

def transform_task():
    print("🔄 Transforming data...")
    # Transform logic
    return "Data transformed"

def load_task():
    print("💾 Loading data...")
    # Load logic
    return "Data loaded"

with DAG(
    'daily_etl',
    default_args=default_args,
    description='Daily ETL pipeline',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False,
    tags=['etl', 'daily'],
) as dag:
    
    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_task,
    )
    
    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_task,
    )
    
    load = PythonOperator(
        task_id='load',
        python_callable=load_task,
    )
    
    # Define dependencies
    extract >> transform >> load
