from datetime import datetime

from sqlalchemy import Column, TIMESTAMP
from sqlmodel import Field, SQLModel


class Example(SQLModel, table=True):
    __tablename__ = 'examples'

    id: int = Field(default=None, primary_key=True)
    name: str
    nick_name: str | None = Field(default=None)
    age: int
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.utcnow))
    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow))
