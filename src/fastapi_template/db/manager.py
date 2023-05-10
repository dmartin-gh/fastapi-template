from contextlib import asynccontextmanager
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import AsyncIterator


class DatabaseManager:
    """Context class for managing the database engine and sessions."""

    def __init__(self, uri: PostgresDsn):
        self.uri = uri

        # create an asynchronous sqlalchemy engine
        # https://github.com/tiangolo/fastapi/issues/4876#issuecomment-1122322251
        self.engine = create_async_engine(uri, pool_pre_ping=True)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    async def __aenter__(self):
        # create a test connection to the database
        async with self.engine.begin():
            pass  # connection was successsful

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.engine.dispose()

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            yield session
