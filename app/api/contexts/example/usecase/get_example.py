from fastapi.param_functions import Depends

from ..domain.schema import ExampleEntity
from ..gateway import ExampleRepository


class GetExample:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self, id: int) -> ExampleEntity:
        data = self.repo.show(id)
        return ExampleEntity(**data.dict())
