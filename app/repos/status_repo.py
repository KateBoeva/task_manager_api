from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from app.models import Status
from app.schemas import StatusCreateUpdate
from app.database import engine, SessionLocal

Session = sessionmaker(engine)


class StatusRepo:
    def create(self, init: StatusCreateUpdate) -> Status:
        status = Status(name=init.name)
        with Session() as session:
            try:
                session.add(status)
            except:
                session.rollback()
                raise
            else:
                session.commit()
                session.refresh(status)

        return status

    def update(self, status_id: int, init: StatusCreateUpdate) -> Status:
        with Session() as session:
            statement = select(Status).where(status_id == Status.id)
            status = session.scalars(statement).one()
            try:
                status.name = init.name
                session.add(status)
            except:
                session.rollback()
                raise
            else:
                session.commit()
                session.refresh(status)

        return status

    def retrieve(self, status_id: int):
        with SessionLocal() as session:
            try:
                statement = select(Status).where(status_id == Status.id)
                db_object = session.scalars(statement).one()
            except NoResultFound:
                return None

        return db_object

    def list(self):
        with SessionLocal() as session:
            statement = select(Status)
            db_objects = session.scalars(statement).all()

        return db_objects

    def delete(self, status_id: int) -> None:
        with SessionLocal() as session:
            statement = select(Status).where(status_id == Status.id)
            db_object = session.scalars(statement).one()
            print(db_object)
            session.delete(db_object)
            session.commit()
