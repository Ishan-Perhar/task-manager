from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from typing import List
from uuid import UUID


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post(
    "/",
    response_model=TaskResponse
)

def create_task(
        task: TaskCreate,
        db: Session = Depends(get_db)
):
    db_task = Task(
        title=task.title,
        description=task.description
    )

    db.add(db_task)

    db.commit()

    db.refresh(db_task)

    return db_task


@router.get(
    "/",
    response_model=List[TaskResponse]
)
def get_tasks(
        db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    return tasks 

@router.get(
    "/{task_id}",
    response_model=TaskResponse
)

def get_task(
        task_id: UUID,
        db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .filter((Task.id == task_id))
        .first()

    )
    if task is None:
        raise HTTPException(
            status_code=404,
            detail = "Task not found"
        )

    return task

@router.patch(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task(
        task_id: UUID,
        task_update: TaskUpdate,
        db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    update_data = task_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)  
def delete_task(
            task_id: UUID, 
            db: Session = Depends(get_db)
):
    task = (
        db.query(Task).filter(Task.id == task_id).first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)

    db.commit()


