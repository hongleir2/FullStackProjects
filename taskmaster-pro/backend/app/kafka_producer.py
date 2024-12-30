import os
import json
from kafka import KafkaProducer

# Create a Kafka producer
KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVER', 'localhost:9092')
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define the topic to which messages will be sent
topic = 'taskmaster-notifications'

def send_notification(user_id: int, message: str):
    # Create a message to be sent to the Kafka topic
    notification = {
        'user_id': user_id,
        'message': message
    }
    # Send the message to the Kafka topic
    producer.send(topic, value=notification)
    producer.flush()