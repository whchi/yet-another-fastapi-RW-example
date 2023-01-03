from app.api.contexts.example.domain import UpdateExampleRequest
from app.api.contexts.example.domain.schema import ExampleEntity
from app.api.contexts.example.gateway import ExampleRepository
from fastapi.param_functions import Depends


class UpdateExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self, id: int, payload: UpdateExampleRequest) -> ExampleEntity:
        data = self.repo.update(id, payload)
        return ExampleEntity(**data[0].dict())
