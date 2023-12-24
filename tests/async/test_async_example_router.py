from httpx import AsyncClient
import pytest
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from starlette import status

from app.models import Example

from .conftest import truncate_all_tables

pytestmark = pytest.mark.asyncio


async def async_example_orm(db_session: AsyncSession) -> Example:
    example = Example(name='test', age=18, nick_name='my_nick')
    db_session.add(example)
    await db_session.commit()

    return example


async def test_add_example(async_client: AsyncClient, async_db: AsyncSession) -> None:
    payload = {'name': 'my name', 'age': 18, 'nick_name': 'my nick name'}
    response = await async_client.post('/api/async-examples', json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == status.HTTP_201_CREATED
    assert (await async_db.execute(func.count(select(Example.id).scalar_subquery())
                                  )).scalar() == 1
    row = (await async_db.execute(select(Example).filter_by(name=payload['name'])
                                 )).scalar_one()
    await async_db.commit()
    await truncate_all_tables(async_db)
    assert row.name == payload['name']


async def test_get_example(async_client: AsyncClient, async_db: AsyncSession) -> None:
    example_orm = await async_example_orm(async_db)
    response = await async_client.get(f'/api/async-examples/{example_orm.id}')
    assert response.status_code == status.HTTP_200_OK
    assert (await async_db.execute(select(Example).filter_by(id=example_orm.id)
                                  )).scalar_one().id == example_orm.id
    await async_db.commit()
    await truncate_all_tables(async_db)


async def test_get_examples(async_client: AsyncClient, async_db: AsyncSession) -> None:
    await async_example_orm(async_db)
    response = await async_client.get('/api/async-examples')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == 1
    await truncate_all_tables(async_db)


async def test_delete_example(async_client: AsyncClient,
                              async_db: AsyncSession) -> None:
    example_orm = await async_example_orm(async_db)
    response = await async_client.delete(f'/api/async-examples/{example_orm.id}')

    assert response.status_code == status.HTTP_200_OK
    assert (await async_db.execute(select(Example).filter_by(id=example_orm.id)
                                  )).scalar() is None
    await async_db.commit()
    await truncate_all_tables(async_db)


async def test_update_example(async_client: AsyncClient,
                              async_db: AsyncSession) -> None:
    example_orm = await async_example_orm(async_db)
    payload = {'name': 'updated_name', 'age': 20}

    response = await async_client.put(f'/api/async-examples/{example_orm.id}',
                                      json=payload)
    await async_db.reset()

    assert response.status_code == status.HTTP_200_OK
    assert (await
            async_db.execute(select(Example).filter_by(id=example_orm.id)
                            )).scalar_one().name == response.json()['data']['name']
    await truncate_all_tables(async_db)


async def test_get_paginate_example(async_client: AsyncClient,
                                    async_db: AsyncSession) -> None:
    await async_example_orm(async_db)

    response = await async_client.get('/api/async-examples/paginate-examples')
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert len(body['data']['items']) == 1
    assert body['data']['total'] == 1
    assert body['data']['current_page'] == 1
    assert not body['data']['next_page']
