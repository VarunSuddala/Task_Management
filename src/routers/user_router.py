from fastapi import FastAPI,HTTPException,Query
from fastapi import APIRouter,Depends
from src.schemas.user_schema import  UserCreate,UserResponse
user_router =APIRouter(prefix="/users", tags=["users"])


@user_router.post("/register")
def register_user(user_data:UserCreate):
    return {"message": "User registered successfully", "user": user_data}



@user_router.post("/login")
def login_user(login_data:UserResponse):
    return {"message": "User logged in successfully"}

@user_router.get("/me")
def get_current_user():
    return {"message": "Current user details"}

