import asyncio

from fastapi import FastAPI
from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.models import Example
from database.async_connection import engine as async_engine


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
async def client(app) -> AsyncClient:
    async with AsyncClient(app=app) as client:
        yield client


@pytest.fixture
async def example_orm(app: FastAPI, db: AsyncSession) -> Example:
    example = Example(name='test', age=18, nick_name='my_nick')
    db.add(example)
    await db.commit()
    await db.refresh(example)
    return example


@pytest.fixture(scope='session')
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

        yield async_engine

        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope='function')
async def async_db(async_db_engine):
    async_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    session = async_session()

    async with session.begin() as s:
        yield s
        await s.rollback()
        for table in reversed(SQLModel.metadata.sorted_tables):
            await s.execute(f'TRUNCATE {table.name} CASCADE;')
            await s.commit()

        await s.close()


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
