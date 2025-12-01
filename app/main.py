from fastapi import FastAPI
from starlette.responses import PlainTextResponse

from .database import create_db_and_tables
from .schemas import TaskCreate, StatusCreateUpdate
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


# tasks
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


@app.get("/tasks")
async def get_tasks():
    service = TaskService()
    data = service.list()
    statuses = "\n".join([f"{d.id}: {d.name}" for d in data])
    return PlainTextResponse(f"Task list: \n\n{statuses}")


# statuses
@app.get("/statuses")
async def get_statuses():
    service = StatusService()
    data = service.list()
    statuses = "\n".join([f"{d.id}: {d.name}" for d in data])
    return PlainTextResponse(f"Status list: \n\n{statuses}")


@app.post("/statuses")
async def create_status(status: StatusCreateUpdate):
    service = StatusService()
    status = service.create(status)
    if status:
        return PlainTextResponse(f"The status was created! \n\nID: {status.id}\nName: {status.name}\n")

    return PlainTextResponse(f"Something went wrong")


@app.put("/statuses/{status_id}")
async def update_status(status_id: int, status: StatusCreateUpdate):
    service = StatusService()
    status = service.update(status_id, status)
    if status:
        return PlainTextResponse(f"The status was updated! \n\nID: {status.id}\nName: {status.name}\n")

    return PlainTextResponse(f"Something went wrong")


@app.get("/statuses/{status_id}")
async def get_status(status_id: int):
    status = StatusService().retrieve(status_id)
    if status:
        return PlainTextResponse(f"Status card: \n\nID: {status_id}\nName: {status.name}")

    return PlainTextResponse(f"The status not found :(")


@app.delete("/statuses/{status_id}")
async def delete_status(status_id: int):
    service = StatusService()
    status = service.retrieve(status_id)
    if status:
        name = status.name
        service.delete(status_id)
        return PlainTextResponse(f'Status "{name}" was successfully deleted.\n')

    return PlainTextResponse(f"The status not found :(")
