"""Tafsir Router — Endpoints for Quran interpretations."""

from fastapi import APIRouter
from data.tafsir_data import TAFSIR_DATA

router = APIRouter()


@router.get("/tafsir/{surah_number}/{ayah_number}")
async def get_tafsir(surah_number: int, ayah_number: int):
    key = f"{surah_number}:{ayah_number}"
    tafsirs = TAFSIR_DATA.get(key, [])
    if not tafsirs:
        return TAFSIR_DATA.get("default", [])
    return tafsirs
