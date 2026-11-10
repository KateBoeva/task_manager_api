from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TaskCreate, TaskDetail
from app.services import TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{task_id}", response_model=TaskDetail)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = TaskService(db).retrieve(task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Task with id = {task_id} not found")

    return task


@router.post("", response_model=TaskDetail, status_code=status.HTTP_201_CREATED)
def create_task(init: TaskCreate, db: Session = Depends(get_db)):
    try:
        return TaskService(db).create(init)
    except (IntegrityError, DataError):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid status_id or priority_id")


@router.get("", response_model=list[TaskDetail])
def get_tasks(db: Session = Depends(get_db)):
    return TaskService(db).list()


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = TaskService(db).delete(task_id)

    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Task with id = {task_id} not found")
