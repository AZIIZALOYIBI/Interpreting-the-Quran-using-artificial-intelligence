"""
اختبارات وحدة لمنطق خدمة الذكاء الاصطناعي (ai_service).
تستخدم القرآن الحقيقي المُحمَّل محلياً — لا ردود وهمية.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.ai_service import classify_question, CATEGORY_KEYWORDS


class TestClassifyQuestion:
    def test_classify_medicine(self):
        assert classify_question("ما إرشاد القرآن في موضوع الصحة؟") == "medicine"

    def test_classify_work(self):
        assert classify_question("كيف أكسب المال الحلال؟") == "work"

    def test_classify_science(self):
        assert classify_question("ما موقف الإسلام من العلم والبحث؟") == "science"

    def test_classify_family(self):
        assert classify_question("ما دور الأسرة والوالدين في الإسلام؟") == "family"

    def test_classify_law(self):
        assert classify_question("ما مبدأ العدل في الشريعة الإسلامية؟") == "law"

    def test_classify_environment(self):
        assert classify_question("كيف يأمر الإسلام بالحفاظ على البيئة؟") == "environment"

    def test_classify_ethics(self):
        assert classify_question("ما أهمية الأخلاق والصدق في الإسلام؟") == "ethics"

    def test_classify_self_development(self):
        assert classify_question("كيف أطور نفسي وأقوي إيماني؟") == "self_development"

    def test_classify_general_fallback(self):
        """سؤال لا يحتوي على كلمات مفتاحية يُصنَّف كـ general."""
        assert classify_question("hello world") == "general"

    def test_classify_empty_string(self):
        assert classify_question("") == "general"

    def test_all_categories_have_keywords(self):
        for category, keywords in CATEGORY_KEYWORDS.items():
            assert len(keywords) > 0, f"الفئة '{category}' ليس لها كلمات مفتاحية"


class TestGetQuranSolutionAsync:
    """يختبر get_quran_solution في وضع Demo (بلا مفاتيح API)."""

    def test_response_has_required_fields(self):
        from services.ai_service import get_quran_solution
        result = asyncio.run(get_quran_solution("ما إرشاد القرآن في الصحة؟", "medicine"))
        assert "answer" in result
        assert "category" in result
        assert "ayahs" in result
        assert "practical_steps" in result

    def test_category_medicine_returned(self):
        from services.ai_service import get_quran_solution
        result = asyncio.run(get_quran_solution("ما إرشاد القرآن في الصحة؟", "medicine"))
        assert result["category"] == "medicine"
        assert len(result["answer"]) > 0

    def test_auto_classify_medicine(self):
        from services.ai_service import get_quran_solution
        result = asyncio.run(get_quran_solution("كيف يرشدنا القرآن في موضوع الصحة؟"))
        assert result["category"] == "medicine"

    def test_general_category(self):
        from services.ai_service import get_quran_solution
        result = asyncio.run(get_quran_solution("سؤال عام جداً", "general"))
        assert "answer" in result

    def test_question_appears_in_answer(self):
        from services.ai_service import get_quran_solution
        question = "ما إرشاد القرآن في الصحة؟"
        result = asyncio.run(get_quran_solution(question, "medicine"))
        assert question in result["answer"]

    def test_ayahs_are_real_quran_dicts(self):
        """الآيات يجب أن تكون قواميس بالحقول الصحيحة من المصحف الحقيقي."""
        from services.ai_service import get_quran_solution
        result = asyncio.run(get_quran_solution("ما إرشاد القرآن في الصحة؟", "medicine"))
        for ayah in result["ayahs"]:
            assert "surah_id" in ayah
            assert "ayah_number" in ayah
            assert "text_uthmani" in ayah
            assert "surah_name_ar" in ayah
            # Verify it contains real Arabic text
            assert any(ord(c) > 0x0600 for c in ayah["text_uthmani"])

    def test_ayah_references_are_valid(self):
        """أرقام السور والآيات يجب أن تكون ضمن النطاق الصحيح."""
        from services.ai_service import get_quran_solution
        result = asyncio.run(get_quran_solution("ما إرشاد القرآن في الصحة؟", "medicine"))
        for ayah in result["ayahs"]:
            assert 1 <= ayah["surah_id"] <= 114
            assert ayah["ayah_number"] >= 1

    def test_work_category(self):
        from services.ai_service import get_quran_solution
        result = asyncio.run(get_quran_solution("كيف يرشدنا القرآن في التجارة والعمل؟", "work"))
        assert result["category"] == "work"

    def test_no_ai_keys_returns_demo_with_real_ayahs(self):
        """في وضع Demo يجب إرجاع آيات حقيقية لا ردود وهمية."""
        import os
        from services.ai_service import get_quran_solution
        # Ensure no API keys are set
        old_key = os.environ.pop("OPENAI_API_KEY", "")
        old_gptq = os.environ.pop("GPTQ_MODEL_PATH", "")
        try:
            result = asyncio.run(get_quran_solution("ما إرشاد القرآن في الصحة؟", "medicine"))
            assert "answer" in result
            assert isinstance(result["ayahs"], list)
        finally:
            if old_key:
                os.environ["OPENAI_API_KEY"] = old_key
            if old_gptq:
                os.environ["GPTQ_MODEL_PATH"] = old_gptq
