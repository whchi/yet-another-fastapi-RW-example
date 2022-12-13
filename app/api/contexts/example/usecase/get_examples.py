from app.api.contexts.example.gateway import ExampleRepository
from fastapi.param_functions import Depends


class GetExamples:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self):
        return self.repo.index()
