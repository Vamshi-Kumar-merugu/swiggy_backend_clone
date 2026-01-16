

from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from sqlalchemy.orm import Session

from Core.dependency import get_db
from models.order import Order
from models.payment import Payment
from schemas.payments import PaymentResponse, PaymentRequest

router = APIRouter(prefix="/payments",tags=["payments"])

@router.post("/pay", response_model=PaymentResponse)
def make_payment(
        payload: PaymentRequest,
        user_id: UUID,
        db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id==payload.order_id).first()

    if not order:
        raise  HTTPException(status_code=404, detail="Order not found")

    if order.status != "CREATED":
        raise HTTPException(status_code=400, detail="Order Already paid or invalid")

    payment = Payment(
        order_id = order.id,
        user_id = user_id,
        amount = order.total_amount,
        status = "SUCCESS",
        payment_method = payload.payment_method
    )
    db.add(payment)
    order.status = "PAID"

    db.commit()

    return {
        "payment_id": payment.id,
        "status": payment.status,
        "order_id": order.id,
        "amount": payment.amount
    }