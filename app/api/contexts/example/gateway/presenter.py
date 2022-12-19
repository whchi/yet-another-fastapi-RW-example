# mypy: ignore-errors
from typing import Any, List

from app.api.contexts.example.domain.schema import ExampleEntity
from sqlalchemy.engine.row import Row


class ExamplePresenter:

    @staticmethod
    def format(rows: List[Row | None] | Row | None) -> Any:
        if isinstance(rows, List):
            return [] if not len(rows) else [ExampleEntity(**row[0].dict()) for row in rows]
        return ExampleEntity(**rows[0].dict())
