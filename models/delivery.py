import uuid
from sqlalchemy.sql import func
from sqlalchemy import Column, UUID, ForeignKey, Boolean, String, TIMESTAMP

from models.base import Base


class DeliveryPartner(Base):
    __tablename__= "delivery_partners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    phone = Column(String(15), unique=True, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
