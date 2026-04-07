"""
اختبارات نقاط نهاية المعجزات العلمية والتفسير.
"""
import pytest


class TestMiracles:
    def test_get_all_miracles(self, client):
        response = client.get("/api/miracles")
        assert response.status_code == 200
        miracles = response.json()
        assert isinstance(miracles, list)
        assert len(miracles) > 0

    def test_miracles_have_required_fields(self, client):
        response = client.get("/api/miracles")
        miracles = response.json()
        for miracle in miracles:
            assert "id" in miracle
            assert "title_ar" in miracle
            assert "ayah" in miracle
            assert "surah_name" in miracle
            assert "ayah_ref" in miracle
            assert "scientific_fact" in miracle
            assert "category" in miracle

    def test_miracles_arabic_content(self, client):
        """يجب أن تحتوي المعجزات على نصوص عربية."""
        response = client.get("/api/miracles")
        miracles = response.json()
        for miracle in miracles:
            assert any(ord(c) > 0x0600 for c in miracle["title_ar"])
            assert any(ord(c) > 0x0600 for c in miracle["ayah"])

    def test_get_miracles_by_category(self, client):
        response = client.get("/api/miracles/astronomy")
        assert response.status_code == 200
        miracles = response.json()
        assert isinstance(miracles, list)
        for miracle in miracles:
            assert miracle["category"] == "astronomy"

    def test_get_miracles_unknown_category(self, client):
        """فئة غير موجودة تُعيد قائمة فارغة."""
        response = client.get("/api/miracles/unknown_category_xyz")
        assert response.status_code == 200
        assert response.json() == []


class TestTafsir:
    def test_get_scholars(self, client):
        response = client.get("/api/tafsir/scholars")
        assert response.status_code == 200
        scholars = response.json()
        assert isinstance(scholars, list)
        assert len(scholars) > 0

    def test_scholars_have_arabic_names(self, client):
        response = client.get("/api/tafsir/scholars")
        scholars = response.json()
        for scholar in scholars:
            assert "name_ar" in scholar
            assert any(ord(c) > 0x0600 for c in scholar["name_ar"])

    def test_get_tafsir_for_ayah(self, client):
        response = client.get("/api/tafsir/1")
        assert response.status_code == 200
        tafsir_list = response.json()
        assert isinstance(tafsir_list, list)
        assert len(tafsir_list) > 0

    def test_tafsir_has_required_fields(self, client):
        response = client.get("/api/tafsir/1")
        tafsir_list = response.json()
        for tafsir in tafsir_list:
            assert "scholar_name_ar" in tafsir
            assert "text" in tafsir
            assert "source" in tafsir
