from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.auth.dependencies import get_current_user
from src.db.session import get_db
from src.schemas.user_schema import TokenResponse, UserCreate, UserLogin, UserResponse
from src.services.auth_service import authenticate_user, register_user


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, payload)


@auth_router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return authenticate_user(db, payload)


@auth_router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user)):
    return current_user
