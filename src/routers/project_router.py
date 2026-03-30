from fastapi import APIRouter,Depends
from services.project_service import create_project_service
from schemas.project_schema import ProjectCreate
from sqlalchemy.orm import Session
from core.db import get_db
project_router = APIRouter(prefix="/project", tags=["project"])


@project_router.get("/list")
def list_projects():
    return {"message": "List of projects"}


@project_router.post("/create")
def create_project(project_data:ProjectCreate,db:Session=Depends(get_db)):
    create_project_service(project_data,db)
    return {"message": "Project created successfully"}
