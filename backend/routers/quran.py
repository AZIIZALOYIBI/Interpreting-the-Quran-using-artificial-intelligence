import datetime
import random as _random
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from services import quran_service
from services.quran_text_service import get_ayah as get_local_ayah, total_ayahs, search_ayahs as local_search

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
    # First try the local verified corpus
    local = get_local_ayah(surah_id, ayah_number)
    if local:
        return local.to_dict()
    # Fall back to external service
    ayah = await quran_service.get_ayah(surah_id, ayah_number)
    if not ayah:
        raise HTTPException(status_code=404, detail="الآية غير موجودة")
    return ayah


@router.get("/search")
async def search_ayahs(q: str = Query(..., min_length=2)):
    results = await quran_service.search_ayahs(q)
    return results


# ---------------------------------------------------------------------------
# ✨ Creative endpoints
# ---------------------------------------------------------------------------

_SURAH_VERSE_COUNTS = {
    1: 7, 2: 286, 3: 200, 4: 176, 5: 120, 6: 165, 7: 206, 8: 75, 9: 129,
    10: 109, 11: 123, 12: 111, 13: 43, 14: 52, 15: 99, 16: 128, 17: 111,
    18: 110, 19: 98, 20: 135, 21: 112, 22: 78, 23: 118, 24: 64, 25: 77,
    26: 227, 27: 93, 28: 88, 29: 69, 30: 60, 31: 34, 32: 30, 33: 73,
    34: 54, 35: 45, 36: 83, 37: 182, 38: 88, 39: 75, 40: 85, 41: 54,
    42: 53, 43: 89, 44: 59, 45: 37, 46: 35, 47: 38, 48: 29, 49: 18,
    50: 45, 51: 60, 52: 49, 53: 62, 54: 55, 55: 78, 56: 96, 57: 29,
    58: 22, 59: 24, 60: 13, 61: 14, 62: 11, 63: 11, 64: 18, 65: 12,
    66: 12, 67: 30, 68: 52, 69: 52, 70: 44, 71: 28, 72: 28, 73: 20,
    74: 56, 75: 40, 76: 31, 77: 50, 78: 40, 79: 46, 80: 42, 81: 29,
    82: 19, 83: 36, 84: 25, 85: 22, 86: 17, 87: 19, 88: 26, 89: 30,
    90: 20, 91: 15, 92: 21, 93: 11, 94: 8, 95: 8, 96: 19, 97: 5,
    98: 8, 99: 8, 100: 11, 101: 11, 102: 8, 103: 3, 104: 9, 105: 5,
    106: 4, 107: 7, 108: 3, 109: 6, 110: 3, 111: 5, 112: 4, 113: 5,
    114: 6,
}


@router.get("/random")
def get_random_ayah(surah_id: Optional[int] = None):
    """
    ✨ آية عشوائية من المصحف الكريم.

    - بدون معامِلات: تختار آية عشوائية من كامل المصحف (6236 آية).
    - مع `surah_id`: تختار آية عشوائية من السورة المحددة.
    """
    if surah_id is not None:
        if surah_id < 1 or surah_id > 114:
            raise HTTPException(status_code=400, detail="رقم السورة يجب أن يكون بين 1 و 114")
        max_verse = _SURAH_VERSE_COUNTS.get(surah_id, 1)
        verse = _random.randint(1, max_verse)
    else:
        # Pick a random surah weighted by verse count
        surah_id = _random.choices(
            list(_SURAH_VERSE_COUNTS.keys()),
            weights=list(_SURAH_VERSE_COUNTS.values()),
        )[0]
        verse = _random.randint(1, _SURAH_VERSE_COUNTS[surah_id])

    ayah = get_local_ayah(surah_id, verse)
    if not ayah:
        raise HTTPException(status_code=404, detail="لم يتم العثور على الآية")
    return ayah.to_dict()


@router.get("/word-of-day")
def get_word_of_day():
    """
    ✨ آية اليوم — آية ثابتة طوال اليوم مستخرجة من المصحف الكريم.

    تتغير كل يوم تلقائياً بناءً على التاريخ الميلادي.
    تضمن توزيعاً عادلاً على كامل المصحف بمرور الوقت.
    """
    day_number = datetime.date.today().toordinal()
    total = total_ayahs()  # 6236
    # Deterministic index based on day number
    index = day_number % total

    # Walk through the corpus to find the ayah at this index
    count = 0
    for s_id in range(1, 115):
        verse_count = _SURAH_VERSE_COUNTS.get(s_id, 0)
        if count + verse_count > index:
            verse = (index - count) + 1
            ayah = get_local_ayah(s_id, verse)
            if ayah:
                return {
                    **ayah.to_dict(),
                    "date": str(datetime.date.today()),
                    "day_index": index,
                }
            break
        count += verse_count

    raise HTTPException(status_code=500, detail="تعذّر تحديد آية اليوم")


@router.get("/corpus/search")
def corpus_search(
    q: str = Query(..., min_length=2, description="نص البحث العربي"),
    category: Optional[str] = None,
    top_k: int = Query(default=5, ge=1, le=20),
):
    """
    ✨ بحث مباشر في نص المصحف المحلي (6236 آية) بدون اتصال خارجي.

    يستخدم محرك البحث العربي المُطبَّع المُدمَج في المنصة.
    - `q`: نص البحث (عربي، حد أدنى حرفان)
    - `category`: فئة اختيارية لتعزيز نتائج البحث
    - `top_k`: عدد النتائج (1-20، افتراضي 5)
    """
    results = local_search(q, category=category, top_k=top_k)
    return {
        "query": q,
        "category": category,
        "total_results": len(results),
        "ayahs": [a.to_dict() for a in results],
    }
