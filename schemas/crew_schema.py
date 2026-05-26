from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Input only
class RetailRequest(BaseModel):
    total_sales: float
    monthly_growth: float
    top_category: str


# Stored in DB
class RetailAnalysis(BaseModel):
    total_sales: float
    monthly_growth: float
    top_category: str

    ai_analysis: Optional[str] = None
    created_at: datetime = datetime.utcnow()