import json
from fastapi import APIRouter, HTTPException
from uuid import UUID

from Core.redis import redis_client
from schemas.cart import AddToCartRequest

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_cart_key(user_id: str) -> str:
    return f"cart:{user_id}"

@router.post("/add")
def add_to_cart(
        payload: AddToCartRequest,
        user_id: UUID
):
    cart_key= get_cart_key(user_id)
    cart_data = redis_client.get(cart_key)

    if cart_data:
        cart = json.loads(cart_data)
    else:
        cart = {
            "restaurant_id": str(payload.restaurant_id),
            "items": {}
        }
    if cart["restaurant_id"] != str(payload.restaurant_id):
        raise HTTPException(
            status_code=400,
            detail="Cart already contains items from another restaurant"
        )

    item_id = str(payload.menu_item_id)

    if item_id in cart["items"]:
        cart["items"][item_id]["quantity"] += payload.quantity
    else:
        cart["items"][item_id] = {
            "name": payload.name,
            "price": float(payload.price),
            "quantity": payload.quantity
        }
    redis_client.setex(
        cart_key,
        60*60,
        json.dumps(cart)
    )

    return {"message": "Item added to cart"}

@router.get("/")
def view_cart(user_id: UUID):
    cart_key = get_cart_key(user_id)
    cart_data = redis_client.get(cart_key)

    if not cart_data:
        return {"message": "Cart is empty"}

    return json.loads(cart_data)

@router.delete("/remove/{menu_item_id}")
def remove_from_cart(menu_item_id: UUID, user_id: UUID):
    cart_key = get_cart_key(user_id)
    cart_data = redis_client.get(cart_key)

    if not cart_data:
        raise HTTPException(
            status_code=404, detail="Cart is empty"
        )
    cart = json.loads(cart_data)
    item_id = str(menu_item_id)

    if item_id not  in cart["items"]:
        raise HTTPException(status_code=404, detail="Item not in cart")

    del cart["items"][item_id]

    if not cart["items"]:
        redis_client.delete(cart_key)
    else:
        redis_client.setex(cart_key, 3600, json.dumps(cart))

    return {"message": "Item removed"}