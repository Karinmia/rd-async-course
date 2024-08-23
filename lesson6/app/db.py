"""This module contains methods for interaction with database"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncio

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.config import DB_URI, DB_ECHO

def get_engine() -> AsyncEngine:
    return create_async_engine(DB_URI, echo=DB_ECHO)


# def make_session_class(engine: AsyncEngine) -> type[AsyncSession]:
#     return async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def make_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(engine)
    async with session_factory() as session:
        yield session
