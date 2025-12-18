"""Real-Time Analytics Platform - Integrator Project"""
# Combines: Kafka + Spark Streaming + Dashboard

from datetime import datetime
import time
from collections import deque

class RealTimeAnalyticsPlatform:
    """End-to-end real-time analytics platform"""
    
    def __init__(self):
        self.kafka_topic = "events"
        self.spark_stream = deque(maxlen=100)
        self.metrics = {
            'total_events': 0,
            'events_per_second': 0,
            'avg_latency_ms': 0
        }
    
    def ingest_event(self, event):
        """Ingest event into Kafka (simulated)"""
        event['ingested_at'] = datetime.now()
        self.spark_stream.append(event)
        self.metrics['total_events'] += 1
    
    def process_stream(self):
        """Spark Streaming processing"""
        if not self.spark_stream:
            return []
        
        # Aggregate last 10 events
        recent = list(self.spark_stream)[-10:]
        
        aggregated = {
            'window_size': len(recent),
            'total_value': sum(e.get('value', 0) for e in recent),
            'avg_value': sum(e.get('value', 0) for e in recent) / len(recent) if recent else 0,
            'timestamp': datetime.now()
        }
        
        return aggregated
    
    def get_dashboard_data(self):
        """Get data for real-time dashboard"""
        return {
            'metrics': self.metrics,
            'latest_aggregation': self.process_stream(),
            'stream_size': len(self.spark_stream)
        }

# Demo
if __name__ == '__main__':
    print("🔄 REAL-TIME ANALYTICS PLATFORM\n")
    print("Components: Kafka → Spark Streaming → Dashboard\n")
    
    platform = RealTimeAnalyticsPlatform()
    
    # Simulate streaming events
    print("📡 Streaming events...")
    for i in range(20):
        event = {
            'event_id': i,
            'user_id': i % 5,
            'value': (i * 10) % 100,
            'timestamp': datetime.now()
        }
        platform.ingest_event(event)
        
        if i % 5 == 0:
            dashboard = platform.get_dashboard_data()
            print(f"\n📊 Dashboard Update (Event#{i}):")
            print(f"  Total Events: {dashboard['metrics']['total_events']}")
            print(f"  Stream Size: {dashboard['stream_size']}")
            print(f"  Avg Value: {dashboard['latest_aggregation'].get('avg_value', 0):.2f}")
        
        time.sleep(0.1)
    
    print("\n✅ Real-time analytics platform demo completed!")
    print("\nArchitecture:")
    print("  1. Kafka - Event ingestion")
    print("  2. Spark Streaming - Real-time processing")
    print("  3. Dashboard - Live visualization")
