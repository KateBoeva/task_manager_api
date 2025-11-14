from pydantic_settings import BaseSettings
from urllib.parse import quote_plus


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432
    sqlalchemy_database_url: str

    def __init__(self):
        super().__init__()
        pwd = quote_plus(self.POSTGRES_PASSWORD)
        self.sqlalchemy_database_url = (f"postgresql://{self.POSTGRES_USER}:{pwd}@{self.POSTGRES_HOST}:"
                                        f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    model_config = {
        "env_file": "service.env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
