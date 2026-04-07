"""
اختبارات نقطة نهاية /api/ask-quran والفئات.
"""
import pytest


class TestAskQuran:
    def test_ask_quran_medicine(self, client):
        response = client.post("/api/ask-quran", json={
            "question": "ما إرشاد القرآن في موضوع الصحة والطب؟",
            "category": "medicine",
        })
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "ayahs" in data
        assert "practical_steps" in data
        assert "disclaimer" in data
        assert data["category"] == "medicine"

    def test_ask_quran_work(self, client):
        response = client.post("/api/ask-quran", json={
            "question": "كيف يرشدنا القرآن في الكسب الحلال؟",
            "category": "work",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "work"
        assert len(data["answer"]) > 0

    def test_ask_quran_science(self, client):
        response = client.post("/api/ask-quran", json={
            "question": "كيف يحث الإسلام على طلب العلم؟",
            "category": "science",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "science"

    def test_ask_quran_family(self, client):
        response = client.post("/api/ask-quran", json={
            "question": "ما دور الأسرة في الإسلام؟",
            "category": "family",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "family"

    def test_ask_quran_law(self, client):
        response = client.post("/api/ask-quran", json={
            "question": "ما موقف الإسلام من العدل؟",
            "category": "law",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "law"

    def test_ask_quran_environment(self, client):
        response = client.post("/api/ask-quran", json={
            "question": "كيف يأمر الإسلام بحماية البيئة؟",
            "category": "environment",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "environment"

    def test_ask_quran_ethics(self, client):
        response = client.post("/api/ask-quran", json={
            "question": "ما أهمية الأخلاق الحسنة في الإسلام؟",
            "category": "ethics",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "ethics"

    def test_ask_quran_self_development(self, client):
        response = client.post("/api/ask-quran", json={
            "question": "كيف أتغلب على الضغوط النفسية؟",
            "category": "self_development",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "self_development"

    def test_ask_quran_auto_classify(self, client):
        """يجب أن يُصنَّف السؤال تلقائياً عند غياب الفئة."""
        response = client.post("/api/ask-quran", json={
            "question": "كيف يرشدنا الإسلام في موضوع الصحة والعلاج؟",
        })
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert data["category"] == "medicine"

    def test_ask_quran_arabic_content(self, client):
        """يجب أن تحتوي الإجابة على محتوى عربي."""
        response = client.post("/api/ask-quran", json={
            "question": "ما معنى الصبر في القرآن؟",
        })
        assert response.status_code == 200
        data = response.json()
        # التحقق من وجود حرف عربي في الإجابة
        assert any(ord(c) > 0x0600 for c in data["answer"])

    def test_ask_quran_has_disclaimer(self, client):
        """يجب أن تتضمن الاستجابة تنبيهاً قانونياً."""
        response = client.post("/api/ask-quran", json={
            "question": "ما هو الصبر؟",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["disclaimer"] != ""

    def test_ask_quran_practical_steps_list(self, client):
        """يجب أن تكون الخطوات العملية قائمة."""
        response = client.post("/api/ask-quran", json={
            "question": "كيف أحافظ على صحتي؟",
            "category": "medicine",
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["practical_steps"], list)


class TestCategories:
    def test_get_categories(self, client):
        response = client.get("/api/categories")
        assert response.status_code == 200
        categories = response.json()
        assert isinstance(categories, list)
        assert len(categories) > 0

    def test_categories_have_required_fields(self, client):
        response = client.get("/api/categories")
        categories = response.json()
        for cat in categories:
            assert "id" in cat
            assert "name_ar" in cat
            assert "icon" in cat

    def test_known_categories_present(self, client):
        response = client.get("/api/categories")
        categories = response.json()
        ids = [c["id"] for c in categories]
        for expected in ["medicine", "work", "science", "family", "law", "environment", "ethics", "self_development"]:
            assert expected in ids, f"الفئة '{expected}' غير موجودة"

    def test_get_category_by_id(self, client):
        response = client.get("/api/categories/medicine")
        assert response.status_code == 200
        data = response.json()
        assert "category" in data
        assert data["category"]["id"] == "medicine"

    def test_get_category_ethics(self, client):
        response = client.get("/api/categories/ethics")
        assert response.status_code == 200
        data = response.json()
        assert data["category"]["id"] == "ethics"

    def test_get_category_not_found(self, client):
        response = client.get("/api/categories/nonexistent_category")
        assert response.status_code == 404
