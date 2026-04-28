from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.project_model import Project
from src.models.users_model import User


def create_project_service(project, db: Session):
    owner = db.query(User).filter(User.id == project.owner_id).first()
    if not owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner user not found")

    db_project = Project(
        key=project.key,
        name=project.name,
        description=project.description,
        owner_id=project.owner_id,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project