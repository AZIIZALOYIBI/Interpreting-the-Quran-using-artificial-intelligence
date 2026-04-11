"""
📖 حلول الحياة من القرآن الكريم — واجهة برمجة التطبيقات الخلفية
Quran Life Solutions — Backend API
"""

import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import quran, ask, categories, miracles, tafsir

load_dotenv()

DEMO_MODE = not os.getenv("OPENAI_API_KEY")


@asynccontextmanager
async def lifespan(app: FastAPI):
    mode = "DEMO" if DEMO_MODE else "PRODUCTION"
    print(f"🚀 Starting Quran Life Solutions API in {mode} mode...")
    yield
    print("👋 Shutting down Quran Life Solutions API...")


app = FastAPI(
    title="حلول الحياة من القرآن الكريم — API",
    description="منصة ذكية تساعدك في العثور على إرشادات قرآنية لأي موضوع في حياتك باستخدام الذكاء الاصطناعي",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quran.router, prefix="/api/quran", tags=["القرآن الكريم"])
app.include_router(ask.router, prefix="/api", tags=["اسأل القرآن"])
app.include_router(categories.router, prefix="/api", tags=["الفئات"])
app.include_router(miracles.router, prefix="/api", tags=["المعجزات العلمية"])
app.include_router(tafsir.router, prefix="/api", tags=["التفسير"])


@app.get("/")
async def root():
    return {
        "name": "حلول الحياة من القرآن الكريم — API",
        "version": "1.0.0",
        "status": "running",
        "mode": "demo" if DEMO_MODE else "production",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "demo" if DEMO_MODE else "production"}
