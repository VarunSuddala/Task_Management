from fastapi import FastAPI
from core.db import engine, Base

# Import all models so Base knows about them
from models.users_model import User
from models.project_model import Project
from models.issue_model import Issue

app = FastAPI(title="Jira Lite")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")

@app.get("/")
def root():
    return {"message": "Jira Lite API is running!"}
