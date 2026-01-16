from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from Core.dependency import get_db
from models.restaurant import Restaurant
from schemas.restaurant import RestaurantResponse, RestaurantCreate

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.post("/", response_model=RestaurantResponse, status_code=201)
def create_restaurant(
        payload: RestaurantCreate,
        db: Session = Depends(get_db),
):
    owner_id = "1a364776-8cf1-42e1-8227-b5cb646426f6"

    restaurant = Restaurant(
        name= payload.name,
        location = payload.location,
        owner_id = owner_id
    )

    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    return restaurant

@router.get("/", response_model=list[RestaurantResponse])
def list_restaurants(db:Session = Depends(get_db)):
    return db.query(Restaurant).filter(Restaurant.is_open==True).all()