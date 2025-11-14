from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from .settings import settings


engine = create_engine(settings.sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)
