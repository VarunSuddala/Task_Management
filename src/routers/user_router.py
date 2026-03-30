from fastapi import FastAPI,HTTPException,Query
from fastapi import APIRouter,Depends
from schemas.user_schema import  UserCreate,UserUpdate,UserResponse
from sqlalchemy.orm import Session
from core.db import get_db
from services.user_service import create_user
user_router =APIRouter(prefix="/users", tags=["users"])


@user_router.post("/register")
def register_user(user_data:UserCreate,db:Session=Depends(get_db)):
    create_user(user_data,db)
    return {"message": "User registered successfully", "user": user_data}



@user_router.post("/login")
def login_user(login_data:UserResponse):
    return {"message": "User logged in successfully"}

@user_router.get("/me")
def get_current_user():
    return {"message": "Current user details"}

