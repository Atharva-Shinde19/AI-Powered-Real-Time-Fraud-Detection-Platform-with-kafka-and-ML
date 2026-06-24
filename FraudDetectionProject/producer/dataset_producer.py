import pandas as pd
import json
import time

from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

df = pd.read_csv("data/creditcard.csv")

print(f"Loaded {len(df)} transactions")

for index, row in df.iterrows():

    transaction = row.to_dict()

    producer.send(
        "creditcard_transactions",
        transaction
    )

    if index % 100 == 0:
        print(f"Sent {index} transactions")

    time.sleep(0.01)

producer.flush()

print("All transactions sent successfully")