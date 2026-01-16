import uuid
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Numeric
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid = True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"),nullable=False)
    amount = Column(Numeric(10,2), nullable=False)
    status = Column(String(20), nullable=False)
    payment_method = Column(String(30))    # Razorpay, Strip
    created_at = Column(TIMESTAMP, server_default=func.now())