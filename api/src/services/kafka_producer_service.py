from kafka import KafkaProducer
import json
from src.core.config import KAFKA_BROKER_URL, TRANSFORMED_TOPIC

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def produce_message(data):
    producer.send(TRANSFORMED_TOPIC, value=data)
    producer.flush()
    print(f"[INFO] Produced message to topic {TRANSFORMED_TOPIC}: {data}")