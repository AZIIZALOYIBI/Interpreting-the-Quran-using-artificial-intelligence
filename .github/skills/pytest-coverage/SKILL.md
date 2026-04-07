---
name: pytest-coverage
description: دليل لكتابة وتشغيل اختبارات Python باستخدام pytest مع قياس تغطية الكود في هذا المستودع. استخدمه عند طلب إضافة اختبارات أو تحسين تغطية الكود.
---

# كتابة اختبارات Python مع pytest وقياس التغطية

## هيكل الاختبارات في هذا المستودع

```
backend/
├── tests/
│   ├── __init__.py
│   ├── test_routers/      # اختبارات API endpoints
│   ├── test_services/     # اختبارات business logic
│   └── conftest.py        # fixtures مشتركة
```

## تشغيل الاختبارات

```bash
cd backend

# تشغيل جميع الاختبارات
python -m pytest

# مع قياس التغطية
python -m pytest --cov=. --cov-report=term-missing

# تقرير HTML للتغطية
python -m pytest --cov=. --cov-report=html
```

## كتابة اختبارات لـ FastAPI

### مثال على اختبار endpoint:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ask_quran_demo_mode():
    response = client.post("/api/ask-quran", json={
        "question": "كيف يرشدنا القرآن في موضوع الصحة؟",
        "category": "medicine"
    })
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "verses" in data

def test_get_categories():
    response = client.get("/api/categories")
    assert response.status_code == 200
    categories = response.json()
    assert len(categories) > 0

def test_search_verses():
    response = client.get("/api/quran/search?q=الصبر")
    assert response.status_code == 200
```

### اختبار الـ AI Engine:

```python
import pytest
from unittest.mock import patch, MagicMock

def test_quran_solver_demo_mode():
    from ai_engine.quran_solver import QuranSolver
    solver = QuranSolver(demo_mode=True)
    result = solver.solve("ما حكم الصبر؟", category="general")
    assert result is not None
    assert "verses" in result
```

## نسبة التغطية المستهدفة

- الـ Routers: 80%+
- الـ Services: 70%+
- الـ Models: 90%+

## الإضافات المطلوبة في requirements.txt

```
pytest>=7.4.0
pytest-cov>=4.1.0
httpx>=0.24.0        # مطلوب لـ TestClient في FastAPI الحديثة
pytest-asyncio>=0.21.0
```
