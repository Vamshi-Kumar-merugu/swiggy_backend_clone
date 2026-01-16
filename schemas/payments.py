from pydantic import BaseModel
from uuid import UUID
from decimal import  Decimal


class PaymentRequest(BaseModel):
    order_id: UUID
    payment_method: str  #upi/card/cod

class PaymentResponse(BaseModel):
    payment_id : UUID
    status: str
    order_id: UUID
    amount: Decimal