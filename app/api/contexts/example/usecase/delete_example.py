from fastapi.param_functions import Depends

from ..gateway import ExampleRepository


class DeleteExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self, id: int) -> None:
        self.repo.delete(id)
