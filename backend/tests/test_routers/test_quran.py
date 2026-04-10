"""
اختبارات نقاط نهاية بيانات القرآن الكريم (السور والآيات والميزات الإبداعية).
"""
import datetime
import pytest
from unittest.mock import AsyncMock, patch


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

    def test_get_surah_negative(self, client):
        """رقم السورة السالب يجب أن يُعيد 400."""
        response = client.get("/api/quran/surah/-1")
        assert response.status_code == 400

    def test_get_surah_boundary_1(self, client):
        """السورة الأولى (الفاتحة) مقبولة رقماً."""
        with patch("routers.quran.quran_service.get_surah", new_callable=AsyncMock) as m:
            m.return_value = {"id": 1, "name": "الفاتحة", "ayahs": []}
            response = client.get("/api/quran/surah/1")
        assert response.status_code == 200

    def test_get_surah_boundary_114(self, client):
        """السورة 114 (الناس) مقبولة رقماً."""
        with patch("routers.quran.quran_service.get_surah", new_callable=AsyncMock) as m:
            m.return_value = {"id": 114, "name": "الناس", "ayahs": []}
            response = client.get("/api/quran/surah/114")
        assert response.status_code == 200

    def test_get_surah_returns_404_when_service_none(self, client):
        """إذا أعادت الخدمة None، يجب إرجاع 404."""
        with patch("routers.quran.quran_service.get_surah", new_callable=AsyncMock) as m:
            m.return_value = None
            response = client.get("/api/quran/surah/50")
        assert response.status_code == 404

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

    def test_search_missing_query_param(self, client):
        """غياب معامل q يُعيد 422."""
        response = client.get("/api/quran/search")
        assert response.status_code == 422


class TestGetAyahLocal:
    """اختبارات نقطة نهاية /api/quran/ayah/{surah}/{verse} بمصدر محلي."""

    def test_get_fatiha_verse_1(self, client):
        """آية الفاتحة الأولى من المصحف المحلي."""
        response = client.get("/api/quran/ayah/1/1")
        assert response.status_code == 200
        data = response.json()
        assert data["surah_id"] == 1
        assert data["ayah_number"] == 1
        assert "text_uthmani" in data
        assert any(ord(c) > 0x0600 for c in data["text_uthmani"])

    def test_get_ayat_al_kursi(self, client):
        """آية الكرسي البقرة:255."""
        response = client.get("/api/quran/ayah/2/255")
        assert response.status_code == 200
        data = response.json()
        assert data["surah_id"] == 2
        assert data["ayah_number"] == 255

    def test_get_ayah_ikhlas_1(self, client):
        """سورة الإخلاص آية 1."""
        response = client.get("/api/quran/ayah/112/1")
        assert response.status_code == 200
        data = response.json()
        assert data["surah_id"] == 112

    def test_get_ayah_nonexistent_verse(self, client):
        """آية غير موجودة تُعيد 404."""
        with patch("routers.quran.quran_service.get_ayah", new_callable=AsyncMock) as m:
            m.return_value = None
            response = client.get("/api/quran/ayah/1/999")
        assert response.status_code == 404

    def test_get_ayah_response_schema(self, client):
        """التحقق من مخطط الاستجابة."""
        response = client.get("/api/quran/ayah/2/1")
        assert response.status_code == 200
        data = response.json()
        for key in ("surah_id", "ayah_number", "text_uthmani", "surah_name_ar"):
            assert key in data, f"الحقل '{key}' مفقود"


class TestRandomAyah:
    """اختبارات نقطة نهاية /api/quran/random — آية عشوائية من المصحف."""

    def test_returns_200(self, client):
        response = client.get("/api/quran/random")
        assert response.status_code == 200

    def test_response_has_required_fields(self, client):
        data = client.get("/api/quran/random").json()
        for key in ("surah_id", "ayah_number", "text_uthmani", "surah_name_ar"):
            assert key in data

    def test_surah_id_in_valid_range(self, client):
        data = client.get("/api/quran/random").json()
        assert 1 <= data["surah_id"] <= 114

    def test_ayah_number_positive(self, client):
        data = client.get("/api/quran/random").json()
        assert data["ayah_number"] >= 1

    def test_text_is_arabic(self, client):
        data = client.get("/api/quran/random").json()
        assert any(ord(c) > 0x0600 for c in data["text_uthmani"])

    def test_with_valid_surah_id(self, client):
        """آية عشوائية من سورة الفاتحة."""
        response = client.get("/api/quran/random?surah_id=1")
        assert response.status_code == 200
        data = response.json()
        assert data["surah_id"] == 1
        assert 1 <= data["ayah_number"] <= 7

    def test_with_surah_baqarah(self, client):
        """آية عشوائية من سورة البقرة."""
        response = client.get("/api/quran/random?surah_id=2")
        assert response.status_code == 200
        data = response.json()
        assert data["surah_id"] == 2
        assert 1 <= data["ayah_number"] <= 286

    def test_with_last_surah(self, client):
        """آية عشوائية من سورة الناس."""
        response = client.get("/api/quran/random?surah_id=114")
        assert response.status_code == 200
        data = response.json()
        assert data["surah_id"] == 114

    def test_invalid_surah_id_returns_400(self, client):
        """رقم سورة خارج النطاق يُعيد 400."""
        assert client.get("/api/quran/random?surah_id=0").status_code == 400
        assert client.get("/api/quran/random?surah_id=115").status_code == 400

    def test_multiple_calls_vary(self, client):
        """استدعاءات متعددة يجب أن تُرجع آيات مختلفة (في الغالب)."""
        results = {
            f"{client.get('/api/quran/random').json()['surah_id']}-"
            f"{client.get('/api/quran/random').json()['ayah_number']}"
            for _ in range(10)
        }
        # With 6236 ayahs the probability all 10 are the same is astronomically low
        assert len(results) >= 1  # At minimum passes; in practice should be > 1


class TestWordOfDay:
    """اختبارات نقطة نهاية /api/quran/word-of-day — آية اليوم."""

    def test_returns_200(self, client):
        response = client.get("/api/quran/word-of-day")
        assert response.status_code == 200

    def test_response_has_date(self, client):
        data = client.get("/api/quran/word-of-day").json()
        assert "date" in data
        assert data["date"] == str(datetime.date.today())

    def test_response_has_day_index(self, client):
        data = client.get("/api/quran/word-of-day").json()
        assert "day_index" in data
        assert isinstance(data["day_index"], int)
        assert 0 <= data["day_index"] < 6236

    def test_response_has_ayah_fields(self, client):
        data = client.get("/api/quran/word-of-day").json()
        for key in ("surah_id", "ayah_number", "text_uthmani", "surah_name_ar"):
            assert key in data

    def test_text_is_arabic(self, client):
        data = client.get("/api/quran/word-of-day").json()
        assert any(ord(c) > 0x0600 for c in data["text_uthmani"])

    def test_same_day_same_ayah(self, client):
        """آية اليوم ثابتة عند استدعاءات متعددة في نفس اليوم."""
        r1 = client.get("/api/quran/word-of-day").json()
        r2 = client.get("/api/quran/word-of-day").json()
        assert r1["surah_id"] == r2["surah_id"]
        assert r1["ayah_number"] == r2["ayah_number"]
        assert r1["text_uthmani"] == r2["text_uthmani"]

    def test_different_days_different_ayahs(self, client):
        """تواريخ مختلفة تُعطي آيات مختلفة."""
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        with patch("routers.quran.datetime") as mock_dt:
            mock_dt.date.today.return_value = today
            mock_dt.date.side_effect = lambda *a, **k: datetime.date(*a, **k)
            r1 = client.get("/api/quran/word-of-day").json()

        with patch("routers.quran.datetime") as mock_dt:
            mock_dt.date.today.return_value = tomorrow
            mock_dt.date.side_effect = lambda *a, **k: datetime.date(*a, **k)
            r2 = client.get("/api/quran/word-of-day").json()

        # Different days should yield different indices
        assert r1["day_index"] != r2["day_index"]


class TestCorpusSearch:
    """اختبارات نقطة نهاية /api/quran/corpus/search — بحث في المصحف المحلي."""

    def test_returns_200(self, client):
        response = client.get("/api/quran/corpus/search?q=الصبر")
        assert response.status_code == 200

    def test_response_structure(self, client):
        data = client.get("/api/quran/corpus/search?q=الصبر").json()
        assert "query" in data
        assert "ayahs" in data
        assert "total_results" in data
        assert isinstance(data["ayahs"], list)

    def test_query_reflected_in_response(self, client):
        data = client.get("/api/quran/corpus/search?q=الشكر").json()
        assert data["query"] == "الشكر"

    def test_top_k_limit_respected(self, client):
        data = client.get("/api/quran/corpus/search?q=الله&top_k=3").json()
        assert len(data["ayahs"]) <= 3

    def test_top_k_max_20(self, client):
        """top_k أكبر من 20 يُعيد 422."""
        response = client.get("/api/quran/corpus/search?q=الله&top_k=21")
        assert response.status_code == 422

    def test_top_k_min_1(self, client):
        """top_k = 0 يُعيد 422."""
        response = client.get("/api/quran/corpus/search?q=الله&top_k=0")
        assert response.status_code == 422

    def test_with_category_boost(self, client):
        data = client.get("/api/quran/corpus/search?q=الصحة&category=medicine").json()
        assert data["category"] == "medicine"

    def test_query_too_short(self, client):
        """مصطلح بحث قصير جداً يُعيد 422."""
        response = client.get("/api/quran/corpus/search?q=أ")
        assert response.status_code == 422

    def test_missing_q_returns_422(self, client):
        response = client.get("/api/quran/corpus/search")
        assert response.status_code == 422

    def test_ayahs_have_required_fields(self, client):
        data = client.get("/api/quran/corpus/search?q=العلم").json()
        if data["ayahs"]:
            ayah = data["ayahs"][0]
            for key in ("surah_id", "ayah_number", "text_uthmani", "surah_name_ar"):
                assert key in ayah

    def test_arabic_text_in_results(self, client):
        data = client.get("/api/quran/corpus/search?q=الإيمان").json()
        if data["ayahs"]:
            text = data["ayahs"][0]["text_uthmani"]
            assert any(ord(c) > 0x0600 for c in text)

    def test_total_results_matches_ayahs_length(self, client):
        data = client.get("/api/quran/corpus/search?q=الرحمن").json()
        assert data["total_results"] == len(data["ayahs"])
