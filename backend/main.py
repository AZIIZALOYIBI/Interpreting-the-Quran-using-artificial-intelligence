from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import quran, tafsir, chat, miracles

app = FastAPI(
    title="حلول الحياة من القرآن الكريم API",
    description="API منصة الإرشاد القرآني بالذكاء الاصطناعي",
    version="1.0.0",
)

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


@app.get("/")
def root():
    return {
        "message": "مرحباً بك في API منصة حلول الحياة من القرآن الكريم",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
