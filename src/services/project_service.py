from sqlalchemy.orm import Session
from models.project_model import Project
from schemas.project_schema import ProjectCreate
from fastapi import HTTPException, status,Depends
from models.users_model import User
def create_project_service(project,db:Session):
    db_project = Project(
        key=project.key,
        name=project.name,
        description=project.description,
        owner_id=project.owner_id
    )
    owner = db.query(User).filter(User.id == project.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner user not found")
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project