"""
📖 حلول الحياة من القرآن الكريم — واجهة برمجة التطبيقات الخلفية
Quran Life Solutions — Backend API
"""

import os
import time
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from routers import quran, miracles, tafsir
from routers import chat as chat_router
from routers import upload

load_dotenv()

_start_time = time.time()


def _ai_mode() -> str:
    if os.getenv("VLLM_BASE_URL"):
        return "vllm"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("GPTQ_MODEL_PATH"):
        return "gptq"
    return "demo"


@asynccontextmanager
async def lifespan(app: FastAPI):
    mode = _ai_mode().upper()
    print(f"🚀 Starting Quran Life Solutions API — AI mode: {mode}")
    yield
    print("👋 Shutting down Quran Life Solutions API...")


# ---------------------------------------------------------------------------
# Security headers middleware
# ---------------------------------------------------------------------------

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        return response


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title="حلول الحياة من القرآن الكريم — API",
    description="منصة ذكية تساعدك في العثور على إرشادات قرآنية لأي موضوع في حياتك باستخدام الذكاء الاصطناعي",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Custom error handlers
# ---------------------------------------------------------------------------

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    detail = exc.detail
    if exc.status_code == 404 and detail == "Not Found":
        detail = "المورد المطلوب غير موجود"
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": detail, "path": str(request.url.path)},
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(chat_router.router)                         # /api/ask-quran, /api/categories, /api/categories/{id}
app.include_router(quran.router, prefix="/api/quran", tags=["القرآن الكريم"])
app.include_router(miracles.router, prefix="/api", tags=["المعجزات العلمية"])
app.include_router(tafsir.router, prefix="/api", tags=["التفسير"])
app.include_router(upload.router)                              # /api/upload-pdf


# ---------------------------------------------------------------------------
# Root & health endpoints
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "message": "حلول الحياة من القرآن الكريم — API",
        "version": "2.0.0",
        "status": "running",
        "ai_mode": _ai_mode(),
        "docs": "/docs",
    }


def _get_memory_info() -> dict:
    try:
        import psutil
        m = psutil.virtual_memory()
        return {
            "total_mb": m.total // (1024 * 1024),
            "available_mb": m.available // (1024 * 1024),
            "percent": m.percent,
        }
    except Exception:
        return {}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_mode": _ai_mode(),
        "uptime_seconds": time.time() - _start_time,
        "memory": _get_memory_info(),
        "dependencies": {
            "ai_service": "ok",
            "data": "ok",
        },
    }
