from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from Core.dependency import get_db
from models.delivery import DeliveryPartner
from models.order import Order

router = APIRouter(prefix="/admin/delivery", tags=["Admin - Delivery"])

@router.get("/performance")
def delivery_partner_performance(
        admin: bool,
        db: Session = Depends((get_db))
):
    if not admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    data = (
        db.query(
            DeliveryPartner.id,
            func.count(Order.id).label("deliveries")
        )
        .join(Order, Order.delivery_partner_id == DeliveryPartner.id)
        .filter(Order.status == "DELIVERED")
        .group_by(DeliveryPartner.id)
        .all()
    )
    return [
        {
            "delivery_partner_id": row.id,
            "name": row.name,
            "completed_deliveries": row.deliveries,
        }
        for row in data
    ]