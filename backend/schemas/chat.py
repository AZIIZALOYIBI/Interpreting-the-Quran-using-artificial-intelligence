from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .ayah import AyahSchema

VALID_CATEGORIES = {
    "medicine", "work", "science", "family", "self_development",
    "law", "environment", "ethics", "general",
}


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=2000)
    category: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default="ar")

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_CATEGORIES:
            raise ValueError(f"الفئة غير مدعومة. الفئات المتاحة: {', '.join(sorted(VALID_CATEGORIES))}")
        return v


class ChatResponse(BaseModel):
    answer: str
    category: str
    ayahs: List[AyahSchema]
    practical_steps: List[str]
    disclaimer: str
