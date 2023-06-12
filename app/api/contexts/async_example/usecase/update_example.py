from fastapi.param_functions import Depends

from app.api.contexts.async_example.domain import UpdateExampleRequest
from app.api.contexts.async_example.domain.schema import ExampleEntity
from app.api.contexts.async_example.gateway import ExampleRepository


class UpdateExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    async def execute(self, id: int, payload: UpdateExampleRequest) -> ExampleEntity:
        data = await self.repo.update(id, payload)
        return ExampleEntity(**data.dict())
