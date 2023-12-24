from typing import Any, Dict, List

from fastapi.param_functions import Depends
from sqlalchemy import desc
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, insert
from sqlmodel.sql.expression import select

from app.api.contexts.async_example.domain import (
    AddExampleRequest,
    UpdateExampleRequest,
)
from app.api.paginator import ModelPaginator
from app.exceptions.schema import ModelNotFoundException
from app.models import Example
from database.async_connection import get_async_session


class ExampleRepository:

    def __init__(self, db_session: AsyncSession = Depends(get_async_session)):
        self.orm = Example
        self.db_session = db_session

    async def index(self) -> List[Row]:
        result = await self.db_session.execute(select(self.orm))
        return result.scalars().all()

    async def paginate_index(self, page: int, per_page: int) -> Dict[str, Any]:
        return await ModelPaginator.async_paginate(
            session=self.db_session,
            model=self.orm,
            page=page,
            per_page=per_page,
            order_by=[desc(self.orm.created_at),
                      desc(self.orm.id)])

    async def show(self, id: int) -> Example:
        result = await self.db_session.execute(select(self.orm).filter_by(id=id))
        row = result.scalar()

        if not row:
            raise ModelNotFoundException(
                detail=f'{self.orm.__tablename__}.id={id} not found')

        return row

    async def update(self, id: int, payload: UpdateExampleRequest) -> Example:
        row = await self.show(id)

        row.nick_name = payload.nick_name
        row.name = payload.name
        if payload.age:
            row.age = payload.age

        self.db_session.add(row)
        await self.db_session.commit()

        return row

    async def delete(self, id: int) -> None:
        await self.show(id)

        stmt = (delete(self.orm).filter_by(id=id))
        await self.db_session.execute(stmt)
        await self.db_session.commit()

    async def add(self, payload: AddExampleRequest) -> None:
        stmt = (insert(self.orm).values(**payload.model_dump()))  # type: ignore
        await self.db_session.execute(stmt)
        await self.db_session.commit()
