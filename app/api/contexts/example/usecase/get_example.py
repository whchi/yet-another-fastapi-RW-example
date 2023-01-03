from app.api.contexts.example.domain.schema import ExampleEntity
from app.api.contexts.example.gateway import ExampleRepository
from fastapi.param_functions import Depends


class GetExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self, id: int) -> ExampleEntity:
        data = self.repo.show(id)
        return ExampleEntity(**data[0].dict())
