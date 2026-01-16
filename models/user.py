import uuid
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    phone = Column(String(15), unique=True, nullable=False)
    email = Column(String(100))
    role = Column(String(20))  # USER, RESTAURANT, DELIVERY, ADMIN
    password_hash = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())