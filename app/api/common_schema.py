import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class IDModel(BaseModel):
    id_: int = Field(..., alias='id')


class RWModel(BaseModel):

    class Config:
        allow_population_by_field_name = True


class TimestampsModel(BaseModel):
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    @validator('created_at', 'updated_at', pre=True)
    def default_datetime(cls, value: datetime.datetime) -> datetime.datetime:
        return value or datetime.datetime.now()


class ResponseBaseModel(BaseModel):
    data: Dict[str, Any] | List[Dict[str, Any]] | None = None
    message: Optional[str] = ''
    status: int = 200

    class Config:
        allow_population_by_field_name = True
