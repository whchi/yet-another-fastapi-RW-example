from datetime import datetime

from sqlalchemy import Column, func, TIMESTAMP
from sqlmodel import Field, SQLModel


class ${model}(SQLModel, table=True):
    __tablename__ = '${table_name}'

    id: int = Field(primary_key=True)

    created_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.utcnow))
    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow))
