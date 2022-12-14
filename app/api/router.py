from app.api.contexts.example import router as example_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(example_router, tags=['example'], prefix='/examples')
