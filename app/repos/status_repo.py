from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Status
from app.schemas import StatusCreateUpdate


class StatusRepo:
    def __init__(self, session: Session):
        self.session = session

    def create(self, init: StatusCreateUpdate) -> Status:
        status = Status(name=init.name)
        self.session.add(status)
        self.session.commit()
        self.session.refresh(status)
        return status

    def update(self, status: Status, init: StatusCreateUpdate) -> Status:
        status.name = init.name
        self.session.commit()
        self.session.refresh(status)
        return status

    def retrieve(self, status_id: int) -> Status | None:
        return self.session.get(Status, status_id)

    def list(self):
        return self.session.scalars(select(Status)).all()

    def delete(self, status: Status) -> None:
        self.session.delete(status)
        self.session.commit()
