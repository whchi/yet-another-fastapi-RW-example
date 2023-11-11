from fastapi import APIRouter
from fastapi.param_functions import Depends, Query

from app.api.contexts.example.domain import (
    AddExampleRequest,
    AddExampleResponse,
    DeleteExampleResponse,
    GetExampleResponse,
    GetExamplesResponse,
    GetPaginateExamplesResponse,
    UpdateExampleRequest,
    UpdateExampleResponse,
)
from app.api.contexts.example.usecase import (
    AddExample,
    DeleteExample,
    GetExample,
    GetExamples,
    UpdateExample,
)
from app.api.contexts.example.usecase.get_paginate_examples import GetPaginateExamples

router = APIRouter()


@router.get('/paginate-examples', response_model=GetPaginateExamplesResponse)
def get_all_paginate(
    page: int = Query(1, gt=0),
    per_page: int = Query(15, gt=0, min=5),
    use_case: GetPaginateExamples = Depends(GetPaginateExamples),
) -> GetPaginateExamplesResponse:
    data = use_case.execute(page, per_page)
    return GetPaginateExamplesResponse(data=data)


@router.get('/{id}', response_model=GetExampleResponse)
def show(id: int, use_case: GetExample = Depends(GetExample)) -> GetExampleResponse:
    data = use_case.execute(id)
    return GetExampleResponse(data=data)


@router.get('', response_model=GetExamplesResponse)
def get_all(use_case: GetExamples = Depends(GetExamples)) -> GetExamplesResponse:
    data = use_case.execute()
    return GetExamplesResponse(data=data)


@router.post('', response_model=AddExampleResponse)
def add(
    payload: AddExampleRequest,
    use_case: AddExample = Depends(AddExample),
) -> AddExampleResponse:
    use_case.execute(payload)
    return AddExampleResponse()


@router.put('/{id}', response_model=UpdateExampleResponse)
def update(
    id: int,
    payload: UpdateExampleRequest,
    use_case: UpdateExample = Depends(UpdateExample)
) -> UpdateExampleResponse:
    data = use_case.execute(id, payload)
    return UpdateExampleResponse(data=data)


@router.delete('/{id}', response_model=DeleteExampleResponse)
def delete(
    id: int,
    use_case: DeleteExample = Depends(DeleteExample),
) -> DeleteExampleResponse:
    use_case.execute(id)
    return DeleteExampleResponse()
