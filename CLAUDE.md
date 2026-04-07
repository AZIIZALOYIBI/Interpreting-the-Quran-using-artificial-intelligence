# CLAUDE.md — منصة حلول الحياة من القرآن الكريم

## نظرة عامة على المشروع

منصة ذكاء اصطناعي لتفسير القرآن الكريم وتقديم الإرشاد القرآني بالعربية، تعمل في وضع Demo بدون مفاتيح API.

## هيكل المشروع

```
.
├── frontend/          # Next.js 14 + TypeScript + Tailwind CSS (RTL عربي)
│   └── src/
│       ├── app/       # صفحات التطبيق (ask, categories, reader, miracles)
│       ├── components/# مكونات UI (AskQuranChat, QuranReader, Header…)
│       ├── lib/       # api.ts — استدعاءات HTTP للـ Backend
│       └── types/     # TypeScript type definitions
├── backend/           # Python FastAPI
│   ├── routers/       # quran, tafsir, chat, miracles
│   ├── services/      # ai_service, quran_service, tafsir_service
│   ├── schemas/       # Pydantic models (ayah, category, chat, tafsir)
│   ├── data/          # بيانات ثابتة (categories, sample_ayahs, scientific_miracles)
│   ├── models/        # SQLAlchemy ORM models
│   └── tests/         # pytest tests (68 tests, 79% coverage)
├── ai-engine/         # LangChain + OpenAI RAG pipeline
│   ├── quran_solver.py
│   ├── prompts/       # domain-specific prompts per category
│   └── data/          # miracle maps
└── database/          # PostgreSQL schema
```

## أوامر التطوير

### Backend
```bash
cd backend && pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend && npm install && npm run dev
```

### الاختبارات
```bash
make test           # تشغيل جميع اختبارات الـ Backend
make test-cov       # مع تقرير التغطية
cd backend && python3 -m pytest tests/ -v
cd backend && python3 -m pytest tests/ --cov=. --cov-report=term-missing
```

### Docker
```bash
make setup   # نسخ .env.example → .env
make build   # بناء الصور
make up      # تشغيل جميع الخدمات
make down    # إيقاف الخدمات
```

## الفئات المدعومة

| ID | العربية | English |
|----|---------|---------|
| `medicine` | الطب والصحة | Medicine & Health |
| `work` | العمل والمال | Work & Finance |
| `science` | العلوم والتكنولوجيا | Science & Technology |
| `family` | الأسرة والمجتمع | Family & Society |
| `self_development` | التطوير الذاتي | Self Development |
| `law` | القانون والشريعة | Law & Sharia |
| `environment` | البيئة والطبيعة | Environment & Nature |
| `ethics` | الأخلاق والقيم | Ethics & Values |
| `general` | عام | General |

## نقاط النهاية الرئيسية

| Method | Path | الوصف |
|--------|------|-------|
| POST | `/api/ask-quran` | السؤال القرآني (الميزة الرئيسية) |
| GET | `/api/categories` | قائمة الفئات |
| GET | `/api/categories/{id}` | تفاصيل فئة مع آياتها |
| GET | `/api/quran/surahs` | قائمة السور |
| GET | `/api/quran/surah/{id}` | سورة كاملة |
| GET | `/api/quran/search?q=...` | بحث في الآيات |
| GET | `/api/tafsir/{ayah_id}` | التفسير |
| GET | `/api/miracles` | المعجزات العلمية |
| GET | `/health` | فحص الصحة |

## وضع Demo

التطبيق يعمل بدون مفاتيح API. عند وجود `OPENAI_API_KEY` في `.env`، يستخدم GPT-3.5-turbo. في غير ذلك، يعود إلى ردود محضّرة مسبقاً.

## الأمان

- التحقق من المدخلات: `question` يجب أن يكون بين 5 و2000 حرف
- الفئات مقيّدة بقائمة معروفة مسبقاً
- CORS مضبوط عبر متغير `CORS_ORIGINS`
- جميع مفاتيح API تُحمَّل من متغيرات البيئة فقط

## إضافة فئة جديدة

1. `backend/data/categories.py` — أضف قاموس الفئة
2. `backend/services/ai_service.py` — أضف كلمات المفتاح في `CATEGORY_KEYWORDS` وردًّا في `MOCK_RESPONSES`
3. `backend/data/sample_ayahs.py` — أضف آيات نموذجية
4. `ai-engine/prompts/` — أنشئ ملف `{category}.txt`
5. `frontend/src/app/page.tsx` — أضف بطاقة الفئة
6. `frontend/src/components/AskQuranChat.tsx` — أضف الفئة في `CATEGORY_LABELS`
