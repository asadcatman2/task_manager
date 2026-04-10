from pydantic import BaseModel, EmailStr
from datetime import datetime
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class ForgotPasswordRequest(BaseModel):
    email: EmailStr
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    class Config:
        from_attributes = True