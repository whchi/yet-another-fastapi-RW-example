from fastapi.param_functions import Depends

from ..domain.schema import AsyncExampleEntity
from ..gateway import ExampleRepository


class GetExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    async def execute(self, id: int) -> AsyncExampleEntity:
        data = await self.repo.show(id)
        return AsyncExampleEntity(**data.model_dump())
