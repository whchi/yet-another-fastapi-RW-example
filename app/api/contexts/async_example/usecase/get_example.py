from fastapi.param_functions import Depends

from app.api.contexts.async_example.domain.schema import ExampleEntity
from app.api.contexts.async_example.gateway import ExampleRepository


class GetExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    async def execute(self, id: int) -> ExampleEntity:
        data = await self.repo.show(id)
        return ExampleEntity(**data.dict())
