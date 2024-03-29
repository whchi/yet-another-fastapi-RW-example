from sqlalchemy import func
from sqlmodel import select, Session
from starlette import status
from starlette.testclient import TestClient

from app.models import Example


def test_add_example(client: TestClient, db: Session) -> None:
    payload = {'name': 'my name', 'age': 18, 'nick_name': 'my nick name'}

    response = client.post('/api/examples', json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == status.HTTP_201_CREATED

    db_row = db.execute(select(Example)).scalar()
    db_count = db.execute(func.count(Example.id)).scalar()

    assert db_count == 1
    assert db_row is not None
    assert db_row.name == payload['name']


def test_get_example(client: TestClient, db: Session, example_orm: Example) -> None:
    response = client.get(f'/api/examples/{example_orm.id}')

    assert response.status_code == status.HTTP_200_OK
    assert db.execute(
        select(Example).filter_by(id=example_orm.id)).scalar().id == example_orm.id


def test_get_examples(client: TestClient, db: Session, example_orm: Example) -> None:
    response = client.get('/api/examples')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == 1


def test_delete_example(client: TestClient, db: Session, example_orm: Example) -> None:
    response = client.delete(f'/api/examples/{example_orm.id}')

    assert response.status_code == status.HTTP_200_OK
    assert db.execute(select(Example).filter_by(id=example_orm.id)).scalar() is None


def test_update_example(client: TestClient, db: Session, example_orm: Example) -> None:
    response = client.put(f'/api/examples/{example_orm.id}',
                          json={
                              'name': 'updated_name',
                              'nick_name': 'nniicckknnaammee',
                              'age': 20
                          })

    assert response.status_code == status.HTTP_200_OK
    db.refresh(example_orm)
    updated_example = db.execute(
        select(Example).filter_by(id=example_orm.id)).scalar_one()
    assert updated_example.name == 'updated_name'


def test_get_paginate_example(client: TestClient, example_orm: Example) -> None:
    response = client.get('/api/examples/paginate-examples')
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert len(body['data']['items']) == 1
    assert body['data']['total'] == 1
    assert body['data']['current_page'] == 1
    assert not body['data']['next_page']
