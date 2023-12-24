import asyncio
from typing import AsyncGenerator, Generator

from fastapi import FastAPI
from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncConnection,
    AsyncSession,
)
from sqlmodel import SQLModel, text

from app.core import get_app_settings
from database.async_connection import engine as async_engine


@pytest.fixture
async def async_client(app: FastAPI) -> AsyncClient:
    return AsyncClient(app=app, base_url=get_app_settings().APP_URL)


@pytest.fixture(scope='session')
async def async_conn() -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    db_conn = await async_engine.connect()

    yield db_conn

    await db_conn.close()

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await async_engine.dispose()


@pytest.fixture(scope='function')
async def async_db(async_conn: AsyncConnection) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_conn,
        expire_on_commit=False,
        autoflush=False,
    )
    async with async_session() as session:
        await session.begin()

        yield session

        await session.rollback()


async def truncate_all_tables(session: AsyncSession) -> None:
    for table in reversed(SQLModel.metadata.sorted_tables):
        await session.execute(text(f'TRUNCATE {table.name} CASCADE;'))
        await session.commit()


@pytest.fixture(scope='session')
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
