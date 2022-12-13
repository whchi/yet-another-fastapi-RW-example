from app.api.router import router as api_router
from app.core.config import get_app_settings
from app.exceptions.handler import (
    http404_exception_handler,
    http422_exception_handler,
    http_exception_handler,
)
from app.exceptions.schema import ModelNotFoundException
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware


def get_application() -> FastAPI:
    settings = get_app_settings()

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )
    application.add_exception_handler(
        RequestValidationError,
        http422_exception_handler,
    )

    application.add_exception_handler(
        ModelNotFoundException,
        http404_exception_handler,
    )

    application.include_router(api_router, prefix='/api')

    return application


app = get_application()
