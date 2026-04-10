"""
اختبارات إضافية لتغطية الفروع غير المُغطاة في:
- services/ai_service.py  (_format_ayah_context بدون آيات، _build_demo_response)
- services/tafsir_service.py  (فلترة العالم)
- services/gptq_service.py   (build_pipeline success path)
"""
import asyncio
import sys
import os
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


# ---------------------------------------------------------------------------
# ai_service — uncovered branches
# ---------------------------------------------------------------------------


class TestFormatAyahContext:
    def test_empty_ayahs_returns_no_results_text(self):
        from services.ai_service import _format_ayah_context
        result = _format_ayah_context([])
        assert "لم يُعثَر" in result

    def test_non_empty_ayahs_formats_correctly(self):
        from services.ai_service import _format_ayah_context
        from services.quran_text_service import Ayah

        ayah = Ayah(
            surah_number=1,
            ayah_number=1,
            text="بِسۡمِ ٱللَّهِ",
            surah_name_ar="الفاتحة",
            surah_name_en="Al-Fatihah",
            surah_type="meccan",
        )
        result = _format_ayah_context([ayah])
        assert "الفاتحة" in result
        assert "Al-Fatihah" in result
        assert "1" in result  # verse number


class TestBuildDemoResponse:
    def test_empty_ayahs_returns_no_results_message(self):
        from services.ai_service import _build_demo_response
        result = _build_demo_response("سؤال اختبار", "general", [])
        assert "answer" in result
        assert "لم يُعثَر" in result["answer"]
        assert result["category"] == "general"
        assert result["ayahs"] == []
        assert isinstance(result["practical_steps"], list)

    def test_with_ayahs_returns_formatted_answer(self):
        from services.ai_service import _build_demo_response
        from services.quran_text_service import Ayah

        ayah = Ayah(
            surah_number=26,
            ayah_number=80,
            text="وَإِذَا مَرِضۡتُ فَهُوَ يَشۡفِينِ",
            surah_name_ar="الشعراء",
            surah_name_en="Ash-Shuara",
            surah_type="meccan",
        )
        result = _build_demo_response("ما الشفاء؟", "medicine", [ayah])
        assert "الشعراء" in result["answer"]
        assert result["category"] == "medicine"
        assert len(result["ayahs"]) == 1
        assert result["ayahs"][0]["surah_id"] == 26

    def test_demo_response_has_practical_steps(self):
        from services.ai_service import _build_demo_response
        from services.quran_text_service import Ayah

        ayah = Ayah(1, 1, "بِسۡمِ", "الفاتحة", "Al-Fatihah", "meccan")
        result = _build_demo_response("سؤال", "general", [ayah])
        assert len(result["practical_steps"]) > 0

    def test_question_appears_in_empty_answer(self):
        from services.ai_service import _build_demo_response
        question = "ما حكم الصدقة؟"
        result = _build_demo_response(question, "ethics", [])
        assert question in result["answer"]

    def test_ayahs_converted_to_dicts(self):
        from services.ai_service import _build_demo_response
        from services.quran_text_service import Ayah

        ayah = Ayah(2, 255, "ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ", "البقرة", "Al-Baqarah", "medinan")
        result = _build_demo_response("سؤال", "general", [ayah])
        assert isinstance(result["ayahs"][0], dict)
        assert result["ayahs"][0]["surah_id"] == 2


class TestGetGPTQSolutionDirect:
    """اختبار مباشر لدالة _get_gptq_solution."""

    def test_gptq_solution_direct(self):
        import asyncio
        from services.ai_service import _get_gptq_solution
        from services.quran_text_service import Ayah

        ayah = Ayah(1, 1, "بِسۡمِ ٱللَّهِ", "الفاتحة", "Al-Fatihah", "meccan")

        with patch("services.ai_service.settings") as mock_settings:
            mock_settings.GPTQ_USE_TRITON = False
            with patch("services.gptq_service.generate", return_value="إجابة GPTQ"):
                result = asyncio.run(_get_gptq_solution(
                    "ما الشفاء؟", "medicine", "/fake/model", [ayah]
                ))

        assert result["answer"] == "إجابة GPTQ"
        assert result["category"] == "medicine"
        assert len(result["ayahs"]) == 1

    def test_gptq_solution_no_ayahs(self):
        import asyncio
        from services.ai_service import _get_gptq_solution

        with patch("services.ai_service.settings") as mock_settings:
            mock_settings.GPTQ_USE_TRITON = False
            with patch("services.gptq_service.generate", return_value="إجابة فارغة"):
                result = asyncio.run(_get_gptq_solution(
                    "سؤال", "general", "/fake/model", []
                ))

        assert result["ayahs"] == []
        assert result["category"] == "general"
    """اختبار مسار GPTQ Fallback في get_quran_solution."""

    def test_gptq_called_when_path_set(self):
        from services.ai_service import get_quran_solution

        with patch.dict(os.environ, {"OPENAI_API_KEY": "", "GPTQ_MODEL_PATH": "/fake/model"}):
            with patch("services.ai_service.settings") as mock_settings:
                mock_settings.GPTQ_MODEL_PATH = "/fake/model"
                mock_settings.GPTQ_USE_TRITON = False
                with patch("services.ai_service._get_gptq_solution", new_callable=__import__("unittest.mock", fromlist=["AsyncMock"]).AsyncMock) as mock_gptq:
                    mock_gptq.return_value = {
                        "answer": "رد من GPTQ",
                        "category": "medicine",
                        "ayahs": [],
                        "practical_steps": [],
                    }
                    result = asyncio.run(get_quran_solution("ما الشفاء؟", "medicine"))

        assert result["answer"] == "رد من GPTQ"

    def test_gptq_failure_falls_back_to_demo(self):
        from services.ai_service import get_quran_solution

        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            with patch("services.ai_service.settings") as mock_settings:
                mock_settings.GPTQ_MODEL_PATH = "/fake/model"
                mock_settings.GPTQ_USE_TRITON = False
                with patch("services.ai_service._get_gptq_solution", new_callable=__import__("unittest.mock", fromlist=["AsyncMock"]).AsyncMock) as mock_gptq:
                    mock_gptq.side_effect = RuntimeError("CUDA error")
                    result = asyncio.run(get_quran_solution("ما الشفاء؟", "medicine"))

        assert "answer" in result
        assert result["category"] == "medicine"


# ---------------------------------------------------------------------------
# tafsir_service — uncovered branch
# ---------------------------------------------------------------------------


class TestTafsirService:
    def test_get_tafsir_all_returns_all_scholars(self):
        from services.tafsir_service import get_tafsir
        result = get_tafsir(1, "all")
        assert len(result) == 3
        scholar_names = [r["scholar_name"] for r in result]
        assert "Ibn Kathir" in scholar_names
        assert "Al-Tabari" in scholar_names
        assert "Al-Qurtubi" in scholar_names

    def test_get_tafsir_filter_by_scholar_arabic(self):
        from services.tafsir_service import get_tafsir
        result = get_tafsir(1, "ابن كثير")
        assert len(result) == 1
        assert result[0]["scholar_name_ar"] == "ابن كثير"

    def test_get_tafsir_filter_nonexistent_scholar(self):
        from services.tafsir_service import get_tafsir
        result = get_tafsir(1, "عالم وهمي")
        assert result == []

    def test_get_tafsir_injects_ayah_id(self):
        from services.tafsir_service import get_tafsir
        result = get_tafsir(42, "all")
        for r in result:
            assert r["ayah_id"] == 42

    def test_get_available_scholars_returns_4(self):
        from services.tafsir_service import get_available_scholars
        scholars = get_available_scholars()
        assert len(scholars) == 4
        names = [s["name"] for s in scholars]
        assert "Ibn Kathir" in names
        assert "Al-Saadi" in names

    def test_get_available_scholars_has_arabic_names(self):
        from services.tafsir_service import get_available_scholars
        scholars = get_available_scholars()
        for s in scholars:
            assert "name_ar" in s
            assert any(ord(c) > 0x0600 for c in s["name_ar"])

    def test_get_available_scholars_has_source(self):
        from services.tafsir_service import get_available_scholars
        scholars = get_available_scholars()
        for s in scholars:
            assert "source" in s
            assert len(s["source"]) > 0


class TestTafsirEndpoint:
    def test_get_tafsir_endpoint(self, client):
        response = client.get("/api/tafsir/1")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_tafsir_with_scholar_filter(self, client):
        response = client.get("/api/tafsir/1?scholar=ابن كثير")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["scholar_name_ar"] == "ابن كثير"

    def test_get_scholars_endpoint(self, client):
        response = client.get("/api/tafsir/scholars")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 4

    def test_tafsir_response_has_required_fields(self, client):
        response = client.get("/api/tafsir/1")
        assert response.status_code == 200
        for item in response.json():
            assert "scholar_name_ar" in item
            assert "text" in item
            assert "source" in item
            assert "ayah_id" in item


# ---------------------------------------------------------------------------
# gptq_service — _build_pipeline success path (fully mocked)
# ---------------------------------------------------------------------------


class TestGPTQBuildPipelineSuccess:
    def test_build_pipeline_success(self):
        """اختبار مسار _build_pipeline عند نجاح التحميل."""
        import services.gptq_service as gptq_service
        gptq_service.reset_pipeline()

        mock_tokenizer = MagicMock()
        mock_model = MagicMock()
        mock_pipe = MagicMock()
        mock_pipe.return_value = [{"generated_text": "test output"}]

        mock_hf_logging = MagicMock()
        mock_hf_logging.CRITICAL = 50

        mock_transformers = MagicMock()
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_transformers.pipeline.return_value = mock_pipe
        mock_transformers.logging = mock_hf_logging

        mock_auto_gptq = MagicMock()
        mock_auto_gptq.AutoGPTQForCausalLM.from_quantized.return_value = mock_model

        with patch.dict(sys.modules, {
            "transformers": mock_transformers,
            "auto_gptq": mock_auto_gptq,
        }):
            result = gptq_service._build_pipeline("fake/model", False)

        assert result is mock_pipe
        mock_transformers.AutoTokenizer.from_pretrained.assert_called_once_with("fake/model", use_fast=True)
        mock_auto_gptq.AutoGPTQForCausalLM.from_quantized.assert_called_once()

        gptq_service.reset_pipeline()
