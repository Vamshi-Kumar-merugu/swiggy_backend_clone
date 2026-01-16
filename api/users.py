import uuid

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from Core.dependency import get_db
from models.user import User
from schemas.user import UserResponse, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user(
        payload: UserCreate,
        db: Session = Depends(get_db)
):
    user = User(
        id = uuid.uuid4(),
        name = payload.name,
        phone = payload.phone,
        email = payload.email,
        role= payload.role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user