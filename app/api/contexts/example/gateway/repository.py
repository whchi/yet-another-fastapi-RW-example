from typing import Any, Dict, List

from fastapi.param_functions import Depends
from sqlalchemy.engine import Row
from sqlalchemy.sql import delete, insert, update
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

    def show(self, id: int) -> Row:
        row = self.db_session.execute(select(self.orm).filter_by(id=id)).fetchone()

        if not row:
            raise ModelNotFoundException(
                detail=f'{self.orm.__tablename__}.id={id} not found')

        return row

    def update(self, id: int, payload: UpdateExampleRequest) -> Row:
        stmt = (update(self.orm).where(self.orm.id == id).values(
            payload.dict(exclude_unset=True)).returning(self.orm.id))

        result = self.db_session.execute(stmt)

        if not result.first():
            raise ModelNotFoundException(
                detail=f'{self.orm.__tablename__}.id={id} not found')

        return self.db_session.execute(select(self.orm).filter_by(id=id)).one()

    def delete(self, id: int) -> None:
        self.show(id)

        stmt = (delete(self.orm).filter_by(id=id))
        self.db_session.execute(stmt)

    def add(self, payload: AddExampleRequest) -> None:
        stmt = (insert(self.orm).values(**payload.dict()))
        self.db_session.execute(stmt)
