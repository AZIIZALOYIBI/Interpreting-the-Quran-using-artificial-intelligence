"""Tafsir Router — Endpoints for Quran interpretations."""

from typing import Optional
from fastapi import APIRouter
from services.tafsir_service import get_tafsir, get_available_scholars

router = APIRouter()


@router.get("/tafsir/scholars")
def list_scholars():
    return get_available_scholars()


@router.get("/tafsir/{ayah_id}")
def get_tafsir_for_ayah(ayah_id: int, scholar: Optional[str] = None):
    return get_tafsir(ayah_id, scholar or "all")
