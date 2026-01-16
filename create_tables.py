from Core.database import engine
from models.base import Base
from models.delivery import DeliveryPartner
from models.menu import MenuItem
from models.order import OrderItem, Order
from models.payment import Payment
from models.restaurant import Restaurant
from models.review import Review
from models.user import User


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully.")


if __name__ == "__main__":
    create_tables()
