from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from decimal import  Decimal
from Core.dependency import get_db
from models.payment import Payment

router = APIRouter(prefix="/admin/payouts",tags=["Admin - Payouts"])

@router.get("/")
def payout_summary(
    admin: bool,
    db: Session = Depends(get_db)
):
    if not admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    total_collected = (
        db.query(func.sum(Payment.amount))
        .filter(Payment.status == "SUCCESS")
        .scalar()
    ) or Decimal("0.00")

    platform_commission = total_collected * Decimal("0.20")
    restaurant_payout = total_collected * Decimal("0.80")

    return {
        "total_collected": total_collected or 0,
        "platform_commission": platform_commission,
        "restaurant_payout": restaurant_payout,
    }
