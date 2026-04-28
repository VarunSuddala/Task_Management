from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.db.base import Base
from src.db.session import engine
from src.models.task_model import Task
from src.models.users_model import User
from src.routers.auth_router import auth_router
from src.routers.task_router import task_router
from src.routers.user_router import user_router
from src.utils.exceptions import (
    generic_exception_handler,
    sqlalchemy_exception_handler,
    validation_exception_handler,
)


app = FastAPI(title="Task Management API", version="1.0.0")

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(user_router)


@app.on_event("startup")
def startup() -> None:
    # Alembic is the source of truth for schema changes; startup only verifies imports.
    _ = (Base, engine, User, Task)


@app.get("/")
def root():
    return {"message": "Task Management API is running!"}


