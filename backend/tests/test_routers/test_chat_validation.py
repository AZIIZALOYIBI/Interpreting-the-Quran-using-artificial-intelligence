"""
اختبارات التحقق من صحة مدخلات ChatRequest وسلوك نقطة نهاية /api/ask-quran.
"""
import pytest


class TestChatRequestValidation:
    def test_ask_quran_question_too_short(self, client):
        """السؤال القصير جداً (أقل من 5 أحرف) يُعيد 422."""
        response = client.post("/api/ask-quran", json={"question": "ما"})
        assert response.status_code == 422

    def test_ask_quran_question_too_long(self, client):
        """السؤال الطويل جداً (أكثر من 2000 حرف) يُعيد 422."""
        response = client.post("/api/ask-quran", json={"question": "أ" * 2001})
        assert response.status_code == 422

    def test_ask_quran_empty_question(self, client):
        """السؤال الفارغ يُعيد 422."""
        response = client.post("/api/ask-quran", json={"question": ""})
        assert response.status_code == 422

    def test_ask_quran_invalid_category(self, client):
        """فئة غير موجودة يُعيد 422."""
        response = client.post(
            "/api/ask-quran",
            json={"question": "ما إرشاد القرآن في الصحة؟", "category": "invalid_cat"},
        )
        assert response.status_code == 422

    def test_ask_quran_valid_category(self, client):
        """الفئات الصحيحة تُقبل بدون خطأ."""
        valid_categories = [
            "medicine", "work", "science", "family",
            "self_development", "law", "environment", "ethics", "general",
        ]
        for cat in valid_categories:
            response = client.post(
                "/api/ask-quran",
                json={"question": "ما إرشاد القرآن في هذا الموضوع؟", "category": cat},
            )
            assert response.status_code == 200, f"فشل للفئة: {cat}"

    def test_ask_quran_no_category(self, client):
        """إرسال بدون فئة يعمل بشكل صحيح (تصنيف تلقائي)."""
        response = client.post(
            "/api/ask-quran",
            json={"question": "ما هو إرشاد القرآن الكريم في الأمور العامة؟"},
        )
        assert response.status_code == 200

    def test_ask_quran_boundary_min_length(self, client):
        """السؤال بطول 5 أحرف مقبول (الحد الأدنى)."""
        response = client.post("/api/ask-quran", json={"question": "الصبر"})
        assert response.status_code == 200

    def test_ask_quran_boundary_max_length(self, client):
        """السؤال بطول 2000 حرف مقبول (الحد الأقصى)."""
        response = client.post("/api/ask-quran", json={"question": "أ" * 2000})
        assert response.status_code == 200

    def test_ask_quran_response_has_disclaimer(self, client):
        """الاستجابة الناجحة تحتوي على إخلاء المسؤولية."""
        response = client.post(
            "/api/ask-quran",
            json={"question": "ما إرشاد القرآن في الصحة والعلاج؟", "category": "medicine"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "disclaimer" in data
        assert len(data["disclaimer"]) > 0

    def test_ask_quran_response_structure(self, client):
        """الاستجابة تحتوي على جميع الحقول المطلوبة."""
        response = client.post(
            "/api/ask-quran",
            json={"question": "كيف يرشدنا القرآن في العمل والرزق؟", "category": "work"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "category" in data
        assert "ayahs" in data
        assert "practical_steps" in data
        assert "disclaimer" in data
        assert data["category"] == "work"
