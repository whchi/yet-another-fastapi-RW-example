from fastapi import FastAPI
import pytest
from sqlmodel import Session
from starlette import status
from starlette.testclient import TestClient

from app.api.contexts.example.domain.schema import AddExampleRequest
from app.api.contexts.example.gateway import ExampleRepository
from app.models import Example

pytestmark = pytest.mark.asyncio


@pytest.fixture
def example_orm(app: FastAPI, db: Session) -> Example:
    to_save = AddExampleRequest(name='test', age=18, nick_name='my_nick')
    repo = ExampleRepository(db)
    repo.add(to_save)
    db.commit()
    return db.query(Example).order_by(Example.id.desc()).limit(1).one()


async def test_add_example(client: TestClient, db: Session) -> None:
    payload = {'name': 'my name', 'age': 18, 'nick_name': 'my nick name'}
    response = client.post('/api/examples', json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == status.HTTP_201_CREATED

    db_row = db.query(Example).first()
    db_count = db.query(Example).count()

    assert db_count == 1
    assert db_row is not None
    assert db_row.name == payload['name']


async def test_get_example(client: TestClient, db: Session,
                           example_orm: Example) -> None:
    response = client.get(f'/api/examples/{example_orm.id}')
    assert response.status_code == status.HTTP_200_OK
    assert db.query(Example).filter_by(id=example_orm.id).first().id == example_orm.id


async def test_get_examples(client: TestClient, db: Session,
                            example_orm: Example) -> None:
    response = client.get(f'/api/examples')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == 1


async def test_delete_example(client: TestClient, db: Session,
                              example_orm: Example) -> None:
    response = client.delete(f'/api/examples/{example_orm.id}')
    assert response.status_code == status.HTTP_200_OK
    assert db.query(Example).filter_by(id=example_orm.id).first() is None


async def test_update_example(client: TestClient, db: Session,
                              example_orm: Example) -> None:
    payload = {'name': 'updated_name', 'age': 20}
    response = client.put(f'/api/examples/{example_orm.id}', json=payload)
    assert response.status_code == status.HTTP_200_OK
    db.commit()
    assert db.query(Example).filter_by(
        id=example_orm.id).first().name == response.json()['data']['name']
