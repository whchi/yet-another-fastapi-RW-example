from fastapi import APIRouter
from fastapi.param_functions import Depends, Query

from app.api.contexts.async_example.domain import (
    AddExampleRequest,
    AddExampleResponse,
    DeleteExampleResponse,
    GetExampleResponse,
    GetExamplesResponse,
    GetPaginateExamplesResponse,
    UpdateExampleRequest,
    UpdateExampleResponse,
)
from app.api.contexts.async_example.usecase import (
    AddExample,
    DeleteExample,
    GetExample,
    GetExamples,
    UpdateExample,
)
from app.api.contexts.async_example.usecase.get_paginate_examples import (
    GetPaginateExamples,
)

router = APIRouter()


@router.get('/paginate-examples', response_model=GetPaginateExamplesResponse)
async def get_all_paginate(
    page: int = Query(1, gt=0),
    per_page: int = Query(15, gt=0, min=5),
    use_case: GetPaginateExamples = Depends(GetPaginateExamples),
) -> GetPaginateExamplesResponse:
    data = await use_case.execute(page, per_page)
    return GetPaginateExamplesResponse(data=data)


@router.get('/{id}', response_model=GetExampleResponse)
async def show(
    id: int, use_case: GetExample = Depends(GetExample)) -> GetExampleResponse:
    data = await use_case.execute(id)
    return GetExampleResponse(data=data)


@router.get('', response_model=GetExamplesResponse)
async def get_all(use_case: GetExamples = Depends(GetExamples)) -> GetExamplesResponse:
    data = await use_case.execute()
    return GetExamplesResponse(data=data)


@router.post('', response_model=AddExampleResponse)
async def add(
        payload: AddExampleRequest,
        use_case: AddExample = Depends(AddExample),
) -> AddExampleResponse:
    await use_case.execute(payload)
    return AddExampleResponse()


@router.put('/{id}', response_model=UpdateExampleResponse)
async def update(
    id: int,
    payload: UpdateExampleRequest,
    use_case: UpdateExample = Depends(UpdateExample)
) -> UpdateExampleResponse:
    data = await use_case.execute(id, payload)
    return UpdateExampleResponse(data=data)


@router.delete('/{id}', response_model=DeleteExampleResponse)
async def delete(
        id: int,
        use_case: DeleteExample = Depends(DeleteExample),
) -> DeleteExampleResponse:
    await use_case.execute(id)
    return DeleteExampleResponse()
