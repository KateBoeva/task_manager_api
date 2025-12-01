from app.repos import StatusRepo
from app.schemas import StatusCreateUpdate


class StatusService:
    def __init__(self):
        self.repo = StatusRepo()

    def create(self, init: StatusCreateUpdate):
        new_status = self.repo.create(init)
        return new_status

    def update(self, status_id: int, init: StatusCreateUpdate):
        updated_status = self.repo.update(status_id, init)
        return updated_status

    def retrieve(self, status_id: int):
        status = self.repo.retrieve(status_id)
        return status

    def list(self):
        statuses = self.repo.list()
        return statuses

    def delete(self, status_id: int):
        self.repo.delete(status_id)
