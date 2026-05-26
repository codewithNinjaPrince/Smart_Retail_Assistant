from fastapi import APIRouter
from schemas.anomaly_schema import SalesInput
import joblib
import pandas as pd

router = APIRouter()

print("Loading anomaly model...")

model = joblib.load(
    "saved_models/anomaly_model.pkl"
)

scaler = joblib.load(
    "saved_models/scaler.pkl"
)

df = pd.read_csv(
    "data/curated/featured_sales.csv"
)


high_sales=df["Units_Sold"].quantile(0.90)
high_discount=df["Discount"].quantile(0.90)
high_footfall=df["Customer_Footfall"].quantile(0.90)
low_inventory=df["Inventory_Level"].quantile(0.10)
high_marketing=df["Marketing_Spend"].quantile(0.90)
high_price=df["Price"].quantile(0.90)


def detect_reason(row):

    reasons=[]

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


    if "low inventory" in reasons and "high pricing" in reasons:
        anomaly="Supply Constraint"

    elif "high discount" in reasons and "high sales volume" in reasons:
        anomaly="Promotional Surge"

    elif "high customer traffic" in reasons and "high sales volume" in reasons:
        anomaly="Traffic Driven Sales"

    elif "high pricing" in reasons and "high sales volume" in reasons:
        anomaly="Demand Spike"

    elif "high pricing" in reasons:
        anomaly="Pricing Shift"

    elif "high sales volume" in reasons:
        anomaly="Sales Spike"

    else:
        anomaly="Behavior Shift"

    return anomaly,", ".join(reasons)


@router.post("/predict-anomaly",summary="Predict Anomaly",)
def predict(data:SalesInput):

    values=[[
        data.Units_Sold,
        data.Price,
        data.Discount,
        data.Customer_Footfall,
        data.Marketing_Spend,
        data.Inventory_Level,
        data.Profit
    ]]

    scaled=scaler.transform(values)

    prediction=model.predict(
        scaled
    )[0]


    row={

        "Units_Sold":data.Units_Sold,
        "Price":data.Price,
        "Discount":data.Discount,
        "Customer_Footfall":data.Customer_Footfall,
        "Marketing_Spend":data.Marketing_Spend,
        "Inventory_Level":data.Inventory_Level,
        "Profit":data.Profit
    }


    anomaly_type,reason=detect_reason(
        row
    )


    if prediction==-1:

        return{

            "status":"Anomaly Detected",

            "anomaly_type":anomaly_type,

            "reason":reason

        }


    return{

        "status":"Normal",

        "reason":"No anomaly found"

    }