from fastapi.param_functions import Depends

from app.api.contexts.example.domain import AddExampleRequest
from app.api.contexts.example.gateway import ExampleRepository


class AddExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self, payload: AddExampleRequest) -> None:
        self.repo.add(payload)
