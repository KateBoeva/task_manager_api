from select import select

from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate
from app.repos.task_repo import TaskRepo


class TaskService:
    def __init__(self):
        self.repo = TaskRepo()
    def create(self, init: TaskCreate):
        new_task = self.repo.create_task(init)
        return new_task.id

    def retrieve(self, task_id: int):
        with Session() as session:
            statement = select(Task).where(Task.id == task_id)
            db_object = session.scalars(statement).one()

        return db_object

    def update(self):
        pass

    def delete(self):
        pass

