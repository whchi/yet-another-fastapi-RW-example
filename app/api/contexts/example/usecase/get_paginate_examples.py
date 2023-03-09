from fastapi.param_functions import Depends

from app.api.contexts.example.domain.schema import ExampleEntity
from app.api.contexts.example.gateway import ExampleRepository
from app.api.shared_schema import PageModel


class GetPaginateExamples:

    def __init__(self, repo: ExampleRepository = Depends(ExampleRepository)):
        self.repo = repo

    def execute(self, page: int = 1, per_page: int = 15) -> PageModel[ExampleEntity]:
        data = self.repo.paginate_index(page, per_page)
        formatted = [ExampleEntity(**item.dict()) for item in data['items']]
        data['items'] = formatted
        return PageModel[ExampleEntity](**data)
