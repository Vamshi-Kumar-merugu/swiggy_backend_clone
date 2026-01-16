import uuid

from sqlalchemy import Column, UUID, ForeignKey, Integer, Text

from models.base import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid = True), primary_key=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"))
    rating = Column(Integer)
    comment = Column(Text)