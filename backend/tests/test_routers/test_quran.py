"""
اختبارات نقاط نهاية بيانات القرآن الكريم (السور والآيات).
"""
import pytest


class TestQuranEndpoints:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_get_surah_valid(self, client):
        """اختبار جلب سورة بمعرّف صحيح."""
        response = client.get("/api/quran/surah/1")
        # قد تُعيد 404 إذا لم تكن API الخارجية متاحة (بيئة الاختبار المعزولة)
        assert response.status_code in (200, 404, 503, 504)

    def test_get_surah_invalid_low(self, client):
        """رقم السورة 0 يجب أن يُعيد 400."""
        response = client.get("/api/quran/surah/0")
        assert response.status_code == 400

    def test_get_surah_invalid_high(self, client):
        """رقم السورة 115 يجب أن يُعيد 400."""
        response = client.get("/api/quran/surah/115")
        assert response.status_code == 400

    def test_search_ayahs_too_short(self, client):
        """البحث بحرف واحد يجب أن يُعيد 422."""
        response = client.get("/api/quran/search?q=ا")
        assert response.status_code == 422

    def test_search_ayahs_valid_query(self, client):
        """البحث بكلمة صحيحة."""
        response = client.get("/api/quran/search?q=الصبر")
        assert response.status_code in (200, 503, 504)
        if response.status_code == 200:
            assert isinstance(response.json(), list)
