from app.api.contexts.example.gateway import ExampleRepository
from fastapi.param_functions import Depends


class DeleteExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self, id: int) -> None:
        self.repo.delete(id)
