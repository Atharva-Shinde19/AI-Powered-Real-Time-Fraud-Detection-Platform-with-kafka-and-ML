import pandas as pd

df = pd.read_csv("data/creditcard.csv")

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nClass Distribution:")
print(df["Class"].value_counts())

print("\nFirst 5 Rows:")
print(df.head())