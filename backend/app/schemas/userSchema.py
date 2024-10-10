from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class CreateUser(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    joined_at: datetime