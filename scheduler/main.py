from src.services.kafka_service import consume_messages

if __name__ == "__main__":
    print("[INFO] Starting Kafka consumer service...")
    consume_messages()
