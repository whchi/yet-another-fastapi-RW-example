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


class AddExampleResponse(ResponseBaseModel):
    status: int = status.HTTP_201_CREATED


class UpdateExampleRequest(BaseModel):
    name: str = Field(..., min_length=2)
    age: int | None = Field(None, min=1)
    nick_name: str | None = Field(None, min_length=2)


class UpdateExampleResponse(ResponseBaseModel):
    data: ExampleEntity


class GetExampleResponse(ResponseBaseModel):
    data: ExampleEntity | None


class GetExamplesResponse(ResponseBaseModel):
    data: List[ExampleEntity | None]


class DeleteExampleResponse(ResponseBaseModel):
    ...
