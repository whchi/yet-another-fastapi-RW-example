import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from database.connection import engine


@pytest.fixture(autouse=True, scope='session')
def db_engine():
    SQLModel.metadata.create_all(engine)

    yield engine

    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def db(db_engine):
    session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine,
        class_=Session,
        expire_on_commit=False,
    )()

    yield session

    session.rollback()
    for table in reversed(SQLModel.metadata.sorted_tables):
        session.execute(f'TRUNCATE {table.name} CASCADE;')
        session.commit()

    session.close()


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
