"""Quran Service — Handles Quran data operations."""

from data.quran_data import QURAN_VERSES, SURAHS


def get_all_surahs() -> list:
    return SURAHS


def get_surah_verses(surah_number: int) -> list:
    return [v for v in QURAN_VERSES if v["surah_number"] == surah_number]


def get_verse(surah_number: int, ayah_number: int) -> dict | None:
    for v in QURAN_VERSES:
        if v["surah_number"] == surah_number and v["ayah_number"] == ayah_number:
            return v
    return None
