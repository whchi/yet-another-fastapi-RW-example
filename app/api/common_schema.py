import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel


class IDModel(BaseModel):
    id_: int = Field(..., alias='id')


class RWModel(BaseModel):

    class Config:
        allow_population_by_field_name = True


class TimestampsModel(BaseModel):
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None

    @validator('created_at', 'updated_at', pre=True)
    def default_datetime(cls, value: datetime.datetime) -> datetime.datetime:
        return value or datetime.datetime.now()


T = TypeVar('T')


class ResponseBaseModel(GenericModel, Generic[T]):
    data: T | None = None
    message: str | None = ''
    status: int = 200

    class Config:
        allow_population_by_field_name = True
