from typing import List

from pydantic import BaseModel, Field, ConfigDict
from starlette import status

from app.api.shared_schema import (
    IDModel,
    PageModel,
    PaginateResponseBaseModel,
    ResponseBaseModel,
    RWModel,
    TimestampsModel,
)


class AsyncExampleEntity(IDModel, TimestampsModel, RWModel):
    name: str
    age: int
    nick_name: str | None


class AddExampleRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        'example': {
            'name': 'my name',
            'age': 18,
            'nick_name': 'my nick name'
        }
    })

    name: str = Field(..., min_length=2)
    age: int = Field(..., min=1)
    nick_name: str | None = Field(None, min_length=2)

class AddExampleResponse(ResponseBaseModel[dict[None, None]]):
    status: int = status.HTTP_201_CREATED
    data: dict[None, None] = {}


class UpdateExampleRequest(BaseModel):
    name: str = Field(..., min_length=2)
    age: int | None = Field(None, min=1)
    nick_name: str | None = Field(None, min_length=2)


class UpdateExampleResponse(ResponseBaseModel[AsyncExampleEntity]):
    data: AsyncExampleEntity


class GetExampleResponse(ResponseBaseModel[AsyncExampleEntity]):
    data: AsyncExampleEntity


class GetExamplesResponse(ResponseBaseModel[List[AsyncExampleEntity]]):
    data: List[AsyncExampleEntity]


class DeleteExampleResponse(ResponseBaseModel[dict[None, None]]):
    data: dict[None, None] = {}


class GetPaginateExamplesResponse(PaginateResponseBaseModel[AsyncExampleEntity]):
    data: PageModel[AsyncExampleEntity]
