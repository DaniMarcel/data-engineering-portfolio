"""Prefect Workflow Example"""
from prefect import flow, task
from datetime import datetime

@task
def extract_data():
    """Extract task"""
    print("📥 Extracting data...")
    return {"records": 1000, "timestamp": datetime.now()}

@task
def transform_data(data):
    """Transform task"""
    print(f"🔄 Transforming {data['records']} records...")
    data['transformed'] = True
    return data

@task
def load_data(data):
    """Load task"""
    print(f"💾 Loading {data['records']} records...")
    print(f"✅ Pipeline completed at {data['timestamp']}")
    return f"Loaded {data['records']} records"

@flow(name="ETL Pipeline")
def etl_flow():
    """Main ETL flow"""
    raw_data = extract_data()
    transformed = transform_data(raw_data)
    result = load_data(transformed)
    return result

if __name__ == "__main__":
    print("🚀 Starting Prefect pipeline...")
    result = etl_flow()
    print(f"\n🎉 Result: {result}")
