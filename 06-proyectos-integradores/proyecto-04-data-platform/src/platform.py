"""Data Platform - Complete Architecture"""
# Full stack data platform simulation

from datetime import datetime
from collections import defaultdict

class DataPlatform:
    """
    Complete Data Platform
    Components: Ingestion, Storage, Processing, Serving, Monitoring
    """
    
    def __init__(self, platform_name):
        self.platform_name = platform_name
        self.data_lake = {}
        self.data_warehouse = {}
        self.metrics = defaultdict(int)
        self.logs = []
    
    def ingest(self, source, data):
        """Data ingestion layer"""
        self.log(f"Ingesting from {source}")
        
        # Store in data lake (raw)
        self.data_lake[source] = {
            'data': data,
            'ingested_at': datetime.now(),
            'format': 'parquet'
        }
        
        self.metrics['ingestion_count'] += len(data)
        self.log(f"Ingested {len(data)} records to data lake")
    
    def process(self, source):
        """Data processing layer (ETL)"""
        if source not in self.data_lake:
            self.log(f"ERROR: Source {source} not found")
            return
        
        self.log(f"Processing data from {source}")
        
        # Transform and load to warehouse
        raw_data = self.data_lake[source]['data']
        
        # Simulate transformation
        processed = {
            'source': source,
            'record_count': len(raw_data),
            'processed_at': datetime.now(),
            'quality_score': 0.95
        }
        
        self.data_warehouse[source] = processed
        self.metrics['processing_count'] += 1
        self.log(f"Processed and loaded to warehouse")
    
    def serve(self, query):
        """Data serving layer (API/Analytics)"""
        self.log(f"Serving query: {query}")
        
        results = {
            'query': query,
            'sources': list(self.data_warehouse.keys()),
            'total_records': sum(dw['record_count'] for dw in self.data_warehouse.values()),
            'served_at': datetime.now()
        }
        
        self.metrics['query_count'] += 1
        return results
    
    def monitor(self):
        """Monitoring and observability"""
        print(f"\n{'='*60}")
        print(f"📊 DATA PLATFORM MONITORING - {self.platform_name}")
        print(f"{'='*60}")
        
        print(f"\n📈 Metrics:")
        for metric, value in self.metrics.items():
            print(f"  {metric}: {value:,}")
        
        print(f"\nData Lake:")
        print(f"  Sources: {len(self.data_lake)}")
        
        print(f"\nData Warehouse:")
        print(f"  Tables: {len(self.data_warehouse)}")
        
        print(f"\nRecent Logs ({len(self.logs)} total):")
        for log in self.logs[-5:]:
            print(f"  {log}")
    
    def log(self, message):
        """Internal logging"""
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        self.logs.append(log_entry)

# Demo
if __name__ == '__main__':
    print("🏗️  COMPLETE DATA PLATFORM\n")
    
    platform = DataPlatform("MyDataPlatform")
    
    # 1. Ingestion
    print("1️⃣ INGESTION LAYER")
    sample_data = [{'id': i, 'value': i*10} for i in range(100)]
    platform.ingest('sales_api', sample_data)
    platform.ingest('user_events', sample_data[:50])
    
    # 2. Processing
    print("\n2️⃣ PROCESSING LAYER")
    platform.process('sales_api')
    platform.process('user_events')
    
    # 3. Serving
    print("\n3️⃣ SERVING LAYER")
    results = platform.serve("SELECT * FROM sales WHERE value > 100")
    print(f"Query results: {results['total_records']} records from {len(results['sources'])} sources")
    
    # 4. Monitoring
    print("\n4️⃣ MONITORING")
    platform.monitor()
    
    print(f"\n{'='*60}")
    print("✅ DATA PLATFORM DEMO COMPLETED")
    print(f"{'='*60}")
    print("\nArchitecture Layers:")
    print("  1. Ingestion - API, Streaming, Batch")
    print("  2. Storage - Data Lake (Raw) + Data Warehouse (Processed)")
    print("  3. Processing - ETL, Data Quality")
    print("  4. Serving - APIs, Analytics")
    print("  5. Monitoring - Metrics, Logs, Alerts")
