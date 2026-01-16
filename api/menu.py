from fastapi import APIRouter
from uuid import UUID

from fastapi.params import Depends
from sqlalchemy.orm import Session

from Core.dependency import get_db
from models.menu import MenuItem
from schemas.menu import MenuResponse, MenuCreate

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.post("/{restaurant_id}", response_model=MenuResponse)
def add_menu_item(
        restaurant_id: UUID,
        payload: MenuCreate,
        db: Session= Depends(get_db)
):
    item = MenuItem(
        restaurant_id= restaurant_id,
        name = payload.name,
        price = payload.price
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item

@router.get("/{restaurant_id}", response_model=list[MenuResponse])
def get_menu(restaurant_id: UUID, db:Session=Depends(get_db)):
    return (
        db.query(MenuItem)
        .filter(MenuItem.restaurant_id == restaurant_id,
                MenuItem.is_available == True
        )
        .all()
    )