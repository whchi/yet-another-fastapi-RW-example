from typing import List

from app.api.contexts.example.gateway import ExampleRepository
from fastapi.param_functions import Depends
from sqlalchemy.engine import Row


class GetExamples:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self) -> List[Row | None]:
        return self.repo.index()
