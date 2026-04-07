from pydantic import BaseModel, ConfigDict
from typing import Optional


class AyahCreate(BaseModel):
    surah_id: int
    ayah_number: int
    text_uthmani: str
    text_simple: str
    surah_name: Optional[str] = None
    surah_name_ar: Optional[str] = None


class AyahSchema(AyahCreate):
    id: int
    tafsir: Optional[str] = None
    relevance_score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
