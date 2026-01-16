from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from typing import List

class OrderItemResponse(BaseModel):
    menu_item_id: UUID
    name: str
    price: Decimal
    quantity: int

class OrderResponse(BaseModel):
    id: UUID
    restaurant_id: UUID
    status: str
    total_amount: Decimal
    items : List[OrderItemResponse]