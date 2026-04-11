"""Categories Router — Endpoints for life categories."""

from fastapi import APIRouter
from data.categories_data import CATEGORIES

router = APIRouter()


@router.get("/categories")
async def get_categories():
    return CATEGORIES
