from sqlalchemy.orm import sessionmaker

from app.models import Status
from app.schemas import StatusCreate
from app.database import engine

Session = sessionmaker(engine)


class StatusRepo:
    def create_status(self, init: StatusCreate) -> None:
        status = Status(name=init.name)
        with Session() as session:
            try:
                session.add(status)
            except:
                session.rollback()
                raise
            else:
                session.commit()
