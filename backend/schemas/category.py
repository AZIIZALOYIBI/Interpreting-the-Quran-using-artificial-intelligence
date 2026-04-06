from pydantic import BaseModel
from typing import Optional


class CategorySchema(BaseModel):
    id: str
    name_ar: str
    name_en: str
    icon: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    bg_color: Optional[str] = None
    text_color: Optional[str] = None

    class Config:
        from_attributes = True
