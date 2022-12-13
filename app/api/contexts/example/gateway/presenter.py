from typing import List

from app.api.contexts.example.domain.schema import ExampleEntity
from sqlalchemy.engine import Row


class ExamplePresenter:

    @staticmethod
    def format(rows: List[Row] | Row):
        if isinstance(rows, List):
            return [] if not len(rows) else [ExampleEntity(**row[0].dict()) for row in rows]
        return ExampleEntity(**rows[0].dict())
