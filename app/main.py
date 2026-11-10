from fastapi import FastAPI

from app.routers import task_router, status_router


app = FastAPI()


# Эндпоинты синхронные, т.к. работа с БД синхронная
# FastAPI выполняет их в threadpool и не блокирует event loop
app.include_router(task_router)
app.include_router(status_router)
