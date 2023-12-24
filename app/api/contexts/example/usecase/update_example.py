from fastapi.param_functions import Depends

from ..domain import ExampleEntity, UpdateExampleRequest
from ..gateway import ExampleRepository


class UpdateExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self, id: int, payload: UpdateExampleRequest) -> ExampleEntity:
        data = self.repo.update(id, payload)
        return ExampleEntity(**data.model_dump())
