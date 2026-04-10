from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
import models, schemas, crud
from database import engine, SessionLocal
import user_schemas
import user_models 

# Create all DB tables on startup
models.Base.metadata.create_all(bind=engine) 
user_models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency gives each request its own DB session, closes it after
def get_db():
    db = SessionLocal()
    try:
        yield db #Returns the session to the endpoint.
    finally:
        db.close()

@app.post("/tasks/", response_model=schemas.TaskResponse) # create  task endpoint 
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@app.get("/tasks/", response_model=List[schemas.TaskResponse])
def get_tasks(
    completed: Optional[bool] = None,
    search: Optional[str] = None,
    sort: Optional[str] = "asc",
    db: Session = Depends(get_db)
):
    return crud.get_tasks(db, completed, search, sort)

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task_full(task_id: int, task_data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task_partial(task_id: int, task_data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
