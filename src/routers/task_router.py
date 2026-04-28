from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.auth.dependencies import get_current_user, require_roles
from src.db.session import get_db
from src.models.users_model import User
from src.schemas.task_schema import TaskAssign, TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from src.services.task_service import (
    assign_task,
    can_user_access_task,
    create_task,
    delete_task,
    get_task_or_404,
    list_tasks,
    update_task,
)


task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "manager")),
):
    return create_task(db, payload, current_user)


@task_router.get("", response_model=TaskListResponse)
def read_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    status_filter: str | None = Query(default=None, alias="status"),
    priority_filter: str | None = Query(default=None, alias="priority"),
    assigned_to_id: int | None = Query(default=None),
):
    return list_tasks(db, current_user, page, page_size, status_filter, priority_filter, assigned_to_id)


@task_router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_or_404(db, task_id)
    if not can_user_access_task(current_user, task):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return task


@task_router.patch("/{task_id}", response_model=TaskResponse)
def edit_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_or_404(db, task_id)
    if current_user.role == "user" and task.created_by_id != current_user.id and task.assigned_to_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return update_task(db, task_id, payload)


@task_router.post("/{task_id}/assign", response_model=TaskResponse)
def set_task_assignee(
    task_id: int,
    payload: TaskAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "manager")),
):
    return assign_task(db, task_id, payload.assigned_to_id)


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    delete_task(db, task_id)
