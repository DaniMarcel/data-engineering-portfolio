"""Streaming Analytics Platform - Kafka + Flink"""
from datetime import datetime
import time
from collections import deque

class StreamingAnalyticsPlatform:
    """
    Real-time streaming analytics platform
    Architecture: Kafka (Ingestion) → Flink (Processing) → Dashboard (Visualization)
    """
    
    def __init__(self):
        self.kafka_buffer = deque(maxlen=1000)
        self.flink_state = {}
        self.dashboard_metrics = {
            'events_processed': 0,
            'alerts_triggered': 0,
            'avg_latency_ms': 0
        }
    
    def produce_to_kafka(self, event):
        """Kafka producer - Ingest events"""
        event['kafka_timestamp'] = datetime.now()
        self.kafka_buffer.append(event)
    
    def flink_window_aggregation(self, window_size=10):
        """Flink stream processing - Windowed aggregation"""
        if len(self.kafka_buffer) < window_size:
            return None
        
        # Get last N events
        window = list(self.kafka_buffer)[-window_size:]
        
        # Aggregate
        agg = {
            'window_start': window[0]['kafka_timestamp'],
            'window_end': window[-1]['kafka_timestamp'],
            'event_count': len(window),
            'total_value': sum(e.get('value', 0) for e in window),
            'avg_value': sum(e.get('value', 0) for e in window) / len(window),
            'max_value': max(e.get('value', 0) for e in window),
            'processed_at': datetime.now()
        }
        
        # Update state
        self.flink_state = agg
        self.dashboard_metrics['events_processed'] += len(window)
        
        # Check for alerts
        if agg['max_value'] > 800:
            self.dashboard_metrics['alerts_triggered'] += 1
            agg['alert'] = f"High value detected: {agg['max_value']}"
        
        return agg
    
    def update_dashboard(self):
        """Real-time dashboard update"""
        latency = 0
        if self.flink_state:
            latency = (datetime.now() - self.flink_state['processed_at']).microseconds / 1000
        
        self.dashboard_metrics['avg_latency_ms'] = latency
        
        return {
            'metrics': self.dashboard_metrics,
            'latest_window': self.flink_state,
            'kafka_buffer_size': len(self.kafka_buffer)
        }

# Demo
if __name__ == '__main__':
    print("🌊 STREAMING ANALYTICS PLATFORM\n")
    print("Components: Kafka → Flink → Dashboard\n")
    
    platform = StreamingAnalyticsPlatform()
    
    # Simulate streaming
    print("📡 Starting event stream...\n")
    
    for i in range(25):
        # Generate event
        event = {
            'event_id': i,
            'user_id': i % 5,
            'value': (i * 37) % 1000,  # Some will trigger alerts
            'event_type': 'purchase' if i % 3 == 0 else 'view'
        }
        
        # Kafka ingestion
        platform.produce_to_kafka(event)
        
        # Flink processing (every 5 events)
        if i % 5 == 0 and i > 0:
            result = platform.flink_window_aggregation(window_size=5)
            dashboard = platform.update_dashboard()
            
            print(f"📊 Window #{i//5}:")
            print(f"  Events: {result['event_count']}")
            print(f"  Avg Value: {result['avg_value']:.2f}")
            print(f"  Max Value: {result['max_value']}")
            if 'alert' in result:
                print(f"  🚨 {result['alert']}")
            print(f"  Dashboard - Total Processed: {dashboard['metrics']['events_processed']}")
            print(f"  Dashboard - Alerts: {dashboard['metrics']['alerts_triggered']}\n")
        
        time.sleep(0.05)
    
    # Final dashboard
    final_dashboard = platform.update_dashboard()
    
    print("\n" + "="*60)
    print("📊 FINAL DASHBOARD")
    print("="*60)
    for metric, value in final_dashboard['metrics'].items():
        print(f"  {metric}: {value}")
    
    print(f"\n✅ Streaming platform demo completed!")
    print("\nArchitecture:")
    print("  • Kafka - Event streaming")
    print("  • Flink - Real-time windowed processing")
    print("  • Dashboard - Live metrics & alerts")
