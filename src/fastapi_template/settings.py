from pydantic import BaseSettings, PostgresDsn
import os


class Settings(BaseSettings):
    ALEMBIC_DIR: str = os.getcwd()

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            path=f"/{self.POSTGRES_DB or ''}",
        )

    class Config:
        case_sensitive = True
