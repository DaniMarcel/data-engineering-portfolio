"""Context Managers for Data Engineering"""
from contextlib import contextmanager
import time
import logging

@contextmanager
def timer(name="Operation"):
    """Context manager para medir tiempo"""
    start = time.time()
    print(f"⏱️  Starting: {name}")
    try:
        yield
    finally:
        duration = time.time() - start
        print(f"✅ {name} completed in {duration:.2f}s")

@contextmanager
def database_connection(db_url):
    """Simula conexión a BD"""
    print(f"📂 Opening connection to {db_url}")
    conn = {'url': db_url, 'active': True}
    try:
        yield conn
    finally:
        conn['active'] = False
        print("🔒 Connection closed")

class DataPipeline:
    """Context manager para pipeline de datos"""
    def __init__(self, name):
        self.name = name
        
    def __enter__(self):
        print(f"🚀 Starting pipeline: {self.name}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"❌ Pipeline failed: {exc_val}")
        else:
            print(f"✅ Pipeline completed: {self.name}")
        return False

# Ejemplos de uso
if __name__ == "__main__":
    # Timer
    with timer("Data Processing"):
        time.sleep(1)
    
    # DB Connection
    with database_connection("postgresql://localhost") as conn:
        print(f"   Working with {conn['url']}")
    
    # Pipeline
    with DataPipeline("ETL Process") as pipeline:
        print("   Processing data...")
