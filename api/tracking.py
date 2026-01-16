from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from sqlalchemy.orm import Session

from Core.auth import get_current_user
from Core.dependency import get_db
from models.order import Order

router = APIRouter(prefix="/tracking", tags=["Live Tracking"])

@router.get("/{ordr_id}")
def track_order_live(
        order_id: UUID,
        current_user = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == current_user["id"]
        )
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not Found")

    return {
        "order_id": order.id,
        "status": order.status,
        "delivery_partner_id": order.delivery_partner_id,
        "last_updated": order.updated_at,
    }