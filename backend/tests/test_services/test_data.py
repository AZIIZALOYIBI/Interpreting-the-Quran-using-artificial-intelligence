"""
اختبارات وحدة لبيانات الفئات والآيات النموذجية.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data.categories import CATEGORIES
from data.sample_ayahs import SAMPLE_AYAHS


class TestCategories:
    def test_categories_is_list(self):
        assert isinstance(CATEGORIES, list)

    def test_categories_not_empty(self):
        assert len(CATEGORIES) > 0

    def test_ethics_category_exists(self):
        ids = [c["id"] for c in CATEGORIES]
        assert "ethics" in ids, "فئة الأخلاق غير موجودة"

    def test_all_required_fields_present(self):
        required = ["id", "name_ar", "name_en", "icon", "description"]
        for cat in CATEGORIES:
            for field in required:
                assert field in cat, f"الحقل '{field}' مفقود في الفئة '{cat.get('id')}'"

    def test_category_ids_unique(self):
        ids = [c["id"] for c in CATEGORIES]
        assert len(ids) == len(set(ids)), "معرّفات الفئات غير فريدة"

    def test_arabic_names_contain_arabic(self):
        for cat in CATEGORIES:
            assert any(ord(c) > 0x0600 for c in cat["name_ar"]), \
                f"الاسم العربي للفئة '{cat['id']}' لا يحتوي على حروف عربية"

    def test_main_categories_present(self):
        expected = ["medicine", "work", "science", "family", "law", "environment", "ethics", "self_development"]
        ids = [c["id"] for c in CATEGORIES]
        for cat_id in expected:
            assert cat_id in ids, f"الفئة '{cat_id}' مفقودة"


class TestSampleAyahs:
    def test_sample_ayahs_is_dict(self):
        assert isinstance(SAMPLE_AYAHS, dict)

    def test_all_main_categories_have_ayahs(self):
        main_categories = ["medicine", "work", "science", "family", "law", "environment", "ethics", "self_development"]
        for cat in main_categories:
            assert cat in SAMPLE_AYAHS, f"الفئة '{cat}' ليس لها آيات نموذجية"
            assert len(SAMPLE_AYAHS[cat]) > 0, f"الفئة '{cat}' لديها قائمة آيات فارغة"

    def test_ayahs_have_required_fields(self):
        required = ["id", "surah_id", "surah_name_ar", "ayah_number", "text_uthmani"]
        for category, ayahs in SAMPLE_AYAHS.items():
            for ayah in ayahs:
                for field in required:
                    assert field in ayah, f"الحقل '{field}' مفقود في آية من فئة '{category}'"

    def test_ayahs_uthmani_text_is_arabic(self):
        for category, ayahs in SAMPLE_AYAHS.items():
            for ayah in ayahs:
                text = ayah.get("text_uthmani", "")
                assert any(ord(c) > 0x0600 for c in text), \
                    f"نص الآية في فئة '{category}' لا يحتوي على حروف عربية"

    def test_surah_ids_are_valid(self):
        """أرقام السور يجب أن تكون بين 1 و 114."""
        for category, ayahs in SAMPLE_AYAHS.items():
            for ayah in ayahs:
                surah_id = ayah["surah_id"]
                assert 1 <= surah_id <= 114, \
                    f"رقم السورة {surah_id} خارج النطاق في فئة '{category}'"

    def test_ayah_ids_unique(self):
        """يجب أن تكون معرّفات الآيات فريدة عبر جميع الفئات."""
        all_ids = []
        for ayahs in SAMPLE_AYAHS.values():
            all_ids.extend(a["id"] for a in ayahs)
        assert len(all_ids) == len(set(all_ids)), "معرّفات الآيات غير فريدة"
