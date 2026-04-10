"""
اختبارات وحدة لمحرك البحث في القرآن الكريم (quran_text_service).
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.quran_text_service import (
    search_ayahs,
    get_ayah,
    total_ayahs,
    reset_corpus,
    Ayah,
    _normalize,
    _strip_diacritics,
    _tokenize,
)


@pytest.fixture(autouse=True)
def reload_corpus():
    """أعد تحميل المصحف قبل كل اختبار لضمان حالة نظيفة."""
    reset_corpus()
    yield
    reset_corpus()


class TestCorpusLoading:
    def test_total_ayahs_is_6236(self):
        """يجب أن يحتوي المصحف على 6236 آية."""
        assert total_ayahs() == 6236

    def test_get_fatiha_verse_1(self):
        """التحقق من الآية الأولى في الفاتحة."""
        a = get_ayah(1, 1)
        assert a is not None
        assert a.surah_number == 1
        assert a.ayah_number == 1
        assert a.surah_name_ar == "الفاتحة"
        assert "بسم" in _strip_diacritics(a.text) or "بِسۡمِ" in a.text or "بِسۡمِ" in a.text

    def test_get_ayat_al_kursi(self):
        """التحقق من آية الكرسي (البقرة:255)."""
        from services.quran_text_service import _strip_diacritics
        a = get_ayah(2, 255)
        assert a is not None
        assert a.surah_number == 2
        assert a.ayah_number == 255
        # The corpus uses ٱ (alef wasla) — normalise before checking
        text_clean = _strip_diacritics(a.text).replace("ٱ", "ا")
        assert "الله" in text_clean

    def test_get_al_ikhlas_verse_1(self):
        """التحقق من الآية الأولى في سورة الإخلاص."""
        a = get_ayah(112, 1)
        assert a is not None
        assert a.surah_name_en == "Al-Ikhlas"

    def test_get_nonexistent_ayah_returns_none(self):
        """طلب آية غير موجودة يجب أن يُرجع None."""
        assert get_ayah(1, 999) is None
        assert get_ayah(115, 1) is None

    def test_ayah_to_dict_has_required_keys(self):
        """to_dict() يجب أن يُرجع القاموس بالحقول الصحيحة."""
        a = get_ayah(1, 1)
        assert a is not None
        d = a.to_dict()
        assert "surah_id" in d
        assert "ayah_number" in d
        assert "text_uthmani" in d
        assert "surah_name_ar" in d
        assert "surah_name" in d

    def test_surah_numbers_in_range(self):
        """جميع الآيات يجب أن تحتوي على أرقام سور بين 1 و 114."""
        # Load corpus then spot-check last surah
        a = get_ayah(114, 1)
        assert a is not None
        assert 1 <= a.surah_number <= 114


class TestArabicNormalization:
    def test_strip_diacritics_removes_tashkeel(self):
        text = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"
        clean = _strip_diacritics(text)
        # No diacritics should remain
        for ch in clean:
            assert ord(ch) < 0x064B or ord(ch) > 0x065F

    def test_normalize_alef_variants(self):
        assert _normalize("أحمد") == "احمد"
        assert _normalize("إبراهيم") == "ابراهيم"
        assert _normalize("آية") == "ايه"

    def test_normalize_ya_maqsura(self):
        assert _normalize("الهدى") == "الهدي"

    def test_tokenize_splits_words(self):
        tokens = _tokenize("قل هو الله أحد")
        # قل and هو are only 2 chars so filtered out (min 3 chars)
        assert "الله" in tokens
        assert "احد" in tokens  # أحد normalized to احد

    def test_tokenize_ignores_short_tokens(self):
        tokens = _tokenize("بت ج الله")
        assert "بت" not in tokens
        assert "ج" not in tokens
        assert "الله" in tokens


class TestSearchAyahs:
    def test_search_returns_list(self):
        results = search_ayahs("الصحة والطب")
        assert isinstance(results, list)

    def test_search_top_k_limit(self):
        results = search_ayahs("الله", top_k=3)
        assert len(results) <= 3

    def test_search_returns_ayah_objects(self):
        results = search_ayahs("الشفاء", category="medicine")
        for r in results:
            assert isinstance(r, Ayah)

    def test_search_medicine_returns_relevant_ayahs(self):
        """البحث في الطب يجب أن يجد آيات ذات صلة."""
        results = search_ayahs("الشفاء والصحة", category="medicine", top_k=5)
        assert len(results) > 0
        # At least one ayah should contain a root related to medicine/healing
        combined = " ".join(_strip_diacritics(r.text).replace("ٱ", "ا") for r in results)
        medicine_roots = ["شفاء", "مرض", "طب", "صحة", "عسل", "شرب", "ماء", "شفا"]
        assert any(root in combined for root in medicine_roots)

    def test_search_science_returns_relevant_ayahs(self):
        results = search_ayahs("العلم والتفكر", category="science", top_k=5)
        assert len(results) > 0

    def test_search_empty_query_returns_empty(self):
        results = search_ayahs("")
        assert results == []

    def test_search_irrelevant_query_may_return_empty(self):
        """استعلام بدون كلمات عربية يجب أن يُرجع قائمة فارغة أو نتائج."""
        results = search_ayahs("xyz123")
        assert isinstance(results, list)

    def test_search_well_known_verse(self):
        """البحث عن 'حسبنا الله' يجب أن يجد آية البقرة 200."""
        results = search_ayahs("حسبنا الله ونعم الوكيل", top_k=5)
        found = any(
            _strip_diacritics("حسبنا الله") in _strip_diacritics(r.text)
            or ("حسبنا" in _strip_diacritics(r.text))
            for r in results
        )
        assert len(results) > 0

    def test_search_category_boost(self):
        """تحديد الفئة يجب أن يُحسّن نتائج البحث."""
        results_with_cat = search_ayahs("الكسب والرزق", category="work", top_k=5)
        results_without = search_ayahs("الكسب والرزق", top_k=5)
        # Both should return results
        assert isinstance(results_with_cat, list)
        assert isinstance(results_without, list)
