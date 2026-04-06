from fastapi import APIRouter
from services import tafsir_service

router = APIRouter(prefix="/api/tafsir", tags=["tafsir"])


@router.get("/scholars")
def get_scholars():
    return tafsir_service.get_available_scholars()


@router.get("/{ayah_id}")
def get_tafsir(ayah_id: int, scholar: str = "all"):
    return tafsir_service.get_tafsir(ayah_id, scholar)
