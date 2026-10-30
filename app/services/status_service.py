from sqlalchemy.orm import Session

from app.models import Status
from app.repos import StatusRepo
from app.schemas import StatusCreateUpdate


class StatusService:
    def __init__(self, session: Session):
        self.repo = StatusRepo(session)

    def create(self, init: StatusCreateUpdate) -> Status:
        return self.repo.create(init)

    def update(self, status_id: int, init: StatusCreateUpdate) -> Status | None:
        status = self.repo.retrieve(status_id)
        if status is None:
            return None

        return self.repo.update(status, init)

    def retrieve(self, status_id: int) -> Status | None:
        return self.repo.retrieve(status_id)

    def list(self):
        return self.repo.list()

    def delete(self, status_id: int) -> bool:
        status = self.repo.retrieve(status_id)
        if status is None:
            return False

        self.repo.delete(status)
        return True
