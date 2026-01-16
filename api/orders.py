import json

from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session

from Core.auth import get_current_user
from Core.dependency import get_db
from Core.redis import redis_client
from models.order import Order, OrderItem
from schemas.order import OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_cart_key(user_id: str) -> str:
    return f"cart:{user_id}"

@router.post("/place", response_model=OrderResponse, status_code=201)
def place_order(current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    cart_key = f"cart:{current_user["id"]}"
    cart_data = redis_client.get(cart_key)

    if not cart_data:
        raise HTTPException(status_code=400, detail="Cart is empty")

    cart = json.loads(cart_data)

    total_amount = sum(
        Decimal(item["price"]) * item["quantity"]
        for item in cart["items"].values()
    )

    order = Order(
        user_id=current_user["id"],
        restaurant_id=UUID(cart["restaurant_id"]),
        total_amount=total_amount,
        status="CREATED",
    )

    db.add(order)
    db.flush()  # now order.id exists

    order_items_response = []

    for menu_item_id, item in cart["items"].items():
        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=UUID(menu_item_id),
            name=item["name"],
            price=item["price"],
            quantity=item["quantity"],
        )
        db.add(order_item)

        order_items_response.append({
            "menu_item_id": UUID(menu_item_id),
            "name": item["name"],
            "price": item["price"],
            "quantity": item["quantity"],
        })

    db.commit()

    redis_client.delete(cart_key)

    return {
        "id": order.id,
        "restaurant_id": order.restaurant_id,
        "status": order.status,
        "total_amount": order.total_amount,
        "items": order_items_response,
    }

@router.get("/history", response_model=list[OrderResponse])
def get_order_history(
        user_id: UUID,
        db: Session = Depends(get_db)
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )
    result = []

    for order in orders:
        items = (
            db.query(OrderItem)
            .filter(OrderItem.order_id == order.id)
            .all()
        )

        result.append({
            "id": order.id,
            "restaurant_id": order.restaurant_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "items":[
                {
                    "menu_item_id": items
                }
            ]
        })

