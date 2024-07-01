from kafka import KafkaProducer
import json

KAFKA_BROKER_URL = "localhost:29092"
TOPIC_NAME = "cadastro-produtos"

def produce_message():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    message = {
        "productId": "12345",
        "productName": "Nome do Produto",
        "productDescription": "Descrição do Produto",
        "price": 100.0,
        "currency": "BRL",
        "stockQuantity": 50,
        "category": "Categoria do Produto"
    }

    producer.send(TOPIC_NAME, message)
    producer.flush()
    print(f"Mensagem enviada para o tópico {TOPIC_NAME}: {message}")

if __name__ == "__main__":
    produce_message()