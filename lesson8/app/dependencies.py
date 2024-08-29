from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import make_session, get_engine


async def get_session() -> AsyncIterator[AsyncSession]:
    async with make_session(get_engine()) as session:
        yield session
