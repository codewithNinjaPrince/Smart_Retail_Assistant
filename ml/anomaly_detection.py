import os, joblib, pandas as pd
from sklearn.ensemble import IsolationForest # Anomaly detection model
from sklearn.preprocessing import StandardScaler # Scale values to same range

print("Loading sales data...")
df = pd.read_csv("data/curated/featured_sales.csv") # Load feature engineered dataset

# Features used for anomaly detection
features=["Units_Sold","Price","Discount",
          "Customer_Footfall","Marketing_Spend",
          "Inventory_Level","Profit"]

X=df[features] # Extract selected columns

# Scale data because features have different ranges
scaler=StandardScaler()
X_scaled=scaler.fit_transform(X)

print("Training anomaly model...")

# Create anomaly detection model
model=IsolationForest(
    contamination=0.03, # Assume 3% records are anomalies
    random_state=42,    
    n_estimators=100,   # Number of trees
    n_jobs=-1           # Use all CPU cores
)

# Predict anomalies
# 1 = normal , -1 = anomaly
df["Anomaly"]=model.fit_predict(X_scaled)

print("Generating anomaly reasons...")

# Create thresholds using dataset statistics
high_sales=df["Units_Sold"].quantile(0.90)
high_discount=df["Discount"].quantile(0.90)
high_footfall=df["Customer_Footfall"].quantile(0.90)
low_inventory=df["Inventory_Level"].quantile(0.10)
high_marketing=df["Marketing_Spend"].quantile(0.90)
high_price=df["Price"].quantile(0.90)

# Function to identify anomaly reasons
def detect_reason(row):

    reasons=[] # Store all detected reasons

    if row["Profit"]<0:
        reasons.append("negative profit")

    if row["Discount"]>high_discount:
        reasons.append("high discount")

    if row["Customer_Footfall"]>high_footfall:
        reasons.append("high customer traffic")

    if row["Inventory_Level"]<low_inventory:
        reasons.append("low inventory")

    if row["Marketing_Spend"]>high_marketing:
        reasons.append("high marketing spend")

    if row["Price"]>high_price:
        reasons.append("high pricing")

    if row["Units_Sold"]>high_sales:
        reasons.append("high sales volume")

    # Business anomaly categories

    if row["Profit"]<0 and row["Discount"]>high_discount:
        anomaly="Discount Loss"

    elif row["Inventory_Level"]<low_inventory and row["Units_Sold"]>high_sales:
        anomaly="Inventory Risk"

    elif row["Customer_Footfall"]>high_footfall and row["Units_Sold"]<high_sales*0.25:
        anomaly="Conversion Anomaly"

    elif row["Marketing_Spend"]>high_marketing and row["Profit"]<0:
        anomaly="Marketing Inefficiency"

    elif row["Price"]>high_price and row["Units_Sold"]<high_sales*0.5:
        anomaly="Pricing Anomaly"

    elif row["Profit"]<0:
        anomaly="Loss Anomaly"

    elif len(reasons)>=2:
        anomaly="Complex Behavior Pattern"

    else:
        anomaly="Behavior Shift"

    # Combine reasons into text
    reason=", ".join(reasons) if reasons else "Unusual feature combination"

    return anomaly,reason


# Default values for all records
df["Anomaly_Type"]="Normal"
df["Reason"]="Normal"

# Select anomaly rows only
mask=df["Anomaly"]==-1

# Assign anomaly type and reason
for idx in df[mask].index:
    anomaly_type,reason=detect_reason(df.loc[idx])

    df.loc[idx,"Anomaly_Type"]=anomaly_type
    df.loc[idx,"Reason"]=reason

# Count normal and anomaly records
normal_count=(df["Anomaly"]==1).sum()
anomaly_count=(df["Anomaly"]==-1).sum()

# Create folder if not present
os.makedirs("saved_models",exist_ok=True)

# Save trained model and scaler
joblib.dump(model,"saved_models/anomaly_model.pkl")
joblib.dump(scaler,"saved_models/scaler.pkl")

# Save output dataset
df.to_csv("data/curated/sales_anomalies.csv",index=False)

print("\nResults")

print(f"Normal Records : {normal_count}")
print(f"Anomalies Found : {anomaly_count}")

# Show sample anomaly records
print("\nSample anomalies:\n")
print(df[df["Anomaly"]==-1][["Anomaly_Type","Reason"]].head(10))

print("\nModel saved successfully")