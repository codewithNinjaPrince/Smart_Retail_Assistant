from fastapi import APIRouter
from schemas.demand_schema import DemandInput

import joblib
import pandas as pd


router = APIRouter()

print("Loading demand model...")


model = joblib.load(
    "saved_models/demand_model.pkl"
)


df = pd.read_csv(
    "data/curated/featured_sales.csv"
)


low_demand = df["Units_Sold"].quantile(
    0.25
)

high_demand = df["Units_Sold"].quantile(
    0.75
)


@router.post("/predict-demand")
def predict_demand(data: DemandInput):


    values = [[
        data.Price,
        data.Discount,
        data.Holiday,
        data.Season,
        data.Weather,
        data.Customer_Footfall,
        data.Marketing_Spend,
        data.Competitor_Price,
        data.Inventory_Level,

        data.Year,
        data.Month,
        data.Day,
        data.Weekday,
        data.Quarter,

        data.Profit_Margin,
        data.Inventory_Ratio,
        data.Marketing_Efficiency
    ]]


    columns = [

        "Price",
        "Discount",
        "Holiday",
        "Season",
        "Weather",
        "Customer_Footfall",
        "Marketing_Spend",
        "Competitor_Price",
        "Inventory_Level",

        "Year",
        "Month",
        "Day",
        "Weekday",
        "Quarter",

        "Profit_Margin",
        "Inventory_Ratio",
        "Marketing_Efficiency"
    ]


    X = pd.DataFrame(
        values,
        columns=columns
    )


    prediction = model.predict(
        X
    )[0]


    if prediction < low_demand:

        demand_level = "Low"

    elif prediction > high_demand:

        demand_level = "High"

    else:

        demand_level = "Medium"



    if demand_level == "High":

        recommendation = (
            "Increase inventory and stock levels, prepare warehouse stock and allocate additional resources"
        )


    elif demand_level == "Low":

        recommendation = (
            "Avoid overstocking and consider promotional campaigns"
        )


    else:

        recommendation = (
            "Maintain balanced inventory and monitor demand trends"
        )


    return {

        "predicted_units_sold":
        round(
            float(prediction),
            2
        ),

        "demand_level":
        demand_level,

        "recommendation":
        recommendation,

        "business_insight":
        f"Expected demand is {demand_level.lower()} with approximately {round(float(prediction))} unit sales."
    }