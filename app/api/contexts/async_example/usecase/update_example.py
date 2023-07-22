from fastapi.param_functions import Depends

from ..domain import UpdateExampleRequest
from ..domain.schema import AsyncExampleEntity
from ..gateway import ExampleRepository


class UpdateExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    async def execute(self, id: int,
                      payload: UpdateExampleRequest) -> AsyncExampleEntity:
        data = await self.repo.update(id, payload)
        return AsyncExampleEntity(**data.dict())
