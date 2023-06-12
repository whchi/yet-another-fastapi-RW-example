from fastapi.param_functions import Depends

from app.api.contexts.async_example.gateway import ExampleRepository


class DeleteExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    async def execute(self, id: int) -> None:
        await self.repo.delete(id)
