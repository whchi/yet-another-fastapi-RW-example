from typing import Union

from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_exception_handler(_: Request, e: HTTPException) -> JSONResponse:
    return JSONResponse({'errors': [e.detail]}, status_code=e.status_code)


async def http422_exception_handler(
        _: Request,
        e: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    return JSONResponse(
        {'errors': e.errors()},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
