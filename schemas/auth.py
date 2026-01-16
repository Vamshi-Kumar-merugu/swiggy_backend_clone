from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    name: str
    phone: str
    email: str | None = None
    password: str = Field(
        min_length=8,
        max_length=64,
        description="Password must be between 8 and 64 characters"
    )
    role: str

class LoginRequest(BaseModel):
    phone: str
    password: str

class TokenResponse(BaseModel):
    access_token : str
    token_type: str = "bearer"