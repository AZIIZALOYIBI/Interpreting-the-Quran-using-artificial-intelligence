from fastapi import APIRouter
from data.scientific_miracles import SCIENTIFIC_MIRACLES

router = APIRouter(prefix="/api/miracles", tags=["miracles"])


@router.get("")
def get_miracles():
    return SCIENTIFIC_MIRACLES


@router.get("/{category}")
def get_miracles_by_category(category: str):
    filtered = [m for m in SCIENTIFIC_MIRACLES if m["category"] == category]
    return filtered
