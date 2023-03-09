import datetime
from enum import Enum
from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel


class ResponseStatusEnum(str, Enum):
    # @see https://github.com/omniti-labs/jsend
    SUCCESS = 'success'
    FAIL = 'fail'
    ERROR = 'error'


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


class PageModel(GenericModel, Generic[T]):
    items: List[T] = []
    total: int
    current_page: int
    last_page: int | None
    prev_page: int | None
    next_page: int | None
    per_page: int


class PaginateResponseBaseModel(GenericModel, Generic[T]):
    data: PageModel[T]
    message: str | None = ''
    status: ResponseStatusEnum = ResponseStatusEnum.SUCCESS

    class Config:
        allow_population_by_field_name = True
