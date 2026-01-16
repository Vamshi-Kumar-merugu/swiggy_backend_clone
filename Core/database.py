from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="swiggy_user",
    password="swiggy123",
    host="127.0.0.1",
    port=5432,
    database="swiggy_db"
)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
