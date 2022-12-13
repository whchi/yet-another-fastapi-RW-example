from app.api.contexts.example.gateway import ExampleRepository
from fastapi.param_functions import Depends


class UpdateExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self, id, payload):
        return self.repo.update(id, payload)
