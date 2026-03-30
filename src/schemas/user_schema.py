from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "member"
    is_active: bool = True
class UserUpdate(BaseModel):
    username: str = None
    email: EmailStr = None
    password: str = None
    role: str = None
    is_active: bool = None
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        orm_mode = True