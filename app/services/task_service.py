from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate
from app.repos.task_repo import TaskRepo


class TaskService:
    def __init__(self, session: Session):
        self.repo = TaskRepo(session)

    def create(self, init: TaskCreate) -> Task:
        return self.repo.create(init)

    def retrieve(self, task_id: int) -> Task | None:
        return self.repo.retrieve(task_id)

    def list(self):
        return self.repo.list()

    def update(self):
        pass

    def delete(self, task_id: int) -> bool:
        task = self.repo.retrieve(task_id)
        if not task:
            return False

        self.repo.delete(task)
        return True
