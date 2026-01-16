from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from Core.dependency import get_db
from models import order
from models.order import Order

router = APIRouter(prefix="/admin/orders", tags=["Admin - orders"])

@router.get("/")
def get_all_orders(
        admin: bool,
        db: Session = Depends(get_db)
):
    if not admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    orders = db.query(Order).order_by(Order.created_at.desc()).all()

    return [
        {
            "order_id": order.id,
            "user_id": order.user_id,
            "restaurant_id": order.restaurant_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
        }
        for order in orders
    ]

@router.get("/status/{status}")
def get_orders_by_status(
        status: str,
        admin: bool,
        db: Session = Depends(get_db)
):
    if not admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    orders = db.query(Order).filter(order.status == status).all()

    return [
        {
            "order_id": order.id,
            "user_id": order.user_id,
            "restaurant_id": order.restaurant_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
        }
        for order in orders
    ]