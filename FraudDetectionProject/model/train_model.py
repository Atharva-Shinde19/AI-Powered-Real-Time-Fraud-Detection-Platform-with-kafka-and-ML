import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load dataset
df = pd.read_csv("data/creditcard.csv")

# Features and target
X = df.drop("Class", axis=1)
y = df["Class"]

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "model/fraud_model.pkl")

print("\nModel saved as fraud_model.pkl")