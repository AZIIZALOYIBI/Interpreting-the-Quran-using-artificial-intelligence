from pydantic import BaseModel, ConfigDict
from typing import Optional


class TafsirCreate(BaseModel):
    ayah_id: int
    scholar_name: Optional[str] = None
    scholar_name_ar: Optional[str] = None
    text: str
    source: Optional[str] = None


class TafsirSchema(TafsirCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
