"""Miracles Router — Endpoints for scientific miracles in the Quran."""

from fastapi import APIRouter
from data.miracles_data import MIRACLES

router = APIRouter()


@router.get("/miracles")
async def get_miracles():
    return MIRACLES


@router.get("/miracles/{miracle_id}")
async def get_miracle(miracle_id: int):
    for miracle in MIRACLES:
        if miracle["id"] == miracle_id:
            return miracle
    return {"error": "لم يتم العثور على المعجزة"}
