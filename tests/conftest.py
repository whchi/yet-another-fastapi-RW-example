import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from database.connection import engine


@pytest.fixture(autouse=True)
def refresh_database(db: Session) -> None:
    SQLModel.metadata.create_all(engine)

    yield

    db.close()
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope='session')
def db():
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=Session,
        expire_on_commit=True,
    )()
