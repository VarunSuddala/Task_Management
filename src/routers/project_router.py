from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.project_schema import ProjectCreate
from src.services.project_service import create_project_service


project_router = APIRouter(prefix="/project", tags=["project"])


@project_router.get("/list")
def list_projects():
    return {"message": "Project endpoints are kept for compatibility."}


@project_router.post("/create")
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    create_project_service(project_data, db)
    return {"message": "Project created successfully"}
