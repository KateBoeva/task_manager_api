from select import select

from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreateUpdate
from app.database import Database as db


class TaskCrud:
    def create(self, session, init: TaskCreateUpdate):
        pass

    def retrieve(self, task_id: int):
        with Session() as session:
            statement = select(Task).where(Task.id == task_id)
            db_object = session.scalars(statement).one()

        return db_object

    def update(self):
        pass

    def delete(self):
        pass

