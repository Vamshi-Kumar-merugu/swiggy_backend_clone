import uuid
from sqlalchemy import Column, String, ForeignKey, Boolean, Numeric, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from models.base import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    location = Column(String)
    is_open = Column(Boolean, default=True)
    rating = Column(Numeric(2,1))
    created_at = Column(TIMESTAMP, server_default=func.now())