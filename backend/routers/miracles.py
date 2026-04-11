"""Miracles Router — Endpoints for scientific miracles in the Quran."""

from fastapi import APIRouter
from data.scientific_miracles import SCIENTIFIC_MIRACLES

router = APIRouter()


@router.get("/miracles")
async def get_miracles():
    return SCIENTIFIC_MIRACLES


@router.get("/miracles/{category}")
async def get_miracles_by_category(category: str):
    return [m for m in SCIENTIFIC_MIRACLES if m.get("category") == category]
