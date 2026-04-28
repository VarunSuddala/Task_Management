import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.db.redis_client import get_redis_client
from src.models.task_model import Task
from src.models.users_model import User
from src.schemas.task_schema import TaskCreate, TaskUpdate
from src.utils.pagination import get_offset


def _cache_key(
    viewer_id: int,
    role: str,
    page: int,
    page_size: int,
    status_filter: str | None,
    priority_filter: str | None,
    assigned_to_id: int | None,
) -> str:
    return (
        f"tasks:list:viewer={viewer_id}:role={role}:page={page}:size={page_size}"
        f":status={status_filter or 'all'}:priority={priority_filter or 'all'}:assignee={assigned_to_id or 'all'}"
    )


def invalidate_task_cache() -> None:
    redis_client = get_redis_client()
    try:
        for key in redis_client.scan_iter("tasks:list:*"):
            redis_client.delete(key)
    except Exception:
        pass


def can_user_access_task(user: User, task: Task) -> bool:
    if user.role in {"admin", "manager"}:
        return True
    return task.created_by_id == user.id or task.assigned_to_id == user.id


def create_task(db: Session, payload: TaskCreate, creator: User) -> Task:
    if payload.assigned_to_id is not None:
        assignee = db.query(User).filter(User.id == payload.assigned_to_id).first()
        if not assignee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assigned user not found")

    task = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        due_date=payload.due_date,
        created_by_id=creator.id,
        assigned_to_id=payload.assigned_to_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    invalidate_task_cache()
    return task


def get_task_or_404(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


def update_task(db: Session, task_id: int, payload: TaskUpdate) -> Task:
    task = get_task_or_404(db, task_id)

    if payload.title is not None:
        task.title = payload.title
    if payload.description is not None:
        task.description = payload.description
    if payload.status is not None:
        task.status = payload.status
    if payload.priority is not None:
        task.priority = payload.priority
    if payload.due_date is not None:
        task.due_date = payload.due_date
    if payload.assigned_to_id is not None:
        assignee = db.query(User).filter(User.id == payload.assigned_to_id).first()
        if not assignee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assigned user not found")
        task.assigned_to_id = payload.assigned_to_id

    db.commit()
    db.refresh(task)
    invalidate_task_cache()
    return task


def assign_task(db: Session, task_id: int, assigned_to_id: int | None) -> Task:
    task = get_task_or_404(db, task_id)

    if assigned_to_id is not None:
        assignee = db.query(User).filter(User.id == assigned_to_id).first()
        if not assignee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assigned user not found")

    task.assigned_to_id = assigned_to_id
    db.commit()
    db.refresh(task)
    invalidate_task_cache()
    return task


def delete_task(db: Session, task_id: int) -> None:
    task = get_task_or_404(db, task_id)
    db.delete(task)
    db.commit()
    invalidate_task_cache()


def list_tasks(
    db: Session,
    viewer: User,
    page: int = 1,
    page_size: int = 10,
    status_filter: str | None = None,
    priority_filter: str | None = None,
    assigned_to_id: int | None = None,
):
    redis_client = get_redis_client()
    cache_key = _cache_key(viewer.id, viewer.role, page, page_size, status_filter, priority_filter, assigned_to_id)

    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    except Exception:
        pass

    query = db.query(Task)
    if viewer.role == "user":
        query = query.filter((Task.created_by_id == viewer.id) | (Task.assigned_to_id == viewer.id))

    if status_filter:
        query = query.filter(Task.status == status_filter)
    if priority_filter:
        query = query.filter(Task.priority == priority_filter)
    if assigned_to_id is not None:
        query = query.filter(Task.assigned_to_id == assigned_to_id)

    total = query.count()
    tasks = query.order_by(Task.created_at.desc()).offset(get_offset(page, page_size)).limit(page_size).all()

    result = {
        "items": tasks,
        "total": total,
        "page": page,
        "page_size": page_size,
    }

    try:
        redis_client.setex(
            cache_key,
            60,
            json.dumps(
                {
                    "items": [
                        {
                            "id": task.id,
                            "title": task.title,
                            "description": task.description,
                            "status": task.status,
                            "priority": task.priority,
                            "due_date": task.due_date.isoformat() if task.due_date else None,
                            "created_by_id": task.created_by_id,
                            "assigned_to_id": task.assigned_to_id,
                            "created_at": task.created_at.isoformat() if task.created_at else None,
                            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                        }
                        for task in tasks
                    ],
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                }
            ),
        )
    except Exception:
        pass

    return result
