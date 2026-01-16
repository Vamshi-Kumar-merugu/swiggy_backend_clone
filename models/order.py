import uuid
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, String, Numeric, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('restaurants.id'))
    status = Column(String(30))
    total_amount = Column(Numeric(10,2))
    delivery_partner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("delivery_partners.id"),
        nullable=True
    )
    created_at = Column(TIMESTAMP, server_default=func.now())

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(40))
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    menu_item_id = Column(UUID(as_uuid=True), ForeignKey("menu_items.id"))
    quantity = Column(Numeric)
    price = Column(Numeric(10,2))
