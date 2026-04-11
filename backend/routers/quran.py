"""Quran Router — Endpoints for Quran data access."""

from fastapi import APIRouter, HTTPException
from services.quran_service import get_all_surahs, get_surah_verses, get_verse
from services.search_service import search_quran

router = APIRouter()


@router.get("/surahs")
async def list_surahs():
    return get_all_surahs()


@router.get("/surah/{surah_number}")
async def get_surah(surah_number: int):
    if surah_number < 1 or surah_number > 114:
        raise HTTPException(status_code=400, detail="رقم السورة يجب أن يكون بين 1 و 114")
    verses = get_surah_verses(surah_number)
    if not verses:
        raise HTTPException(status_code=404, detail="لم يتم العثور على آيات لهذه السورة")
    return verses


@router.get("/verse/{surah_number}/{ayah_number}")
async def get_single_verse(surah_number: int, ayah_number: int):
    verse = get_verse(surah_number, ayah_number)
    if not verse:
        raise HTTPException(status_code=404, detail="لم يتم العثور على الآية")
    return verse


@router.get("/search")
async def search(q: str = ""):
    if not q or len(q) < 2:
        raise HTTPException(status_code=400, detail="يجب أن يكون البحث أكثر من حرفين")
    return search_quran(q)
