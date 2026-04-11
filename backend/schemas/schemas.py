"""Pydantic schemas for request and response models."""

from typing import Optional
from pydantic import BaseModel, Field


class AskQuranRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500, description="السؤال باللغة العربية")
    category: Optional[str] = Field("general", description="فئة السؤال")


class QuranVerseSchema(BaseModel):
    id: int
    surah_number: int
    surah_name: str
    surah_name_en: str
    ayah_number: int
    text_uthmani: str
    text_simple: str
    translation: Optional[str] = None
    juz_number: int
    hizb_number: int
    page_number: int


class AskQuranResponse(BaseModel):
    answer: str
    verses: list[QuranVerseSchema]
    category: str
    confidence: float
    related_topics: list[str]
    tafsir_notes: list[str]


class SearchResponse(BaseModel):
    verses: list[QuranVerseSchema]
    total_count: int
    query: str
    suggestions: list[str]


class CategorySchema(BaseModel):
    id: str
    name: str
    name_en: str
    icon: str
    description: str
    color: str
    verse_count: int


class MiracleSchema(BaseModel):
    id: int
    title: str
    description: str
    scientific_fact: str
    quran_reference: str
    verse_text: str
    surah_name: str
    ayah_number: int
    category: str
    discovery_year: Optional[str] = None


class TafsirSchema(BaseModel):
    id: int
    verse_id: int
    scholar_name: str
    scholar_name_en: str
    tafsir_text: str
    source: str
    era: str


class SurahSchema(BaseModel):
    number: int
    name: str
    name_en: str
    name_translation: str
    revelation_type: str
    ayah_count: int
