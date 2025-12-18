"""Kafka Producer/Consumer Example"""
# Note: Requires Kafka running
# docker run -p 9092:9092 apache/kafka:latest

from kafka import KafkaProducer, KafkaConsumer
import json
from datetime import datetime

def produce_messages():
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    for i in range(10):
        message = {
            'id': i,
            'timestamp': datetime.now().isoformat(),
            'data': f'Message {i}'
        }
        producer.send('data-topic', value=message)
        print(f"📤 Sent: {message}")
    
    producer.flush()
    producer.close()

def consume_messages():
    consumer = KafkaConsumer(
        'data-topic',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    print("📥 Listening for messages...")
    for message in consumer:
        print(f"   Received: {message.value}")

if __name__ == "__main__":
    print("🔥 Kafka Example")
    print("Make sure Kafka is running!")
    # produce_messages()
    # consume_messages()
