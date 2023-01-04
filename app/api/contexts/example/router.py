from fastapi import APIRouter
from fastapi.param_functions import Depends

from app.api.contexts.example.domain import (AddExampleRequest, AddExampleResponse,
                                             DeleteExampleResponse, GetExampleResponse,
                                             GetExamplesResponse, UpdateExampleRequest,
                                             UpdateExampleResponse)
from app.api.contexts.example.usecase import (AddExample, DeleteExample, GetExample,
                                              GetExamples, UpdateExample)

router = APIRouter()


@router.get('/{id}', response_model=GetExampleResponse)
def show(id: int, use_case: GetExample = Depends(GetExample)) -> GetExampleResponse:
    data = use_case.execute(id)
    return GetExampleResponse(data=data)


@router.get('', response_model=GetExamplesResponse)
async def get_all(use_case: GetExamples = Depends(GetExamples)) -> GetExamplesResponse:
    data = use_case.execute()
    return GetExamplesResponse(data=data)


@router.post('', response_model=AddExampleResponse)
async def add(
        payload: AddExampleRequest,
        use_case: AddExample = Depends(AddExample),
) -> AddExampleResponse:
    use_case.execute(payload)
    return AddExampleResponse()


@router.put('/{id}', response_model=UpdateExampleResponse)
async def update(
    id: int,
    payload: UpdateExampleRequest,
    use_case: UpdateExample = Depends(UpdateExample)
) -> UpdateExampleResponse:
    data = use_case.execute(id, payload)
    return UpdateExampleResponse(data=data)


@router.delete('/{id}', response_model=DeleteExampleResponse)
async def delete(
        id: int,
        use_case: DeleteExample = Depends(DeleteExample),
) -> DeleteExampleResponse:
    use_case.execute(id)
    return DeleteExampleResponse()
