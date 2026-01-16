import uuid

from sqlalchemy import Column, ForeignKey, String, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('restaurants.id'))
    name = Column(String(100))
    price = Column(Numeric(10,2))
    is_available = Column(Boolean, default=True)