from sqlalchemy.orm import Session #You need it to query, insert, update, or delete data in your database.
from sqlalchemy import asc, desc #Used for sorting tasks based on created_at.
from typing import Optional
import models, schemas

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)  # reload to get the generated id, created_at
    return db_task


def get_tasks(db: Session, completed: Optional[bool], search: Optional[str], sort: Optional[str]):
    query = db.query(models.Task)

    if completed is not None:
        query = query.filter(models.Task.is_completed == completed)
    if search:
        query = query.filter(models.Task.title.contains(search))
    if sort == "desc":
        query = query.order_by(desc(models.Task.created_at))
    else:
        query = query.order_by(asc(models.Task.created_at))

    return query.all()



def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate):
    task = get_task(db, task_id)
    if not task:
        return None
    update_fields = task_data.model_dump(exclude_unset=True)  # only changed fields
    for key, value in update_fields.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    if not task:
        return None
    db.delete(task)
    db.commit()
    return task