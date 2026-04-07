from fastapi import APIRouter, HTTPException
from schemas.chat import ChatRequest, ChatResponse
from services import ai_service
from data.categories import CATEGORIES
from data.sample_ayahs import SAMPLE_AYAHS

router = APIRouter(prefix="/api", tags=["chat"])

DISCLAIMER = "هذه الإجابة للتوجيه العام فقط. يُرجى الرجوع إلى العلماء المتخصصين في المسائل الدينية الدقيقة."


@router.post("/ask-quran", response_model=ChatResponse)
async def ask_quran(request: ChatRequest):
    result = await ai_service.get_quran_solution(request.question, request.category)
    ayahs = result.get("ayahs", [])
    return ChatResponse(
        answer=result.get("answer", ""),
        category=result.get("category", "general"),
        ayahs=ayahs,
        practical_steps=result.get("practical_steps", []),
        disclaimer=DISCLAIMER,
    )


@router.get("/categories")
def get_categories():
    return CATEGORIES


@router.get("/categories/{category_id}")
def get_category(category_id: str):
    category = next((c for c in CATEGORIES if c["id"] == category_id), None)
    if not category:
        raise HTTPException(status_code=404, detail="التصنيف غير موجود")
    ayahs = SAMPLE_AYAHS.get(category_id, [])
    return {"category": category, "ayahs": ayahs}
