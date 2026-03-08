from fastapi import FastAPI,HTTPException,Query
from  src.service import get_tasks,get_task_by_id,create_task,update_task,delete_task

app=FastAPI()

@app.get("/")
def read_root():
    return {"message":"Welcome to the Task Management API"}

@app.get("/tasks")
def read_tasks():
    return get_tasks()

@app.get("/tasks/{task_id}")
def read_task(task_id:int):
    return get_task_by_id(task_id)

@app.post("/tasks")
def create_new_task(task:dict):
    return create_task(task)

@app.put("/tasks/{task_id}")
def update_existing_task(task_id:int,task:dict):
    return update_task(task_id,task)

@app.delete("/tasks/{task_id}")
def delete_existing_task(task_id:int):
    return delete_task(task_id)

