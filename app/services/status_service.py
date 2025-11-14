from sqlalchemy import select

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Task
from app.models import Status
from app.repos import StatusRepo
from app.schemas import TaskCreate, StatusCreate
from app.repos.task_repo import TaskRepo


class StatusService:
    def __init__(self):
        self.repo = StatusRepo()

    def create(self, init: StatusCreate):
        new_status = self.repo.create_status(init)
        return new_status.id

    def retrieve(self, status_id: int):
        with Session() as session:
            statement = select(Status).where(Status.id == status_id)
            db_object = session.scalars(statement).one()

        return db_object

    def list(self):
        with SessionLocal() as session:
            statement = select(Status)
            db_objects = session.scalars(statement).all()
        return db_objects

    def update(self):
        pass

    def delete(self):
        pass

