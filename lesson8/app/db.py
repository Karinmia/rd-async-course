"""This module contains methods for interaction with database"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.config import DB_URI, DB_ECHO


def get_engine() -> AsyncEngine:
    return create_async_engine(DB_URI, echo=DB_ECHO)


@asynccontextmanager
async def make_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(engine)
    async with session_factory() as session:
        yield session
