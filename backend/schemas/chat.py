from pydantic import BaseModel
from typing import List, Optional
from .ayah import AyahSchema


class ChatRequest(BaseModel):
    question: str
    category: Optional[str] = None
    language: Optional[str] = "ar"


class ChatResponse(BaseModel):
    answer: str
    category: str
    ayahs: List[AyahSchema]
    practical_steps: List[str]
    disclaimer: str
