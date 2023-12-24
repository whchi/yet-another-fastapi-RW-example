from typing import Any, Dict, List

from fastapi.param_functions import Depends
from sqlalchemy.engine import Row
from sqlalchemy.sql import delete, insert
from sqlmodel import Session
from sqlmodel.sql.expression import col, select

from app.api.contexts.example.domain import AddExampleRequest, UpdateExampleRequest
from app.api.paginator import ModelPaginator
from app.exceptions.schema import ModelNotFoundException
from app.models import Example
from database.connection import get_session


# a = Row()
class ExampleRepository:

    def __init__(self, db_session: Session = Depends(get_session)):
        self.orm = Example
        self.db_session = db_session

    def index(self) -> List[Row]:
        return self.db_session.execute(select(self.orm)).all()

    def paginate_index(
        self,
        page: int,
        per_page: int,
    ) -> Dict[str, Any]:
        query = self.db_session.query(self.orm).order_by(
            col(self.orm.created_at).desc(),
            col(self.orm.id).desc())

        return ModelPaginator.paginate(query, page, per_page)

    def show(self, id: int) -> Example:
        row = self.db_session.execute(select(self.orm).filter_by(id=id)).scalar()

        if not row:
            raise ModelNotFoundException(
                detail=f'{self.orm.__tablename__}.id={id} not found')

        return row

    def update(self, id: int, payload: UpdateExampleRequest) -> Example:
        row = self.show(id)
        row.name = payload.name
        if payload.age:
            row.age = payload.age
        row.nick_name = payload.nick_name
        self.db_session.add(row)
        self.db_session.commit()
        self.db_session.refresh(row)
        return row

    def delete(self, id: int) -> None:
        self.show(id)

        stmt = (delete(self.orm).filter_by(id=id))
        self.db_session.execute(stmt)
        self.db_session.commit()

    def add(self, payload: AddExampleRequest) -> None:
        stmt = (insert(self.orm).values(**payload.model_dump()))  # type: ignore
        self.db_session.execute(stmt)
        self.db_session.commit()
