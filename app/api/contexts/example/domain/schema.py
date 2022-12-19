from typing import List

from app.api.common_schema import IDModel, ResponseBaseModel, RWModel, TimestampsModel  # noqa: E501
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
        schema_extra = {'example': {'name': 'my name', 'age': 18, 'nick_name': 'my nick name'}}


class AddExampleResponse(ResponseBaseModel):
    status: int = status.HTTP_201_CREATED


class UpdateExampleRequest(BaseModel):
    name: str = Field(..., min_length=2)
    age: int | None = Field(None, min=1)
    nick_name: str | None = Field(None, min_length=2)


class UpdateExampleResponse(ResponseBaseModel):
    data: ExampleEntity  # type: ignore


class GetExampleResponse(ResponseBaseModel):
    data: ExampleEntity | None  # type: ignore


class GetExamplesResponse(ResponseBaseModel):
    data: List[ExampleEntity | None]  # type: ignore


class DeleteExampleResponse(ResponseBaseModel):
    ...
