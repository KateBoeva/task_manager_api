from fastapi import FastAPI
from starlette.responses import PlainTextResponse

from .database import create_db_and_tables, Base
from .models import Status, Priority
from .schemas import TaskCreate, StatusCreate
from app.services.task_service import TaskService
from .services import StatusService

app = FastAPI()

create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = TaskService().retrieve(task_id)
    if task:
        return {"message": f"Found task with id = task_id"}

    return {"message": f"Not found task with id = task_id"}


@app.post("/tasks")
async def create_task(task: TaskCreate):
    service = TaskService()
    task_id = service.create(task)
    if task_id:
        return {"message": f"Added task with id = {task_id}"}

    return {"message": f"Something went wrong"}


@app.get("/statuses")
async def get_statuses():
    service = StatusService()

    data = service.list()

    statuses = "\n".join([f"{d.id}: {d.name}" for d in data])

    return PlainTextResponse(f"Status list: \n\n{statuses}")


@app.post("/statuses")
async def create_status(status: StatusCreate):
    service = StatusService()
    task_id = service.create(status)
    if task_id:
        return {"message": f"Added task with id = {task_id}"}

    return {"message": f"Something went wrong"}
