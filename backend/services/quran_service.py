import httpx
from typing import List, Optional, Dict, Any

ALQURAN_API = "https://api.alquran.cloud/v1"


async def get_ayah(surah_id: int, ayah_number: int) -> Optional[Dict[str, Any]]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{ALQURAN_API}/ayah/{surah_id}:{ayah_number}/ar.uthmani")
            if resp.status_code == 200:
                data = resp.json()
                ayah = data.get("data", {})
                surah = ayah.get("surah", {})
                return {
                    "id": ayah.get("number"),
                    "surah_id": surah_id,
                    "surah_name": surah.get("englishName", ""),
                    "surah_name_ar": surah.get("name", ""),
                    "ayah_number": ayah_number,
                    "text_uthmani": ayah.get("text", ""),
                    "text_simple": ayah.get("text", ""),
                }
    except Exception:
        pass
    return None


async def get_surah(surah_id: int) -> Optional[Dict[str, Any]]:
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{ALQURAN_API}/surah/{surah_id}/ar.uthmani")
            if resp.status_code == 200:
                data = resp.json()
                surah_data = data.get("data", {})
                ayahs = []
                for a in surah_data.get("ayahs", []):
                    ayahs.append({
                        "id": a.get("number"),
                        "surah_id": surah_id,
                        "surah_name": surah_data.get("englishName", ""),
                        "surah_name_ar": surah_data.get("name", ""),
                        "ayah_number": a.get("numberInSurah"),
                        "text_uthmani": a.get("text", ""),
                        "text_simple": a.get("text", ""),
                    })
                return {
                    "info": {
                        "id": surah_id,
                        "name_ar": surah_data.get("name", ""),
                        "name_en": surah_data.get("englishName", ""),
                        "ayah_count": surah_data.get("numberOfAyahs", 0),
                        "revelation_type": surah_data.get("revelationType", "").lower(),
                    },
                    "ayahs": ayahs,
                }
    except Exception:
        pass
    return None


async def search_ayahs(query: str) -> List[Dict[str, Any]]:
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{ALQURAN_API}/search/{query}/all/ar")
            if resp.status_code == 200:
                data = resp.json()
                matches = data.get("data", {}).get("matches", [])
                results = []
                for m in matches[:10]:
                    surah = m.get("surah", {})
                    results.append({
                        "id": m.get("number"),
                        "surah_id": surah.get("number"),
                        "surah_name": surah.get("englishName", ""),
                        "surah_name_ar": surah.get("name", ""),
                        "ayah_number": m.get("numberInSurah"),
                        "text_uthmani": m.get("text", ""),
                        "text_simple": m.get("text", ""),
                    })
                return results
    except Exception:
        pass
    return []


async def get_surah_list() -> List[Dict[str, Any]]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{ALQURAN_API}/surah")
            if resp.status_code == 200:
                data = resp.json()
                return [
                    {
                        "id": s.get("number"),
                        "name_ar": s.get("name"),
                        "name_en": s.get("englishName"),
                        "ayah_count": s.get("numberOfAyahs"),
                        "revelation_type": s.get("revelationType", "").lower(),
                    }
                    for s in data.get("data", [])
                ]
    except Exception:
        pass
    return []
