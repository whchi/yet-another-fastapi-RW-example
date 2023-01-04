from fastapi import APIRouter

from app.api.contexts.example import router as example_router

router = APIRouter()

router.include_router(example_router, tags=['example'], prefix='/examples')
