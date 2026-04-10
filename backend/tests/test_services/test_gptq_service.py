"""
اختبارات وحدة لخدمة gptq_service (WizardCoder GPTQ).
جميع الاستدعاءات لـ auto-gptq وtransformers مُستبدلة بـ mock لتجنب الحاجة إلى GPU.
"""
import sys
import os
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import services.gptq_service as gptq_service


@pytest.fixture(autouse=True)
def reset_singleton():
    """أعد تعيين حالة الـ singleton قبل كل اختبار."""
    gptq_service.reset_pipeline()
    yield
    gptq_service.reset_pipeline()


def _make_mock_pipe(generated_text: str):
    """بناء mock لـ pipeline يُرجع نصاً محدداً."""
    pipe = MagicMock()
    pipe.return_value = [{"generated_text": generated_text}]
    return pipe


class TestGenerateStripsPrompt:
    def test_returns_only_assistant_text(self):
        """يجب أن تُزيل generate بادئة الـ prompt وتُرجع النص الفعلي فقط."""
        answer = "الإسلام يحث على الصحة والوقاية."
        prompt_prefix = (
            "<|system|>\n"
            + gptq_service._SYSTEM_PROMPT
            + "\n<|end|>\n<|user|>\nسؤال<|end|>\n<|assistant|>"
        )
        mock_pipe = _make_mock_pipe(prompt_prefix + answer)

        with patch.object(gptq_service, "get_pipeline", return_value=mock_pipe):
            result = gptq_service.generate(
                query="سؤال",
                model_path="fake/model",
            )

        assert result == answer

    def test_full_text_returned_when_no_prefix(self):
        """إذا لم يبدأ النص بالـ prompt، يُرجع النص كاملاً."""
        answer = "إجابة مباشرة."
        mock_pipe = _make_mock_pipe(answer)

        with patch.object(gptq_service, "get_pipeline", return_value=mock_pipe):
            result = gptq_service.generate(
                query="سؤال",
                model_path="fake/model",
            )

        assert result == answer

    def test_pipeline_called_with_correct_eos_token(self):
        """يجب استدعاء pipeline بـ eos_token_id الصحيح."""
        mock_pipe = _make_mock_pipe("إجابة")

        with patch.object(gptq_service, "get_pipeline", return_value=mock_pipe):
            gptq_service.generate(query="سؤال", model_path="fake/model")

        call_kwargs = mock_pipe.call_args[1]
        assert call_kwargs["eos_token_id"] == gptq_service._EOS_TOKEN_ID

    def test_pipeline_called_with_do_sample(self):
        """يجب أن يكون do_sample=True لضمان التنوع في الإجابات."""
        mock_pipe = _make_mock_pipe("إجابة")

        with patch.object(gptq_service, "get_pipeline", return_value=mock_pipe):
            gptq_service.generate(query="سؤال", model_path="fake/model")

        call_kwargs = mock_pipe.call_args[1]
        assert call_kwargs["do_sample"] is True


class TestGetPipelineSingleton:
    def test_pipeline_loaded_once(self):
        """يجب تحميل الـ pipeline مرة واحدة فقط."""
        mock_pipe = _make_mock_pipe("test")

        with patch.object(gptq_service, "_build_pipeline", return_value=mock_pipe) as mock_build:
            p1 = gptq_service.get_pipeline("fake/model")
            p2 = gptq_service.get_pipeline("fake/model")

        assert p1 is p2
        mock_build.assert_called_once()

    def test_load_error_propagates_on_retry(self):
        """إذا فشل التحميل، يجب أن يُعيد رفع الخطأ عند الاستدعاء التالي."""
        with patch.object(
            gptq_service, "_build_pipeline", side_effect=RuntimeError("فشل التحميل")
        ):
            with pytest.raises(RuntimeError):
                gptq_service.get_pipeline("fake/model")

        # الاستدعاء الثاني يجب أن يرفع خطأ أيضاً (من _load_error المخزّن)
        with pytest.raises(RuntimeError):
            gptq_service.get_pipeline("fake/model")


class TestBuildPipelineImportError:
    def test_import_error_raises_friendly_message(self):
        """غياب auto-gptq يجب أن يُنتج ImportError بمساعد نصي واضح."""
        import builtins
        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name in ("auto_gptq", "transformers"):
                raise ImportError("No module named '%s'" % name)
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            with pytest.raises(ImportError, match="auto-gptq"):
                gptq_service._build_pipeline("fake/model", False)


class TestResetPipeline:
    def test_reset_clears_state(self):
        """reset_pipeline يجب أن يُفرغ الـ pipeline والخطأ المخزّن."""
        mock_pipe = _make_mock_pipe("test")

        with patch.object(gptq_service, "_build_pipeline", return_value=mock_pipe):
            gptq_service.get_pipeline("fake/model")

        gptq_service.reset_pipeline()
        assert gptq_service._pipeline is None
        assert gptq_service._load_error is None
