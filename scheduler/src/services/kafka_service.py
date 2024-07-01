from kafka import KafkaConsumer, KafkaProducer
import json
import requests
from datetime import datetime
from src.core.config import KAFKA_BROKER_URL, TOPIC_NAME, API_URL, ERROR_TOPIC_NAME
from src.domain.models.product import ProductSchema

# Configurações de Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def transform_message(message):
    data = json.loads(message)
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

def send_to_error_topic(message):
    print(f"Sending message to error topic: {ERROR_TOPIC_NAME}")
    producer.send(ERROR_TOPIC_NAME, value=message)
    producer.flush()

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
            attempt = 0
            max_attempts = 3
            while attempt < max_attempts:
                try:
                    product = transform_message(json.dumps(message.value))
                    transformed_data = product.dict()
                    response = requests.post(API_URL, json=transformed_data)
                    if response.status_code == 200:
                        print("Message sent successfully!")
                        break
                    else:
                        print(f"Failed to send message: {response.status_code}")
                        print(f"Detail: {response.text}")
                        attempt += 1
                except Exception as e:
                    print(f"Exception occurred: {str(e)}")
                    attempt += 1

            if attempt == max_attempts:
                print(f"Failed to process message after {max_attempts} attempts. Sending to error topic.")
                send_to_error_topic(message.value)

    except Exception as e:
        print(f"Exception occurred while consuming messages: {str(e)}")

if __name__ == "__main__":
    consume_messages()