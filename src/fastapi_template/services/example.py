from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_template.db.dependency import SessionDependency
from fastapi_template.db.models import Example


class ExampleService:
    def __init__(self, session: AsyncSession = SessionDependency):
        self.session = session

    async def get_example_data(self) -> list[Example]:
        result = await self.session.execute(select(Example))
        return list(result.scalars().all())
