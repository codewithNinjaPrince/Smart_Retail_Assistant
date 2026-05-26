import pandas as pd

# Extracting data from raw folder
df = pd.read_csv("data/raw/sales.csv")

# Dataset inspection--> will give no of rows and columns in the dataset
print("Shape:", df.shape)

print("\nColumns:") # printing column name in the list
print(df.columns.tolist())

# Checking for missing values in the dataset
print("\nMissing Values:") 
print(df.isnull().sum())

df = df.drop_duplicates() # Remove duplicate rows

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])
# because previously it was in string format which is not suitable for time series analysis 

# Saving cleaned data to processed folder, without index column
df.to_csv("data/processed/cleaned_sales.csv",index=False)

print("\nSales data cleaned successfully")
print(df.info()) # metadata or information about the dataset, like data types and non-null counts