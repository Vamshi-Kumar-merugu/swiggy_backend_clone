from pydantic import BaseModel
from uuid import UUID

class AssignDeliveryRequest(BaseModel):
    order_id: UUID
    delivery_partner_id: UUID

class OrderTrackingResponse(BaseModel):
    order_id: UUID
    status: str
    delivery_partner_id: UUID | None