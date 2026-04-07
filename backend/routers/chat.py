import logging
import time
from collections import defaultdict, deque
from typing import Deque

from fastapi import APIRouter, HTTPException, Request

from data.categories import CATEGORIES
from data.sample_ayahs import SAMPLE_AYAHS
from schemas.chat import ChatRequest, ChatResponse
from services import ai_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])

DISCLAIMER = "هذه الإجابة للتوجيه العام فقط. يُرجى الرجوع إلى العلماء المتخصصين في المسائل الدينية الدقيقة."

# ---------------------------------------------------------------------------
# Simple in-memory rate limiter: max 20 requests per minute per IP
# ---------------------------------------------------------------------------
_RATE_LIMIT_MAX = 20
_RATE_LIMIT_WINDOW = 60  # seconds
_ip_request_times: dict[str, Deque[float]] = defaultdict(deque)


def _check_rate_limit(ip: str) -> None:
    """Raise HTTP 429 if the IP has exceeded the rate limit."""
    now = time.time()
    window_start = now - _RATE_LIMIT_WINDOW
    times = _ip_request_times[ip]

    # Remove timestamps outside the current window
    while times and times[0] < window_start:
        times.popleft()

    if len(times) >= _RATE_LIMIT_MAX:
        logger.warning("Rate limit exceeded for IP: %s", ip)
        raise HTTPException(
            status_code=429,
            detail="لقد تجاوزت الحد المسموح به من الطلبات. يرجى الانتظار دقيقة والمحاولة مجدداً.",
        )

    times.append(now)


def reset_rate_limiter_for_testing() -> None:
    """Clear all in-memory rate-limit state.  Intended for use in tests only."""
    _ip_request_times.clear()


@router.post("/ask-quran", response_model=ChatResponse)
async def ask_quran(request: ChatRequest, req: Request) -> ChatResponse:
    """Handle a Quranic guidance request with rate limiting."""
    client_ip = req.client.host if req.client else "unknown"
    _check_rate_limit(client_ip)

    logger.info(
        "ask-quran request from %s | category=%s | question_len=%d",
        client_ip,
        request.category,
        len(request.question),
    )

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
def get_categories() -> list:
    """Return the list of all available categories."""
    return CATEGORIES


@router.get("/categories/{category_id}")
def get_category(category_id: str) -> dict:
    """Return category details along with sample ayahs."""
    category = next((c for c in CATEGORIES if c["id"] == category_id), None)
    if not category:
        raise HTTPException(status_code=404, detail="التصنيف غير موجود")
    ayahs = SAMPLE_AYAHS.get(category_id, [])
    return {"category": category, "ayahs": ayahs}
