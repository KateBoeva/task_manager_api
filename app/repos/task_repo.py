from sqlalchemy.orm import sessionmaker

from app.models import Task
from app.schemas import TaskCreate
from app.database import engine

Session = sessionmaker(engine)


class TaskRepo:
    def create_task(self, init: TaskCreate) -> None:
        task = Task(
            title=init.title,
            # description: str
            # priority: int,
        )
        with Session() as session:
            try:
                session.add(task)
            except:
                session.rollback()
                raise
            else:
                session.commit()
