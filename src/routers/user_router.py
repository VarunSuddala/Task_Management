from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.auth.dependencies import require_roles
from src.db.session import get_db
from src.schemas.user_schema import UserResponse, UserUpdate
from src.services.user_service import delete_user, get_user_by_id, list_users, update_user


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("", response_model=list[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin")),
):
    return list_users(db)


@user_router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin")),
):
    return get_user_by_id(db, user_id)


@user_router.patch("/{user_id}", response_model=UserResponse)
def edit_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin")),
):
    return update_user(db, user_id, payload)


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin")),
):
    delete_user(db, user_id)


