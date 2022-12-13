from typing import Union

from app.exceptions.schema import ModelNotFoundException
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY


async def http_exception_handler(_: Request, e: HTTPException):
    return JSONResponse({'errors': [e.detail]}, status_code=e.status_code)


async def http404_exception_handler(
    _: Request,
    e: ModelNotFoundException,
) -> JSONResponse:
    return JSONResponse({'message': e.message}, status_code=HTTP_404_NOT_FOUND)


async def http422_exception_handler(
    _: Request,
    e: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    return JSONResponse(
        {'errors': e.errors()},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


validation_error_response_definition['properties'] = {
    'errors': {
        'title': 'Errors',
        'type': 'array',
        'items': {
            '$ref': '{0}ValidationError'.format(REF_PREFIX)
        },
    },
}
