from pydantic import BaseModel
from decimal import Decimal
from uuid import UUID

class MenuCreate(BaseModel):
    name: str
    price: Decimal

class MenuResponse(BaseModel):
    id:UUID
    name: str
    price: Decimal
    is_available: bool

    class Config:
        from_attributes = True