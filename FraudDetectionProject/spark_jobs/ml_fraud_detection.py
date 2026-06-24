import pandas as pd
import joblib
import json
import os

from kafka import KafkaConsumer

# Load trained model
model = joblib.load("model/fraud_model.pkl")

# Kafka Consumer
consumer = KafkaConsumer(
    "creditcard_transactions",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

# Output CSV file
output_file = "data/predictions.csv"

# Create file if it doesn't exist
if not os.path.exists(output_file):
    with open(output_file, "w") as f:
        f.write("Amount,Actual,Prediction\n")

count = 0
fraud_count = 0

print("ML Fraud Detection Started...")
print("-" * 50)

for message in consumer:

    transaction = message.value

    # Create dataframe for prediction
    X = pd.DataFrame([transaction])

    # Get actual label before dropping
    actual = int(transaction.get("Class", 0))

    # Remove target column
    if "Class" in X.columns:
        X = X.drop("Class", axis=1)

    # Predict
    prediction = int(model.predict(X)[0])

    count += 1

    if prediction == 1:
        fraud_count += 1

        print(
            f"🚨 FRAUD DETECTED | "
            f"Amount={transaction['Amount']} | "
            f"Actual={actual}"
        )

    # Save prediction to CSV
    with open(output_file, "a") as f:
        f.write(
            f"{transaction['Amount']},{actual},{prediction}\n"
        )

    # Progress update every 100 transactions
    if count % 100 == 0:
        print(
            f"Processed={count} | "
            f"Fraud Predicted={fraud_count}"
        )