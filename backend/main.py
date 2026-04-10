import logging
import time
from contextlib import asynccontextmanager
from typing import Any, Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings
from routers import chat, miracles, quran, tafsir, upload

logger = logging.getLogger(__name__)

# Application start time for uptime calculation
_START_TIME: float = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and graceful shutdown."""
    global _START_TIME
    _START_TIME = time.time()
    logger.info("Starting Quran AI Platform API")
    yield
    logger.info("Shutting down Quran AI Platform API")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add OWASP-recommended security headers to every response."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
        return response


app = FastAPI(
    title="حلول الحياة من القرآن الكريم API",
    description="API منصة الإرشاد القرآني بالذكاء الاصطناعي",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quran.router)
app.include_router(tafsir.router)
app.include_router(chat.router)
app.include_router(miracles.router)
app.include_router(upload.router)


# ---------------------------------------------------------------------------
# Global error handlers
# ---------------------------------------------------------------------------


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.warning("404 Not Found: %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=404,
        content={"detail": "المورد المطلوب غير موجود", "path": request.url.path},
    )


@app.exception_handler(422)
async def validation_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.warning("422 Validation Error: %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=422,
        content={"detail": "بيانات الطلب غير صحيحة. يرجى مراجعة المدخلات."},
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "500 Internal Server Error: %s %s — %s",
        request.method,
        request.url.path,
        exc,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "حدث خطأ داخلي في الخادم. يرجى المحاولة لاحقاً."},
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "مرحباً بك في API منصة حلول الحياة من القرآن الكريم",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, Any]:
    """Enhanced health check with uptime and basic memory info."""
    uptime_seconds = time.time() - _START_TIME

    memory_info: dict[str, Any] = {}
    try:
        with open("/proc/meminfo", encoding="utf-8") as f:
            lines = f.readlines()
        meminfo: dict[str, int] = {}
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0].rstrip(":")
                meminfo[key] = int(parts[1])
        total_mb = meminfo.get("MemTotal", 0) // 1024
        available_mb = meminfo.get("MemAvailable", 0) // 1024
        used_mb = total_mb - available_mb
        memory_info = {
            "total_mb": total_mb,
            "used_mb": used_mb,
            "available_mb": available_mb,
        }
    except (OSError, ValueError):
        memory_info = {"error": "unavailable"}

    return {
        "status": "healthy",
        "uptime_seconds": round(uptime_seconds, 2),
        "memory": memory_info,
        "dependencies": {
            "ai_service": "ok",
            "data": "ok",
        },
    }
