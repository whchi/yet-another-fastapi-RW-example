import datetime
from enum import Enum
from typing import Any, Generic, List, TypeVar

from pydantic import BaseModel, Field
from pydantic.functional_validators import field_validator


class ResponseStatusEnum(str, Enum):
    # @see https://github.com/omniti-labs/jsend
    SUCCESS = 'success'
    FAIL = 'fail'
    ERROR = 'error'


class IDModel(BaseModel):
    id_: int = Field(..., alias='id')


class RWModel(BaseModel):
    model_config: dict[str, Any] = {'populate_by_name': True}


class TimestampsModel(BaseModel):
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def default_datetime(cls, value: datetime.datetime) -> datetime.datetime:
        return value or datetime.datetime.now()


T = TypeVar('T')


class ResponseBaseModel(BaseModel, Generic[T]):
    model_config: dict[str, Any] = {'populate_by_name': True}

    data: T | None = None
    message: str | None = ''
    status: int = 200


class PageModel(BaseModel, Generic[T]):
    items: List[T] = []
    total: int
    current_page: int
    last_page: int | None
    prev_page: int | None
    next_page: int | None
    per_page: int


class PaginateResponseBaseModel(BaseModel, Generic[T]):
    model_config: dict[str, Any] = {'populate_by_name': True}

    data: PageModel[T]
    message: str | None = ''
    status: ResponseStatusEnum = ResponseStatusEnum.SUCCESS
