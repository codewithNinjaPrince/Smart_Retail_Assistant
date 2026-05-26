import pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

print("\nLoading featured sales data...")
df = pd.read_csv("data/curated/featured_sales.csv")  # Load feature-engineered dataset

# Input features for prediction
features = ["Price","Discount","Holiday","Season","Weather",
            "Customer_Footfall","Marketing_Spend","Competitor_Price",
            "Inventory_Level","Year","Month","Day","Weekday","Quarter",
            "Profit_Margin","Inventory_Ratio","Marketing_Efficiency"]

target = "Units_Sold"  # Prediction target

# Split features and target
X=df[features] # To be trained on these features to predict the target variable
y=df[target] # The variable we want to predict, which is Units_Sold in this case

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining XGBoost model...")

# Create XGBoost regression model
model = XGBRegressor(
    n_estimators=200,   # Number of trees
    max_depth=8,        # Tree depth
    learning_rate=0.05, # Learning speed
    random_state=42
)

model.fit(X_train, y_train)          # Train model
predictions = model.predict(X_test)  # Generate predictions

# Evaluate model performance
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nModel Results")
print(f"MAE : {mae:.2f}")
print(f"R2 Score : {r2:.4f}")

# Save trained model
joblib.dump(model, "saved_models/demand_model.pkl")

print("\nModel Saved Successfully")