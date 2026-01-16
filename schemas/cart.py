from pydantic import BaseModel
from uuid import UUID
from decimal import  Decimal

class AddToCartRequest(BaseModel):
    restaurant_id: UUID
    menu_item_id: UUID
    name: str
    price: Decimal
    quantity: int = 1

class CartItemResponse(BaseModel):
    menu_item_id: UUID
    name: str
    price: Decimal
    quantity: int