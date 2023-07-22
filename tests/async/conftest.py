import asyncio

from fastapi import FastAPI
from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.core import get_app_settings
from app.models import Example
from database.async_connection import engine as async_engine


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    return AsyncClient(app=app, base_url=get_app_settings().APP_URL)


@pytest.fixture
async def async_example_orm(async_db: AsyncSession) -> Example:
    example = Example(name='test', age=18, nick_name='my_nick')
    async_db.add(example)
    await async_db.commit()
    await async_db.refresh(example)
    return example


@pytest.fixture(scope='session')
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope='function')
async def async_db(async_db_engine):
    async_session = sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )

    async with async_session() as session:
        await session.begin()

        yield session

        await session.rollback()

        for table in reversed(SQLModel.metadata.sorted_tables):
            await session.execute(f'TRUNCATE {table.name} CASCADE;')
            await session.commit()

        # await session.close()


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
