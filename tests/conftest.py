from urllib.parse import quote_plus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker

from app.database import get_db
from app.main import app
from app.models import Base, Status
from app.settings import settings


fixture_used = False

TEST_DATABASE_URL = (f"postgresql://{settings.POSTGRES_USER}:{quote_plus(settings.POSTGRES_PASSWORD)}"
                     f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}_test")




test_engine = create_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


@pytest.fixture(scope="function") # Фикстура, которая будет создавать и удалять БД для каждого теста
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    yield session # Предоставляем сессию
    session.close()
    transaction.rollback() # Откатываем транзакцию
    connection.close()

@pytest.fixture(scope="module") # Фикстура для клиента
def client():
    # Переопределяем зависимость для тестов
    # FastAPI использует `Depends(get_db)` по умолчанию
    # Здесь мы перенаправляем на тестовую сессию
    app.dependency_overrides[get_db] = lambda: db_session() # Предполагается, что get_db - ваша обычная функция получения сессии
    return TestClient(app)



class TestDatabase:
    def __init__(self, session: Session):
        self.session = session

    def populate_test_database(self):
        status_1 = Status(
            name="Status 1",
        )
        status_2 = Status(
            name="Status 2",
        )
        status_3 = Status(
            name="Status 3",
        )

        self.session.add_all([status_1, status_2, status_3])
        self.session.commit()


# def override_get_db():
#     test_engine = create_engine(TEST_DATABASE_URL)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# @pytest.fixture(scope="session", autouse=True)
# def create_and_delete_database():
#     app.dependency_overrides[get_db] = override_get_db
#     global fixture_used
#     if fixture_used:
#         yield
#         return
#     if database_exists(TEST_DATABASE_URL):
#         drop_database(TEST_DATABASE_URL)
#     create_database(TEST_DATABASE_URL)
#     test_engine = create_engine(TEST_DATABASE_URL)
#     Base.metadata.create_all(bind=test_engine)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
#     TestDatabase(session=SessionLocal()).populate_test_database()
#     fixture_used = True
#     yield
#     close_all_sessions()
#     # todo
#     # drop_database(TEST_DATABASE_URL)
#

@pytest.fixture(scope='session', autouse=True)
def create_and_use_database():
    engine = create_engine(TEST_DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    TestDatabase(session=SessionLocal()).populate_test_database()


@pytest.fixture(scope="session", autouse=True)
def client():
    return TestClient(app)
