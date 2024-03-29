from typing import Generator

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, text

from app.main import get_application
from app.models import Example
from database.connection import engine


@pytest.fixture(scope='session')
def db_engine() -> Generator[Session, None, None]:
    SQLModel.metadata.create_all(engine)

    yield engine

    SQLModel.metadata.drop_all(engine)

    with engine.connect() as conn:
        conn.execute(text('DROP TABLE IF EXISTS alembic_version;'))
        conn.commit()


@pytest.fixture(scope='function')
def db(db_engine: Engine) -> Generator[Session, None, None]:
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
        session.execute(text(f'TRUNCATE {table.name} CASCADE;'))
        session.commit()

    session.close()


@pytest.fixture(scope='session')
def app() -> FastAPI:
    return get_application()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def example_orm(app: FastAPI, db: Session) -> Example:
    example = Example(name='test', age=18, nick_name='my_nick')
    db.add(example)
    db.commit()
    db.refresh(example)
    return example
