from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from Core.dependency import get_db
from models.order import Order

router = APIRouter(prefix="/admin/restaurants", tags=["Admin - Restaurants"])

@router.get("/revenue")
def restaurant_revenue(
        admin: bool,
        db: Session = Depends(get_db)
):
    if not admin:
        raise  HTTPException(status_code=403, detail="Admin access required")

    data = (
        db.query(
            Order.restaurant_id,
            func.sum(Order.total_amount).label("revenue"),
            func.count(Order.id).label("orders_count")
        )
        .filter(Order.status == "DELIVERED")
        .group_by(Order.restaurant_id)
        .all()
    )
    return [
        {
            "restaurant_id": row.restaurant_id,
            "total_revenue": row.revenue,
            "orders": row.orders_count,
        }
        for row in data
    ]