from app.api.contexts.example.gateway import ExampleRepository
from fastapi.param_functions import Depends
from sqlalchemy.engine import Row


class GetExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self, id: int) -> Row:
        return self.repo.show(id)
