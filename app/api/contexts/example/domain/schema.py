from typing import Any, List

from pydantic import BaseModel, Field
from starlette import status

from app.api.shared_schema import (
    IDModel,
    PageModel,
    PaginateResponseBaseModel,
    ResponseBaseModel,
    RWModel,
    TimestampsModel,
)


class ExampleEntity(IDModel, TimestampsModel, RWModel):
    name: str
    age: int
    nick_name: str | None


class AddExampleRequest(BaseModel):
    model_config: dict[str, Any] = {  # type: ignore
        'json_schema_extra': {
            'example': {
                'name': 'my name',
                'age': 18,
                'nick_name': 'my nick name'
            }
        }
    }

    name: str = Field(..., min_length=2)
    age: int = Field(..., gt=1)
    nick_name: str | None = Field(None, min_length=2)


class AddExampleResponse(ResponseBaseModel[dict[None, None]]):
    status: int = status.HTTP_201_CREATED
    data: dict[None, None] = {}


class UpdateExampleRequest(BaseModel):
    name: str = Field(..., min_length=2)
    age: int | None = Field(None, gt=1)
    nick_name: str | None = Field(None, min_length=2)


class UpdateExampleResponse(ResponseBaseModel[ExampleEntity]):
    data: ExampleEntity


class GetExampleResponse(ResponseBaseModel[ExampleEntity]):
    data: ExampleEntity


class GetExamplesResponse(ResponseBaseModel[List[ExampleEntity]]):
    data: List[ExampleEntity]


class DeleteExampleResponse(ResponseBaseModel[dict[None, None]]):
    data: dict[None, None] = {}


class GetPaginateExamplesResponse(PaginateResponseBaseModel[ExampleEntity]):
    data: PageModel[ExampleEntity]
