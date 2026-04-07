"""
اختبارات خدمة جلب بيانات القرآن الكريم من API الخارجية.
تستخدم مكتبة unittest.mock لمحاكاة استجابات HTTP بدون اتصال فعلي.
"""
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
import pytest


# ── مساعدات بناء الاستجابات الوهمية ──────────────────────────────────────────

def _make_response(status_code: int, data: dict) -> MagicMock:
    """ينشئ كائن استجابة httpx وهمياً."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = data
    return mock_resp


def _mock_client(response: MagicMock) -> MagicMock:
    """ينشئ AsyncClient وهمياً يُعيد استجابة محددة."""
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    return mock_client


def _error_client() -> MagicMock:
    """ينشئ AsyncClient وهمياً يُطلق استثناء عند الاستدعاء."""
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=Exception("network error"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    return mock_client


# ── بيانات الاختبار ──────────────────────────────────────────────────────────

SAMPLE_AYAH_RESPONSE = {
    "code": 200,
    "data": {
        "number": 7,
        "text": "صِرَاطَ الَّذِينَ أَنۡعَمۡتَ عَلَيۡهِمۡ",
        "numberInSurah": 7,
        "surah": {
            "number": 1,
            "name": "سُورَةُ ٱلْفَاتِحَةِ",
            "englishName": "Al-Faatiha",
        },
    },
}

SAMPLE_SURAH_RESPONSE = {
    "code": 200,
    "data": {
        "number": 1,
        "name": "سُورَةُ ٱلْفَاتِحَةِ",
        "englishName": "Al-Faatiha",
        "numberOfAyahs": 7,
        "revelationType": "Meccan",
        "ayahs": [
            {
                "number": 1,
                "text": "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ",
                "numberInSurah": 1,
            },
            {
                "number": 2,
                "text": "ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ",
                "numberInSurah": 2,
            },
        ],
    },
}

SAMPLE_SURAH_LIST_RESPONSE = {
    "code": 200,
    "data": [
        {
            "number": 1,
            "name": "سُورَةُ ٱلْفَاتِحَةِ",
            "englishName": "Al-Faatiha",
            "numberOfAyahs": 7,
            "revelationType": "Meccan",
        },
        {
            "number": 2,
            "name": "سُورَةُ ٱلْبَقَرَةِ",
            "englishName": "Al-Baqara",
            "numberOfAyahs": 286,
            "revelationType": "Medinan",
        },
    ],
}

SAMPLE_SEARCH_RESPONSE = {
    "code": 200,
    "data": {
        "matches": [
            {
                "number": 103,
                "text": "وَٱصۡبِرۡۚ إِنَّ ٱللَّهَ مَعَ ٱلصَّـٰبِرِينَ",
                "numberInSurah": 46,
                "surah": {
                    "number": 8,
                    "name": "سُورَةُ ٱلْأَنفَالِ",
                    "englishName": "Al-Anfal",
                },
            }
        ]
    },
}


# ── اختبارات get_ayah ────────────────────────────────────────────────────────

class TestGetAyah:
    def test_get_ayah_success(self):
        """يُعيد بيانات الآية عند نجاح الاستجابة."""
        from services.quran_service import get_ayah

        mock_resp = _make_response(200, SAMPLE_AYAH_RESPONSE)
        with patch("httpx.AsyncClient", return_value=_mock_client(mock_resp)):
            result = asyncio.run(get_ayah(1, 7))

        assert result is not None
        assert result["surah_id"] == 1
        assert result["ayah_number"] == 7
        assert result["surah_name"] == "Al-Faatiha"
        assert result["text_uthmani"] != ""

    def test_get_ayah_not_found(self):
        """يُعيد None عند استجابة غير 200."""
        from services.quran_service import get_ayah

        mock_resp = _make_response(404, {"code": 404, "data": "Not Found"})
        with patch("httpx.AsyncClient", return_value=_mock_client(mock_resp)):
            result = asyncio.run(get_ayah(1, 999))

        assert result is None

    def test_get_ayah_network_error(self):
        """يُعيد None عند فشل الاتصال."""
        from services.quran_service import get_ayah

        with patch("httpx.AsyncClient", return_value=_error_client()):
            result = asyncio.run(get_ayah(1, 1))

        assert result is None


# ── اختبارات get_surah ───────────────────────────────────────────────────────

class TestGetSurah:
    def test_get_surah_success(self):
        """يُعيد بيانات السورة مع آياتها عند النجاح."""
        from services.quran_service import get_surah

        mock_resp = _make_response(200, SAMPLE_SURAH_RESPONSE)
        with patch("httpx.AsyncClient", return_value=_mock_client(mock_resp)):
            result = asyncio.run(get_surah(1))

        assert result is not None
        assert "info" in result
        assert "ayahs" in result
        assert result["info"]["id"] == 1
        assert result["info"]["name_ar"] == "سُورَةُ ٱلْفَاتِحَةِ"
        assert result["info"]["revelation_type"] == "meccan"
        assert len(result["ayahs"]) == 2

    def test_get_surah_ayah_fields(self):
        """تتضمن الآيات جميع الحقول المطلوبة."""
        from services.quran_service import get_surah

        mock_resp = _make_response(200, SAMPLE_SURAH_RESPONSE)
        with patch("httpx.AsyncClient", return_value=_mock_client(mock_resp)):
            result = asyncio.run(get_surah(1))

        ayah = result["ayahs"][0]
        assert "surah_id" in ayah
        assert "text_uthmani" in ayah
        assert "ayah_number" in ayah

    def test_get_surah_not_found(self):
        """يُعيد None عند استجابة غير 200."""
        from services.quran_service import get_surah

        mock_resp = _make_response(404, {"code": 404})
        with patch("httpx.AsyncClient", return_value=_mock_client(mock_resp)):
            result = asyncio.run(get_surah(999))

        assert result is None

    def test_get_surah_network_error(self):
        """يُعيد None عند فشل الاتصال."""
        from services.quran_service import get_surah

        with patch("httpx.AsyncClient", return_value=_error_client()):
            result = asyncio.run(get_surah(1))

        assert result is None


# ── اختبارات get_surah_list ──────────────────────────────────────────────────

class TestGetSurahList:
    def test_get_surah_list_success(self):
        """يُعيد قائمة السور عند النجاح."""
        from services.quran_service import get_surah_list

        mock_resp = _make_response(200, SAMPLE_SURAH_LIST_RESPONSE)
        with patch("httpx.AsyncClient", return_value=_mock_client(mock_resp)):
            result = asyncio.run(get_surah_list())

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["name_ar"] == "سُورَةُ ٱلْفَاتِحَةِ"
        assert result[1]["id"] == 2

    def test_get_surah_list_fields(self):
        """كل سورة تحتوي على الحقول المطلوبة."""
        from services.quran_service import get_surah_list

        mock_resp = _make_response(200, SAMPLE_SURAH_LIST_RESPONSE)
        with patch("httpx.AsyncClient", return_value=_mock_client(mock_resp)):
            result = asyncio.run(get_surah_list())

        for surah in result:
            assert "id" in surah
            assert "name_ar" in surah
            assert "name_en" in surah
            assert "ayah_count" in surah
            assert "revelation_type" in surah

    def test_get_surah_list_error_returns_empty(self):
        """يُعيد قائمة فارغة عند فشل الاستجابة."""
        from services.quran_service import get_surah_list

        mock_resp = _make_response(500, {})
        with patch("httpx.AsyncClient", return_value=_mock_client(mock_resp)):
            result = asyncio.run(get_surah_list())

        assert result == []

    def test_get_surah_list_network_error(self):
        """يُعيد قائمة فارغة عند فشل الاتصال."""
        from services.quran_service import get_surah_list

        with patch("httpx.AsyncClient", return_value=_error_client()):
            result = asyncio.run(get_surah_list())

        assert result == []


# ── اختبارات search_ayahs ────────────────────────────────────────────────────

class TestSearchAyahs:
    def test_search_success(self):
        """يُعيد نتائج البحث عند النجاح."""
        from services.quran_service import search_ayahs

        mock_resp = _make_response(200, SAMPLE_SEARCH_RESPONSE)
        with patch("httpx.AsyncClient", return_value=_mock_client(mock_resp)):
            result = asyncio.run(search_ayahs("الصبر"))

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["surah_id"] == 8
        assert result[0]["text_uthmani"] != ""

    def test_search_url_encodes_query(self):
        """يُشفِّر معامل البحث قبل وضعه في URL."""
        from services.quran_service import search_ayahs
        import httpx

        captured_url = []

        async def fake_get(url, **kwargs):
            captured_url.append(url)
            return _make_response(200, {"data": {"matches": []}})

        mock_client = AsyncMock()
        mock_client.get = fake_get
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)

        with patch("httpx.AsyncClient", return_value=mock_client):
            asyncio.run(search_ayahs("الصبر في القرآن"))

        assert len(captured_url) == 1
        # المسافات يجب أن تكون مُشفَّرة
        assert " " not in captured_url[0]

    def test_search_empty_result(self):
        """يُعيد قائمة فارغة عند عدم وجود نتائج."""
        from services.quran_service import search_ayahs

        mock_resp = _make_response(200, {"data": {"matches": []}})
        with patch("httpx.AsyncClient", return_value=_mock_client(mock_resp)):
            result = asyncio.run(search_ayahs("xyz"))

        assert result == []

    def test_search_network_error(self):
        """يُعيد قائمة فارغة عند فشل الاتصال."""
        from services.quran_service import search_ayahs

        with patch("httpx.AsyncClient", return_value=_error_client()):
            result = asyncio.run(search_ayahs("الصبر"))

        assert result == []

    def test_search_limits_to_10_results(self):
        """يقتصر على 10 نتائج كحد أقصى."""
        from services.quran_service import search_ayahs

        matches = [
            {
                "number": i,
                "text": f"آية {i}",
                "numberInSurah": i,
                "surah": {"number": 1, "name": "الفاتحة", "englishName": "Al-Fatiha"},
            }
            for i in range(1, 16)  # 15 نتيجة
        ]
        mock_resp = _make_response(200, {"data": {"matches": matches}})
        with patch("httpx.AsyncClient", return_value=_mock_client(mock_resp)):
            result = asyncio.run(search_ayahs("آية"))

        assert len(result) <= 10
