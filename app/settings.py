from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432
    SQL_ECHO: bool = False

    model_config = SettingsConfigDict(
        env_file="service.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        pwd = quote_plus(self.POSTGRES_PASSWORD)
        return (f"postgresql://{self.POSTGRES_USER}:{pwd}@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}")


settings = Settings()
