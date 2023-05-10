from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncIterator

from fastapi_template.db.manager import DatabaseManager


async def get_async_session(request: Request) -> AsyncIterator[AsyncSession]:
    manager: DatabaseManager = request.app.state.db

    async with manager.session() as db:
        yield db


SessionDependency = Depends(get_async_session)
