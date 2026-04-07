.PHONY: help build up down logs ps clean dev-frontend dev-backend dev-ai test test-cov

# Default target
help:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════╗"
	@echo "║   حلول الحياة من القرآن الكريم — أوامر البناء والنشر  ║"
	@echo "╚══════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  make setup        — نسخ ملف البيئة وإعداد المشروع"
	@echo "  make build        — بناء جميع صور Docker"
	@echo "  make up           — تشغيل جميع الخدمات"
	@echo "  make down         — إيقاف جميع الخدمات"
	@echo "  make restart      — إعادة تشغيل جميع الخدمات"
	@echo "  make logs         — عرض السجلات"
	@echo "  make ps           — حالة الحاويات"
	@echo "  make clean        — حذف الحاويات والبيانات"
	@echo "  make dev-frontend — تشغيل الواجهة الأمامية محلياً"
	@echo "  make dev-backend  — تشغيل الخادم الخلفي محلياً"
	@echo "  make test          — تشغيل اختبارات الـ Backend"
	@echo "  make test-cov      — تشغيل الاختبارات مع تقرير التغطية"
	@echo ""

# ── Initial setup ────────────────────────────────────────────────────────────

setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ تم إنشاء ملف .env — يرجى تعديله وإضافة مفاتيح API قبل التشغيل."; \
	else \
		echo "ℹ️  ملف .env موجود بالفعل."; \
	fi

# ── Docker commands ───────────────────────────────────────────────────────────

build:
	docker compose build --parallel

up: setup
	docker compose up -d
	@echo ""
	@echo "✅ الموقع يعمل على:"
	@echo "   🌐 الواجهة الأمامية : http://localhost:3000"
	@echo "   🔌 API الخادم       : http://localhost:8000"
	@echo "   📚 توثيق API        : http://localhost:8000/docs"
	@echo ""

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

logs-backend:
	docker compose logs -f backend

logs-frontend:
	docker compose logs -f frontend

ps:
	docker compose ps

# ── Cleanup ───────────────────────────────────────────────────────────────────

clean:
	docker compose down -v --remove-orphans
	@echo "✅ تم حذف الحاويات والبيانات."

clean-images:
	docker compose down --rmi all -v --remove-orphans

# ── Local development (without Docker) ───────────────────────────────────────

dev-frontend:
	cd frontend && npm install && npm run dev

dev-backend:
	cd backend && pip install -r requirements.txt && uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-ai:
	cd ai-engine && pip install -r requirements.txt && python worker.py

# ── Tests ─────────────────────────────────────────────────────────────────────

test:
	cd backend && python -m pytest tests/ -v

test-cov:
	cd backend && python -m pytest tests/ --cov=. --cov-report=term-missing

# ── Database ──────────────────────────────────────────────────────────────────

db-shell:
	docker compose exec db psql -U $${POSTGRES_USER:-quran_user} -d $${POSTGRES_DB:-quran_ai}

db-reset:
	docker compose down -v db
	docker compose up -d db
