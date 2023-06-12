from fastapi import APIRouter

from app.api.contexts.async_example import router as async_example_router
from app.api.contexts.example import router as example_router

router = APIRouter()

router.include_router(example_router, tags=['example'], prefix='/examples')
router.include_router(async_example_router,
                      tags=['async_example'],
                      prefix='/async-examples')
