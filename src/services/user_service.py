from schemas.user_schema import  UserCreate,UserUpdate,UserResponse
from sqlalchemy.orm import Session
from models.users_model import User
def create_user(user_data:UserCreate,db:Session):
    # Logic to create a user in the database
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,  # In a real application, make sure to hash the password
        role=user_data.role,
        is_active=user_data.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user