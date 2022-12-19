from app.api.contexts.example.domain import UpdateExampleRequest
from app.api.contexts.example.gateway import ExampleRepository
from fastapi.param_functions import Depends
from sqlalchemy.engine import Row


class UpdateExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self, id: int, payload: UpdateExampleRequest) -> Row | None:
        return self.repo.update(id, payload)
