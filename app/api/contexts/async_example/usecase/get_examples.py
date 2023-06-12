from typing import List

from fastapi.param_functions import Depends

from app.api.contexts.async_example.domain.schema import ExampleEntity
from app.api.contexts.async_example.gateway import ExampleRepository


class GetExamples:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    async def execute(self) -> List[ExampleEntity]:
        data = await self.repo.index()
        return [] if not len(data) else [ExampleEntity(**row.dict()) for row in data]
