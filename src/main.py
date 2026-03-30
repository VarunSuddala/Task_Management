from fastapi import FastAPI
from core.db import engine, Base
from routers.project_router import project_router
from routers.user_router import user_router

# Import all models so Base knows about them
from models.users_model import User
from models.project_model import Project
from models.issue_model import Issue

app = FastAPI(title="Jira Lite")
app.include_router(project_router)
app.include_router(user_router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")

@app.get("/")
def root():
    return {"message": "Jira Lite API is running!"}

