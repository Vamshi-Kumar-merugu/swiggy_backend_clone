from uuid import UUID
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    phone: str
    email: str | None = None
    role: str

class UserResponse(BaseModel):
    id: UUID
    name: str
    phone: str
    email: str|None
    role: str

    class Config:
        from_attributes = True