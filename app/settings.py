from pydantic_settings import BaseSettings
from pydantic import computed_field
from urllib.parse import quote_plus


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    @computed_field(return_type=str)
    @property
    def sqlalchemy_database_url(self) -> str:
        pwd = quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql://{self.POSTGRES_USER}:{pwd}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = {
        "env_file": "service.env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
