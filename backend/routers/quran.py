"""Quran Router — Endpoints for Quran data access (local corpus + external service)."""

import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

import services.quran_service as quran_service
import services.quran_text_service as _local
from services.quran_text_service import search_ayahs, total_ayahs

router = APIRouter()


@router.get("/surahs")
async def list_surahs():
    return quran_service.get_all_surahs()


@router.get("/surah/{surah_number}")
async def get_surah_endpoint(surah_number: int):
    if surah_number < 1 or surah_number > 114:
        raise HTTPException(status_code=400, detail="رقم السورة يجب أن يكون بين 1 و 114")
    result = await quran_service.get_surah(surah_number)
    if not result:
        raise HTTPException(status_code=404, detail="لم يتم العثور على آيات لهذه السورة")
    return result


@router.get("/ayah/{surah}/{verse}")
async def get_ayah_local(surah: int, verse: int):
    """Return a specific ayah from the local corpus."""
    ayah = _local.get_ayah(surah, verse)
    if ayah is None:
        raise HTTPException(status_code=404, detail="الآية غير موجودة")
    return ayah.to_dict()


@router.get("/random")
async def get_random_ayah(surah_id: Optional[int] = None):
    """Return a random ayah, optionally from a specific surah."""
    if surah_id is not None and (surah_id < 1 or surah_id > 114):
        raise HTTPException(status_code=400, detail="رقم السورة يجب أن يكون بين 1 و 114")
    result = await quran_service.get_random_ayah(surah_id)
    if result is None:
        raise HTTPException(status_code=404, detail="لم يتم العثور على آيات")
    return result


@router.get("/word-of-day")
async def word_of_day():
    """Return today's fixed Quranic ayah (deterministic per calendar date)."""
    today = datetime.date.today()
    n = total_ayahs()
    day_index = today.toordinal() % n
    ayah = await quran_service.get_ayah_by_index(day_index)
    if ayah is None:
        raise HTTPException(status_code=503, detail="المصحف غير متاح")
    return {
        "date": str(today),
        "day_index": day_index,
        **ayah,
    }


@router.get("/corpus/search")
async def corpus_search(
    q: str = Query(min_length=2),
    top_k: int = Query(default=5, ge=1, le=20),
    category: Optional[str] = None,
):
    """Search the local Quran corpus and return ranked ayahs."""
    ayahs = search_ayahs(q, category, top_k=top_k)
    return {
        "query": q,
        "ayahs": [a.to_dict() for a in ayahs],
        "total_results": len(ayahs),
        "category": category or "general",
    }


@router.get("/search")
async def search(q: str = Query(min_length=2)):
    """Search the Quran corpus and return a list of matching ayahs."""
    ayahs = search_ayahs(q, top_k=20)
    return [a.to_dict() for a in ayahs]


@router.get("/verse/{surah_number}/{ayah_number}")
async def get_single_verse(surah_number: int, ayah_number: int):
    verse = quran_service.get_verse(surah_number, ayah_number)
    if not verse:
        raise HTTPException(status_code=404, detail="لم يتم العثور على الآية")
    return verse
