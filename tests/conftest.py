from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from testcontainers.postgres import PostgresContainer
from typing import AsyncIterator, Iterator
import os
import pytest

from fastapi_template.app import create_app
from fastapi_template.db.models import Base
from fastapi_template.settings import Settings


def pytest_collection_modifyitems(items):
    # Mark any tests that use the 'postgres' fixture as integration tests
    for item in items:
        if "postgres" in getattr(item, "fixturenames", ()):
            item.add_marker("integration")


@pytest.fixture(scope="session", autouse=True)
def test_env(session_mocker: MockerFixture) -> Iterator[None]:
    # Ensure no test can accidentally talk to a non-test database
    env = {
        "POSTGRES_SERVER": f"localhost",
        "POSTGRES_USER": "test",
        "POSTGRES_PASSWORD": "test",
        "POSTGRES_DB": "test",
    }
    session_mocker.patch.dict(os.environ, env)
    yield


@pytest.fixture(scope="session")
def postgres(session_mocker: MockerFixture) -> Iterator[None]:
    container = PostgresContainer(
        image="postgres:14",
        user="test",
        dbname="test",
        password="test",
    )

    with container as postgres:
        port = postgres.get_exposed_port(postgres.port_to_expose)
        env = {
            "POSTGRES_SERVER": f"localhost:{port}",
            "POSTGRES_USER": postgres.POSTGRES_USER,
            "POSTGRES_PASSWORD": postgres.POSTGRES_PASSWORD,
            "POSTGRES_DB": postgres.POSTGRES_DB,
        }
        session_mocker.patch.dict(os.environ, env)

        # populate schema
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(bind=engine)
        engine.dispose()

        yield


@pytest.fixture()
async def engine(postgres) -> AsyncIterator[AsyncEngine]:
    settings = Settings()
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
    yield engine
    await engine.dispose()


@pytest.fixture
async def cli(engine: AsyncEngine) -> AsyncIterator[TestClient]:
    with TestClient(create_app()) as client:
        yield client

    # Truncate all tables for next test (faster than drop all => create all)
    async with engine.begin() as conn:
        tables = ", ".join(
            [f'"{table.name}"' for table in reversed(Base.metadata.sorted_tables)]
        )
        await conn.execute(text(f"TRUNCATE {tables} RESTART IDENTITY"))
        await conn.commit()


@pytest.fixture
async def session(engine: AsyncEngine):
    async with AsyncSession(engine) as session:
        yield session
