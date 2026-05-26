from pydantic import BaseModel
from typing import Optional

class DocumentData(BaseModel):

    invoice_id: Optional[str]=None
    supplier: Optional[str]=None
    amount: Optional[str]=None
    date: Optional[str]=None
    address: Optional[str]=None