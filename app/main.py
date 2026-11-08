from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TaskCreate, TaskDetail, StatusCreateUpdate, StatusDetail
from app.services import TaskService, StatusService


app = FastAPI()


# Эндпоинты синхронные (def), т.к. работа с БД синхронная:
# FastAPI выполняет их в threadpool и не блокирует event loop.

# tasks
@app.get("/tasks/{task_id}", response_model=TaskDetail)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = TaskService(db).retrieve(task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Task with id = {task_id} not found")

    return task


@app.post("/tasks", response_model=TaskDetail, status_code=status.HTTP_201_CREATED)
def create_task(init: TaskCreate, db: Session = Depends(get_db)):
    try:
        return TaskService(db).create(init)
    except (IntegrityError, DataError):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid status_id or priority_id")


@app.get("/tasks", response_model=list[TaskDetail])
def get_tasks(db: Session = Depends(get_db)):
    return TaskService(db).list()


# statuses
@app.get("/statuses", response_model=list[StatusDetail])
def get_statuses(db: Session = Depends(get_db)):
    return StatusService(db).list()


@app.post("/statuses", response_model=StatusDetail, status_code=status.HTTP_201_CREATED)
def create_status(init: StatusCreateUpdate, db: Session = Depends(get_db)):
    try:
        return StatusService(db).create(init)
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Status with name = {init.name} already exists")


@app.put("/statuses/{status_id}", response_model=StatusDetail)
def update_status(status_id: int, init: StatusCreateUpdate, db: Session = Depends(get_db)):
    try:
        updated = StatusService(db).update(status_id, init)
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Status with name = {init.name} already exists")

    if updated is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Status with id = {status_id} not found")

    return updated


@app.get("/statuses/{status_id}", response_model=StatusDetail)
def get_status(status_id: int, db: Session = Depends(get_db)):
    found = StatusService(db).retrieve(status_id)
    if found is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Status with id = {status_id} not found")

    return found


@app.delete("/statuses/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_status(status_id: int, db: Session = Depends(get_db)):
    try:
        deleted = StatusService(db).delete(status_id)
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Status is used by tasks")

    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Status with id = {status_id} not found")
