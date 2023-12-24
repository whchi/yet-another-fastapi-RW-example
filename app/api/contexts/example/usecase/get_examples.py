from typing import List

from fastapi.param_functions import Depends

from ..domain.schema import ExampleEntity
from ..gateway import ExampleRepository


class GetExamples:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self) -> List[ExampleEntity]:
        data = self.repo.index()
        return [] if not len(data) else [
            ExampleEntity(**row.model_dump()) for row in data
        ]
