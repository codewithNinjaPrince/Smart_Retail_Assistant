from pydantic import BaseModel


class DemandInput(BaseModel):

    Price: float
    Discount: float
    Holiday: int
    Season: int
    Weather: int
    Customer_Footfall: int
    Marketing_Spend: float
    Competitor_Price: float
    Inventory_Level: int

    Year: int
    Month: int
    Day: int
    Weekday: int
    Quarter: int

    Profit_Margin: float
    Inventory_Ratio: float
    Marketing_Efficiency: float