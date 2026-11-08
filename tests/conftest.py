from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import select, text
from sqlalchemy.orm import sessionmaker

from app.database import engine, get_db
from app.main import app
from app.models import Priority, Status
from app.settings import settings


BASE_DIR = Path(__file__).resolve().parent.parent

# create_savepoint: commit в коде приложения не завершает внешнюю транзакцию теста
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, join_transaction_mode="create_savepoint")


@pytest.fixture(scope="session")
def alembic_config():
    config = Config(str(BASE_DIR / "alembic.ini"))
    config.set_main_option("script_location", str(BASE_DIR / "migrations"))
    return config


@pytest.fixture(scope="session", autouse=True)
def prepare_database(alembic_config):
    # Защита на случай, если настройки из pytest.ini не применились: ниже схема удаляется целиком
    if not settings.POSTGRES_DB.endswith("_test"):
        pytest.exit(f"Refusing to run tests against database '{settings.POSTGRES_DB}'", returncode=1)

    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))

    command.upgrade(alembic_config, "head")
    yield
    engine.dispose()


@pytest.fixture
def connection():
    # Всё, что сделал тест, откатывается вместе с этой транзакцией
    with engine.connect() as connection:
        transaction = connection.begin()
        yield connection
        transaction.rollback()


@pytest.fixture
def db_session(connection):
    session = TestSessionLocal(bind=connection)
    yield session
    session.close()


@pytest.fixture
def client(connection):
    # Как и в приложении, у каждого запроса своя сессия
    def override_get_db():
        session = TestSessionLocal(bind=connection)
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def task_status(db_session):
    status = Status(name="To Do")
    db_session.add(status)
    db_session.commit()
    return status


@pytest.fixture
def priority(db_session):
    return db_session.scalars(select(Priority).where(Priority.name == "Low")).one()
