from fastapi import APIRouter, HTTPException, Query
from typing import List
from services import quran_service

router = APIRouter(prefix="/api/quran", tags=["quran"])


@router.get("/surahs")
async def get_surahs():
    surahs = await quran_service.get_surah_list()
    return surahs


@router.get("/surah/{surah_id}")
async def get_surah(surah_id: int):
    if surah_id < 1 or surah_id > 114:
        raise HTTPException(status_code=400, detail="رقم السورة يجب أن يكون بين 1 و 114")
    data = await quran_service.get_surah(surah_id)
    if not data:
        raise HTTPException(status_code=404, detail="السورة غير موجودة")
    return data


@router.get("/ayah/{surah_id}/{ayah_number}")
async def get_ayah(surah_id: int, ayah_number: int):
    ayah = await quran_service.get_ayah(surah_id, ayah_number)
    if not ayah:
        raise HTTPException(status_code=404, detail="الآية غير موجودة")
    return ayah


@router.get("/search")
async def search_ayahs(q: str = Query(..., min_length=2)):
    results = await quran_service.search_ayahs(q)
    return results
