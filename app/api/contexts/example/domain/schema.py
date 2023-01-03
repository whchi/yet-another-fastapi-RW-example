from typing import List

from app.api.common_schema import RWModel  # noqa: E501
from app.api.common_schema import IDModel, ResponseBaseModel, TimestampsModel
from pydantic import BaseModel, Field
from starlette import status


class ExampleEntity(IDModel, TimestampsModel, RWModel):
    name: str
    age: int
    nick_name: str | None


class AddExampleRequest(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., min=1)
    nick_name: str | None = Field(None, min_length=2)

    class Config:
        schema_extra = {
            'example': {
                'name': 'my name',
                'age': 18,
                'nick_name': 'my nick name'
            }
        }


class AddExampleResponse(ResponseBaseModel[dict[None, None]]):
    status: int = status.HTTP_201_CREATED
    data: dict[None, None] = {}


class UpdateExampleRequest(BaseModel):
    name: str = Field(..., min_length=2)
    age: int | None = Field(None, min=1)
    nick_name: str | None = Field(None, min_length=2)


class UpdateExampleResponse(ResponseBaseModel[ExampleEntity]):
    data: ExampleEntity


class GetExampleResponse(ResponseBaseModel[ExampleEntity]):
    data: ExampleEntity


class GetExamplesResponse(ResponseBaseModel[List[ExampleEntity]]):
    data: List[ExampleEntity]


class DeleteExampleResponse(ResponseBaseModel[dict[None, None]]):
    data: dict[None, None] = {}
