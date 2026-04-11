"""Ask Quran Router — AI-powered Quranic guidance endpoint."""

from fastapi import APIRouter
from schemas.schemas import AskQuranRequest, AskQuranResponse
from services.ai_service import get_ai_response

router = APIRouter()


@router.post("/ask-quran", response_model=AskQuranResponse)
async def ask_quran(request: AskQuranRequest):
    result = await get_ai_response(
        question=request.question,
        category=request.category or "general",
    )
    return AskQuranResponse(**result)
