from httpx import AsyncClient
import pytest
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from starlette import status

from app.models import Example

pytestmark = pytest.mark.asyncio


async def test_add_example(client: AsyncClient, async_db: AsyncSession) -> None:
    payload = {'name': 'my name', 'age': 18, 'nick_name': 'my nick name'}

    response = await client.post('/api/async-examples', json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == status.HTTP_201_CREATED
    assert (await async_db.execute(func.count(select(Example.id)))).scalar() == 1
    row = (await async_db.execute(select(Example).filter_by(name=payload['name'])
                                 )).scalar_one()
    assert row.name == payload['name']


async def test_get_example(client: AsyncClient, async_db: AsyncSession,
                           async_example_orm: Example) -> None:
    response = await client.get(f'/api/async-examples/{async_example_orm.id}')

    assert response.status_code == status.HTTP_200_OK
    assert (await async_db.execute(select(Example).filter_by(id=async_example_orm.id)
                                  )).scalar_one().id == async_example_orm.id


async def test_get_examples(client: AsyncClient, async_db: AsyncSession,
                            async_example_orm: Example) -> None:
    response = await client.get('/api/async-examples')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == 1


async def test_delete_example(client: AsyncClient, async_db: AsyncSession,
                              async_example_orm: Example) -> None:
    response = await client.delete(f'/api/async-examples/{async_example_orm.id}')

    assert response.status_code == status.HTTP_200_OK
    assert (await async_db.execute(select(Example).filter_by(id=async_example_orm.id)
                                  )).scalar() is None


async def test_update_example(client: AsyncClient, async_db: AsyncSession,
                              async_example_orm: Example) -> None:
    payload = {'name': 'updated_name', 'age': 20}

    response = await client.put(f'/api/async-examples/{async_example_orm.id}',
                                json=payload)
    assert response.status_code == status.HTTP_200_OK
    await async_db.refresh(async_example_orm)
    assert (await
            async_db.execute(select(Example).filter_by(id=async_example_orm.id)
                            )).scalar_one().name == response.json()['data']['name']


async def test_get_paginate_example(client: AsyncClient,
                                    async_example_orm: Example) -> None:
    response = await client.get('/api/async-examples/paginate-examples')

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert len(body['data']['items']) == 1
    assert body['data']['total'] == 1
    assert body['data']['current_page'] == 1
    assert not body['data']['next_page']
