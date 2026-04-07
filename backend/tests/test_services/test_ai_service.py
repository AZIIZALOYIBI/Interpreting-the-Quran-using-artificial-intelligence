"""
اختبارات وحدة لمنطق خدمة الذكاء الاصطناعي (ai_service).
"""
import pytest
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.ai_service import classify_question, CATEGORY_KEYWORDS, MOCK_RESPONSES, DEFAULT_RESPONSE


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
        """سؤال لا يحتوي على كلمات مفتاحية يجب أن يُصنَّف كـ general."""
        assert classify_question("hello world") == "general"

    def test_classify_empty_string(self):
        assert classify_question("") == "general"

    def test_all_categories_have_keywords(self):
        """يجب أن تحتوي جميع الفئات على كلمات مفتاحية."""
        for category, keywords in CATEGORY_KEYWORDS.items():
            assert len(keywords) > 0, f"الفئة '{category}' ليس لها كلمات مفتاحية"


class TestMockResponses:
    def test_all_main_categories_have_mock_responses(self):
        """يجب أن تحتوي جميع الفئات الرئيسية على ردود Mock."""
        main_categories = ["medicine", "work", "science", "family", "law", "environment", "ethics", "self_development"]
        for cat in main_categories:
            assert cat in MOCK_RESPONSES, f"الفئة '{cat}' لا تملك رد Mock"

    def test_mock_responses_have_required_fields(self):
        for category, response in MOCK_RESPONSES.items():
            assert "answer" in response, f"'{category}': حقل answer مفقود"
            assert "category" in response, f"'{category}': حقل category مفقود"
            assert "ayahs" in response, f"'{category}': حقل ayahs مفقود"
            assert "practical_steps" in response, f"'{category}': حقل practical_steps مفقود"
            assert isinstance(response["practical_steps"], list)
            assert isinstance(response["ayahs"], list)

    def test_mock_responses_category_matches(self):
        """يجب أن تتطابق قيمة category مع المفتاح."""
        for category, response in MOCK_RESPONSES.items():
            assert response["category"] == category

    def test_mock_responses_arabic_content(self):
        """يجب أن تحتوي الردود على محتوى عربي."""
        for category, response in MOCK_RESPONSES.items():
            assert any(ord(c) > 0x0600 for c in response["answer"]), \
                f"'{category}': لا يحتوي على نص عربي"

    def test_mock_responses_have_practical_steps(self):
        """يجب أن تحتوي الردود على خطوات عملية."""
        for category, response in MOCK_RESPONSES.items():
            assert len(response["practical_steps"]) > 0, \
                f"'{category}': لا تحتوي على خطوات عملية"

    def test_default_response_structure(self):
        assert "answer" in DEFAULT_RESPONSE
        assert "category" in DEFAULT_RESPONSE
        assert "ayahs" in DEFAULT_RESPONSE
        assert "practical_steps" in DEFAULT_RESPONSE
        assert DEFAULT_RESPONSE["category"] == "general"


class TestGetQuranSolutionAsync:
    def test_get_solution_medicine(self):
        from services.ai_service import get_quran_solution
        result = asyncio.run(get_quran_solution("ما إرشاد القرآن في الصحة؟", "medicine"))
        assert result["category"] == "medicine"
        assert len(result["answer"]) > 0

    def test_get_solution_auto_classify(self):
        from services.ai_service import get_quran_solution
        result = asyncio.run(get_quran_solution("كيف يرشدنا القرآن في موضوع الصحة؟"))
        assert result["category"] == "medicine"

    def test_get_solution_general(self):
        from services.ai_service import get_quran_solution
        result = asyncio.run(get_quran_solution("سؤال عام", "general"))
        assert "answer" in result

    def test_get_solution_prepends_question(self):
        from services.ai_service import get_quran_solution
        question = "ما إرشاد القرآن في الصحة؟"
        result = asyncio.run(get_quran_solution(question, "medicine"))
        assert question in result["answer"]
