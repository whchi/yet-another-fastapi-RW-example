from fastapi.param_functions import Depends

from app.api.contexts.async_example.domain import AddExampleRequest
from app.api.contexts.async_example.gateway import ExampleRepository


class AddExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    async def execute(self, payload: AddExampleRequest) -> None:
        await self.repo.add(payload)
