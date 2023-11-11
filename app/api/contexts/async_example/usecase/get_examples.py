from typing import List

from fastapi.param_functions import Depends

from ..domain import AsyncExampleEntity
from ..gateway import ExampleRepository


class GetExamples:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    async def execute(self) -> List[AsyncExampleEntity]:
        data = await self.repo.index()
        return [] if not len(data) else [
            AsyncExampleEntity(**row.dict()) for row in data
        ]
