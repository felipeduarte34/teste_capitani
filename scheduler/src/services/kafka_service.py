from kafka import KafkaConsumer
import json
import requests
from datetime import datetime
from time import sleep
from src.core.config import KAFKA_BROKER_URL, TOPIC_NAME, API_URL
from src.domain.models.product import ProductSchema

def transform_message(message):
    data = json.loads(message)
    print(data)
    product = ProductSchema(
        id=data["productId"],
        name=data["productName"],
        description=data["productDescription"],
        pricing={
            "amount": data["price"],
            "currency": data["currency"]
        },
        availability={
            "quantity": data["stockQuantity"],
            "timestamp": datetime.utcnow().isoformat()
        },
        category=data["category"]
    )
    return product

def consume_messages():
    print(f"[INFO] Consuming messages from topic {TOPIC_NAME}")
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_BROKER_URL,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        print(f"Connected to Kafka")
        for message in consumer:
            print(f"Received message: {message.value}")
            product = transform_message(json.dumps(message.value))
            transformed_data = product.dict()
            response = requests.post(API_URL, json=transformed_data)
            if response.status_code == 200:
                print("Message sent successfully!")
            else:
                print(f"Failed to send message: {response.status_code}")
                print(f"Detail {response.text}")

    except Exception as e:
        print(str(e))