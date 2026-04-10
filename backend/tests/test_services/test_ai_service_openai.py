"""
اختبارات إضافية لخدمة الذكاء الاصطناعي — تغطية مسار OpenAI والحالات الحدية.
"""
import asyncio
import os
from unittest.mock import AsyncMock, MagicMock, patch
import pytest


class TestOpenAIPath:
    def test_get_solution_uses_openai_when_key_present(self):
        """عند وجود مفتاح OpenAI، يستخدم مسار OpenAI."""
        from services.ai_service import get_quran_solution

        # بناء استجابة OpenAI وهمية
        mock_message = MagicMock()
        mock_message.content = "هذا رد من OpenAI يتضمن إرشاداً قرآنياً."

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]

        mock_openai_client = AsyncMock()
        mock_openai_client.chat = AsyncMock()
        mock_openai_client.chat.completions = AsyncMock()
        mock_openai_client.chat.completions.create = AsyncMock(return_value=mock_completion)

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-123"}):
            with patch("services.ai_service._get_openai_solution", new_callable=AsyncMock) as mock_fn:
                mock_fn.return_value = {
                    "answer": "رد OpenAI",
                    "category": "medicine",
                    "ayahs": [],
                    "practical_steps": [],
                }
                result = asyncio.run(get_quran_solution("ما إرشاد القرآن في الصحة؟", "medicine"))

        assert result["answer"] == "رد OpenAI"
        assert result["category"] == "medicine"
        mock_fn.assert_called_once()

    def test_get_solution_falls_back_on_openai_exception(self):
        """عند فشل OpenAI، يعود إلى الرد الوهمي."""
        from services.ai_service import get_quran_solution

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-123"}):
            with patch("services.ai_service._get_openai_solution", new_callable=AsyncMock) as mock_fn:
                mock_fn.side_effect = Exception("OpenAI connection failed")
                result = asyncio.run(get_quran_solution("ما إرشاد القرآن في الصحة؟", "medicine"))

        assert "answer" in result
        assert result["category"] == "medicine"
        # تحقق من أن الرد يتضمن نصاً عربياً
        assert any(ord(c) > 0x0600 for c in result["answer"])

    def test_get_openai_solution_direct(self):
        """اختبار مباشر لدالة _get_openai_solution."""
        import sys
        from services.ai_service import _get_openai_solution

        mock_message = MagicMock()
        mock_message.content = "إجابة قرآنية من نموذج الذكاء الاصطناعي حول الصحة."

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]

        mock_client_instance = AsyncMock()
        mock_client_instance.chat.completions.create = AsyncMock(return_value=mock_completion)

        mock_openai_module = MagicMock()
        mock_openai_module.AsyncOpenAI = MagicMock(return_value=mock_client_instance)

        with patch.dict(sys.modules, {"openai": mock_openai_module}):
            result = asyncio.run(_get_openai_solution(
                "كيف يرشدنا القرآن في الصحة؟", "medicine", "fake-api-key", []
            ))

        assert result["category"] == "medicine"
        assert result["answer"] == "إجابة قرآنية من نموذج الذكاء الاصطناعي حول الصحة."
        assert "ayahs" in result
        assert "practical_steps" in result
        assert isinstance(result["practical_steps"], list)

    def test_get_openai_solution_null_content(self):
        """عند إرجاع محتوى None من OpenAI، الإجابة تكون سلسلة فارغة."""
        import sys
        from services.ai_service import _get_openai_solution

        mock_message = MagicMock()
        mock_message.content = None

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]

        mock_client_instance = AsyncMock()
        mock_client_instance.chat.completions.create = AsyncMock(return_value=mock_completion)

        mock_openai_module = MagicMock()
        mock_openai_module.AsyncOpenAI = MagicMock(return_value=mock_client_instance)

        with patch.dict(sys.modules, {"openai": mock_openai_module}):
            result = asyncio.run(_get_openai_solution(
                "سؤال اختبار", "general", "fake-api-key", []
            ))

        assert result["answer"] == ""
        assert result["category"] == "general"

    def test_get_openai_solution_all_categories(self):
        """_get_openai_solution تعمل مع جميع الفئات."""
        import sys
        from services.ai_service import _get_openai_solution

        mock_message = MagicMock()
        mock_message.content = "إجابة اختبار."

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]

        mock_client_instance = AsyncMock()
        mock_client_instance.chat.completions.create = AsyncMock(return_value=mock_completion)

        mock_openai_module = MagicMock()
        mock_openai_module.AsyncOpenAI = MagicMock(return_value=mock_client_instance)

        categories = ["medicine", "work", "science", "family", "self_development",
                      "law", "environment", "ethics", "general"]

        with patch.dict(sys.modules, {"openai": mock_openai_module}):
            for cat in categories:
                result = asyncio.run(_get_openai_solution("سؤال اختبار", cat, "fake-key", []))
                assert result["category"] == cat


class TestGetSolutionEdgeCases:
    def test_no_api_key_uses_mock(self):
        """بدون مفتاح API، يستخدم الرد الوهمي مباشرة."""
        from services.ai_service import get_quran_solution

        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            result = asyncio.run(get_quran_solution("ما إرشاد القرآن؟", "science"))

        assert result["category"] == "science"
        assert "answer" in result

    def test_unknown_category_uses_default_response(self):
        """فئة غير معروفة تُعيد الرد الافتراضي."""
        from services.ai_service import get_quran_solution

        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            result = asyncio.run(get_quran_solution("سؤال اختبار", "unknown_category"))

        assert "answer" in result
        assert "category" in result
