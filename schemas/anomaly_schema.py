from pydantic import BaseModel


class SalesInput(BaseModel):

    Units_Sold: int
    Price: float
    Discount: float
    Customer_Footfall: int
    Marketing_Spend: float
    Inventory_Level: int
    Profit: float