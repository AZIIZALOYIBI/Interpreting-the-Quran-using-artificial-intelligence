"""Quran Service — Quran data from local corpus and external AlQuran.cloud API."""

import random
import urllib.parse
from typing import Optional

import httpx

from data.quran_data import QURAN_VERSES, SURAHS
import services.quran_text_service as _corpus

_BASE_URL = "https://api.alquran.cloud/v1"


# ── Local corpus helpers ─────────────────────────────────────────────────────

def get_all_surahs() -> list:
    return SURAHS


def get_surah_verses(surah_number: int) -> list:
    return [v for v in QURAN_VERSES if v["surah_number"] == surah_number]


def get_verse(surah_number: int, ayah_number: int) -> dict | None:
    for v in QURAN_VERSES:
        if v["surah_number"] == surah_number and v["ayah_number"] == ayah_number:
            return v
    return None


async def get_random_ayah(surah_id: Optional[int] = None) -> dict | None:
    """Return a random ayah dict from the local corpus."""
    _corpus._ensure_loaded()
    ayahs = _corpus._ayahs
    if not ayahs:
        return None
    if surah_id is not None:
        candidates = [a for a in ayahs if a.surah_number == surah_id]
        if not candidates:
            return None
    else:
        candidates = list(ayahs)
    return random.choice(candidates).to_dict()


async def get_ayah_by_index(index: int) -> dict | None:
    """Return the ayah at position *index* (0-based) in the local corpus."""
    _corpus._ensure_loaded()
    ayahs = _corpus._ayahs
    if not ayahs or index < 0 or index >= len(ayahs):
        return None
    return ayahs[index].to_dict()


# ── External API helpers (AlQuran.cloud) ─────────────────────────────────────

async def get_ayah(surah: int, verse: int) -> dict | None:
    """Fetch a single ayah from AlQuran.cloud API."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{_BASE_URL}/ayah/{surah}:{verse}/ar.uthmani")
            if resp.status_code != 200:
                return None
            data = resp.json().get("data", {})
            return {
                "surah_id": data["surah"]["number"],
                "ayah_number": data["numberInSurah"],
                "surah_name": data["surah"]["englishName"],
                "text_uthmani": data["text"],
            }
    except Exception:
        return None


async def get_surah(surah_number: int) -> dict | None:
    """Fetch a full surah (with ayahs) from AlQuran.cloud API."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{_BASE_URL}/surah/{surah_number}/ar.uthmani"
            )
            if resp.status_code != 200:
                return None
            data = resp.json().get("data", {})
            return {
                "info": {
                    "id": data["number"],
                    "name_ar": data["name"],
                    "name_en": data["englishName"],
                    "revelation_type": data.get("revelationType", "").lower(),
                    "ayah_count": data["numberOfAyahs"],
                },
                "ayahs": [
                    {
                        "surah_id": surah_number,
                        "ayah_number": a["numberInSurah"],
                        "text_uthmani": a["text"],
                    }
                    for a in data.get("ayahs", [])
                ],
            }
    except Exception:
        return None


async def get_surah_list() -> list:
    """Fetch the full list of surahs from AlQuran.cloud API."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{_BASE_URL}/surah")
            if resp.status_code != 200:
                return []
            items = resp.json().get("data", [])
            return [
                {
                    "id": s["number"],
                    "name_ar": s["name"],
                    "name_en": s["englishName"],
                    "ayah_count": s["numberOfAyahs"],
                    "revelation_type": s.get("revelationType", "").lower(),
                }
                for s in items
            ]
    except Exception:
        return []


async def search_ayahs(query: str) -> list:
    """Search ayahs via AlQuran.cloud API (max 10 results)."""
    try:
        encoded = urllib.parse.quote(query, safe="")
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{_BASE_URL}/search/{encoded}/all/ar")
            if resp.status_code != 200:
                return []
            matches = resp.json().get("data", {}).get("matches", [])
            return [
                {
                    "surah_id": m["surah"]["number"],
                    "ayah_number": m["numberInSurah"],
                    "surah_name": m["surah"]["englishName"],
                    "text_uthmani": m["text"],
                }
                for m in matches[:10]
            ]
    except Exception:
        return []
