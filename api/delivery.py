from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from Core.dependency import get_db
from models.delivery import DeliveryPartner
from models.order import Order
from schemas.delivery import AssignDeliveryRequest, OrderTrackingResponse

router = APIRouter(prefix="/delivery", tags=["Delivery"])

@router.post("/assign")
def assign_delivery(
        payload: AssignDeliveryRequest,
        db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == payload.order_id).first()
    partner = db.query(DeliveryPartner).filter(
        DeliveryPartner.id == payload.delivery_partner_id
    ).first()

    if not order or not partner:
        raise HTTPException(status_code=404, detail="Order or partner not found")

    if not partner.is_availble:
        raise HTTPException(status_code=400, detail="Partner not available")

    order.delivery_partner_id = partner.id
    order.status = "CONFIRMED"
    partner.is_availble = False

    db.commit()
    return {"message": "Delivery partner assigned"}

@router.post("/updates-status")
def update_delivery_status(
        order_id : UUID,
        status: str,
        db: Session = Depends(get_db)
):
    valid_status = [
        "CONFIRMED",
        "PICKED_UP",
        "OUT_FOR_DELIVERY",
        "DELIVERED"
    ]

    if status not in valid_status:
        raise  HTTPException(status_code=400, detail="Invalid_status")

    order = db.query(Order). filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status

    if status == " DELIVERED":
        partner = db.query(DeliveryPartner).filter(
            DeliveryPartner.id == order.delivery_partner_id
        ).first()
        if partner:
            partner.is_availble = True
    db.commit()
    return {"message": f"Order status updated to {status}"}

@router.get("/track/{order_id}", response_model=OrderTrackingResponse)
def track_order(order_id: UUID, db:Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order Not found")

    return {
        "order_id": order.id,
        "status": order.status,
        "delivery_partner_id": order.delivery_partner_id,
    }