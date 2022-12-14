from fastapi.exceptions import HTTPException
from starlette import status


class BadArgsException(ValueError):
    ...


class ModelNotFoundException(HTTPException):

    def __init__(self, detail: str = ''):
        self.detail = detail
        self.status_code = status.HTTP_404_NOT_FOUND
