import math
from typing import Any, Dict, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Query
from sqlalchemy.sql import func


class ModelPaginator:

    @staticmethod
    def paginate(
            query: Query,  # type: ignore
            page: int,
            per_page: int) -> Dict[str, Any]:
        total = query.count()
        last_page = math.ceil(float(total) / float(per_page))

        next_page = None if page == last_page else page + 1
        prev_page = None if page <= 1 else page - 1

        if page > last_page:
            next_page = None
            prev_page = last_page
        items = list(query.offset((page - 1) * per_page).limit(per_page))
        return {
            'items': items,
            'total': total,
            'current_page': page,
            'last_page': last_page,
            'prev_page': prev_page,
            'next_page': next_page,
            'per_page': per_page
        }

    @staticmethod
    async def async_paginate(session: AsyncSession,
                             model: Any,
                             page: int,
                             per_page: int,
                             order_by: List[Any] | None = None) -> Dict[str, Any]:

        # count total number of rows
        stmt = select(func.count()).select_from(model)
        total = await session.scalar(stmt) or 0
        last_page = math.ceil(total / per_page)

        next_page = None if page == last_page else page + 1
        prev_page = None if page <= 1 else page - 1

        if page > last_page:
            next_page = None
            prev_page = last_page

        # select rows for current page
        stmt = select(model)
        if order_by:
            stmt = stmt.order_by(*order_by)
        stmt = stmt.offset((page - 1) * per_page).limit(per_page)

        result = await session.execute(stmt)
        items = result.scalars().all()  # updated this line

        return {
            'items': items,
            'total': total,
            'current_page': page,
            'last_page': last_page,
            'prev_page': prev_page,
            'next_page': next_page,
            'per_page': per_page
        }
