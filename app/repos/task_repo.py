from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate


class TaskRepo:
    def __init__(self, session: Session):
        self.session = session

    def create(self, init: TaskCreate) -> Task:
        task = Task(**init.model_dump())
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def retrieve(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def list(self):
        return self.session.scalars(select(Task)).all()

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()
