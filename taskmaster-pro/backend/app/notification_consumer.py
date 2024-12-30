import os
import json
import redis
from kafka import KafkaConsumer

KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER", "localhost:9092")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Create a Kafka consumer that subscribes to the 'taskmaster-notifications' topic
# and listens for new messages
consumer = KafkaConsumer(
    "taskmaster-notifications",
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="taskmaster-consumer-group",
)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def consume_notifications():
    # Continuously listen for new messages from the Kafka topic
    for message in consumer:
        # Retrieve the user ID and message from the Kafka message
        user_id = message.value["user_id"]
        notification = message.value["message"]
        # Store the notification in Redis
        r.lpush(f"user:{user_id}:notifications", notification)
        print(f"Notification for user {user_id}: {notification}")

if __name__ == "__main__":
    consume_notifications()