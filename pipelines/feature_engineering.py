import os # Used for operating system related tasks, mainly creating folders.
import joblib # Used to save Python objects to a file and load them later.
import pandas as pd # for the pandas operations on the dataset
from sklearn.preprocessing import LabelEncoder # Used to convert categorical variables into numerical format

df = pd.read_csv("data/processed/cleaned_sales.csv") # Load cleaned dataset

# Date conversion + date features
df["Date"] = pd.to_datetime(df["Date"])

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df["Weekday"] = df["Date"].dt.dayofweek
df["Quarter"] = df["Date"].dt.quarter


# Business features
df["Profit_Margin"] = df["Profit"] / ((df["Units_Sold"] * df["Price"]) + 1)
df["Inventory_Ratio"] = df["Inventory_Level"] / (df["Units_Sold"] + 1)
df["Marketing_Efficiency"] = df["Profit"] / (df["Marketing_Spend"] + 1)

# Encode categorical columns
categorical_cols = ["Holiday", "Season", "Weather", "City", "Category"]

encoders = {}
for col in categorical_cols:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])
    encoders[col] = encoder

os.makedirs("saved_models", exist_ok=True) # Save encoders

joblib.dump(encoders,"saved_models/encoders.pkl")

df.to_csv("data/curated/featured_sales.csv",index=False) # Saving file to curated folder as featured_sales.csv, without index column

print("\nFeature engineering completed") # Storing all learned mappings in encoders.pkl

print("\nFeatures Added:")
print(["Year","Month","Day","Weekday","Quarter","Profit_Margin","Inventory_Ratio","Marketing_Efficiency"])

print("\nEncoded:")
print(categorical_cols)

print("\nFinal Shape:", df.shape)