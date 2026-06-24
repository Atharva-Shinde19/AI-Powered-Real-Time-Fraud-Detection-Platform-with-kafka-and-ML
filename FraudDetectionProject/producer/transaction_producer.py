from kafka import KafkaProducer
from faker import Faker
import json
import random
import time

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:

    transaction = {
        "transaction_id": random.randint(1000, 9999),
        "user_id": random.randint(1, 100),
        "amount": round(random.uniform(10, 5000), 2),
        "merchant": fake.company(),
        "location": fake.city(),
        "is_fraud": random.choice([0, 0, 0, 0, 1])
    }

    producer.send("transactions", transaction)

    print(transaction)

    time.sleep(2)