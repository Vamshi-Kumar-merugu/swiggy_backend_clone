from pydantic import BaseModel
from uuid import UUID

class RestaurantCreate(BaseModel):
    name: str
    location: str

class RestaurantResponse(BaseModel):
    id: UUID
    name: str
    location: str
    is_open: bool

    class Config:
        from_attributes = True
