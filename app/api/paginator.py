import math
from typing import Any, Dict

from sqlalchemy.orm import Query


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

        items = [x for x in query.offset((page - 1) * per_page).limit(per_page)]
        return {
            'items': items,
            'total': total,
            'current_page': page,
            'last_page': last_page,
            'prev_page': prev_page,
            'next_page': next_page,
            'per_page': per_page
        }
