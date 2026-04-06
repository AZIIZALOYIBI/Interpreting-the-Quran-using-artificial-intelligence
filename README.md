<div dir="rtl">

# 📖 حلول الحياة من القرآن الكريم بالذكاء الاصطناعي

منصة ذكية تساعدك في إيجاد الإرشاد والتوجيه القرآني لأي موضوع في حياتك

</div>

---

## 🌟 Life Solutions from the Holy Quran — AI Platform

An intelligent platform that helps you find Quranic guidance for any topic in your life, using Artificial Intelligence and Natural Language Processing.

---

## ✨ Features

- 🤖 **AI-powered Q&A** — Ask any question in Arabic and get Quranic guidance
- 📖 **Quran Reader** — Browse the Quran in Uthmani script with beautiful typography
- 🔬 **Scientific Miracles** — Explore scientific facts mentioned in the Quran
- 🗂️ **8 Life Categories** — Medicine, Work, Science, Family, Self-Development, Law, Environment, General
- 📝 **Tafsir Panel** — Multiple scholar interpretations for each verse
- 🔍 **Smart Search** — Search through Quran verses by keywords
- 🌐 **RTL Arabic UI** — Full Arabic right-to-left interface

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS |
| Backend | Python FastAPI |
| AI Engine | LangChain, OpenAI GPT |
| Database | PostgreSQL |
| Cache | Redis |
| Vector DB | Pinecone |
| Container | Docker & Docker Compose |

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose (optional)

### Option 1: With Docker (Recommended)

```bash
# Clone the repository
git clone <repo-url>
cd Interpreting-the-Quran-using-artificial-intelligence

# Setup environment file, then edit .env and add your API keys
make setup

# Build all Docker images
make build

# Start all services
make up
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

Useful commands:
```bash
make logs    # stream logs from all services
make ps      # show container status
make down    # stop all services
make clean   # stop and delete all data
make help    # show all available commands
```

### Option 2: Local Development

#### Frontend
```bash
cd frontend
npm install
npm run dev
# Access at http://localhost:3000
```

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start without database (demo mode)
uvicorn main:app --reload --port 8000
```

---

## 🔑 Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI responses | Optional (demo mode without it) |
| `PINECONE_API_KEY` | Pinecone vector database key | Optional |
| `POSTGRES_*` | PostgreSQL credentials | Optional (in-memory demo) |
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes |

> **Note**: The platform works in **demo mode** without any API keys — it returns pre-defined example responses.

---

## 📡 API Documentation

### Ask Quran
```http
POST /api/ask-quran
Content-Type: application/json

{
  "question": "كيف يرشدنا القرآن في موضوع الصحة؟",
  "category": "medicine"
}
```

### Search Verses
```http
GET /api/quran/search?q=الصبر
```

### Get Categories
```http
GET /api/categories
```

### Get Scientific Miracles
```http
GET /api/miracles
```

Full API docs available at `/docs` when backend is running.

---

## 📁 Project Structure

```
.
├── frontend/          # Next.js 14 + TypeScript + Tailwind CSS
│   └── src/
│       ├── app/       # App router pages
│       ├── components/ # React components
│       ├── lib/       # API client
│       └── types/     # TypeScript interfaces
├── backend/           # Python FastAPI
│   ├── routers/      # API route handlers
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   └── data/         # Static data
├── ai-engine/         # AI/RAG pipeline
│   ├── quran_solver.py
│   ├── worker.py
│   ├── prompts/      # Domain-specific prompts
│   └── data/         # Miracle maps
├── database/          # SQL schema & seed data
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## ⚠️ Disclaimer

> هذه المنصة مخصصة للتوجيه العام والاستئناس فقط، وليست بديلاً عن الفتاوى الشرعية المعتمدة من العلماء المتخصصين. يُرجى الرجوع إلى أهل العلم الموثوقين في المسائل الدينية الدقيقة.

> This platform is intended for general guidance only and is not a substitute for authoritative religious rulings from qualified scholars. Please consult certified Islamic scholars for precise religious matters.

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.
