from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_template.db.models import Example


async def test_get_example_data(cli: TestClient, session: AsyncSession):
    session.add(Example(id=1, col1="test1", col2=1))
    session.add(Example(id=2, col1="test2", col2=2))
    await session.commit()

    resp = cli.get("/api/fastapi-template/example")

    assert resp.status_code == 200
    assert resp.json() == [
        {"id": 1, "col1": "test1", "col2": 1},
        {"id": 2, "col1": "test2", "col2": 2},
    ]


async def test_get_example_data_empty(cli: TestClient):
    resp = cli.get("/api/fastapi-template/example")

    assert resp.status_code == 200
    assert resp.json() == []
