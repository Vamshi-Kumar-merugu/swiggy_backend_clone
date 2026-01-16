from http.client import HTTPException

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from Core.dependency import get_db
from Core.security import hash_password, verify_password, create_access_token
from models.user import User
from schemas.auth import RegisterRequest, TokenResponse, LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone == payload.phone).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")

    user = User(
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        role=payload.role,
        password_hash=hash_password(payload.password),
    )

    db.add(user)
    db.commit()

    return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == payload.phone).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(user.id), "role": user.role})

    return {"access_token": token, "token_type": "bearer"}

