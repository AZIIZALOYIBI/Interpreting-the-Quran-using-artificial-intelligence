"""
خدمة الاستدلال المحلي باستخدام WizardCoder-GPTQ عبر auto-gptq وtransformers.

يتم تحميل النموذج بشكل كسول (lazy) عند أول استخدام ويُعاد استخدامه بعد ذلك.
يتطلب بيئة CUDA ومكتبتي ``auto-gptq`` و``transformers``.

تفعيل: اضبط متغير البيئة ``GPTQ_MODEL_PATH`` باسم النموذج على HuggingFace
أو بمسار محلي، مثلاً::

    GPTQ_MODEL_PATH=TheBloke/WizardCoder-15B-1.0-GPTQ

النموذج الافتراضي: TheBloke/WizardCoder-15B-1.0-GPTQ
"""
from __future__ import annotations

import logging
import threading
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prompt template for WizardCoder (StarCoder-based chat format)
# EOS token ID 49155 marks the end of a turn.
# ---------------------------------------------------------------------------
_PROMPT_TEMPLATE = "<|system|>\n{system}\n<|end|>\n<|user|>\n{query}<|end|>\n<|assistant|>"
_EOS_TOKEN_ID = 49155

_SYSTEM_PROMPT = (
    "أنت مساعد قرآني متخصص يُجيب باللغة العربية الفصحى فقط. "
    "يجب أن تستند في إجاباتك إلى آيات القرآن الكريم مع ذكر اسم السورة ورقم الآية. "
    "لا تخترع آيات غير موجودة في القرآن الكريم. "
    "قدم خطوات عملية قابلة للتطبيق في الحياة اليومية."
)

# ---------------------------------------------------------------------------
# Singleton state protected by a lock
# ---------------------------------------------------------------------------
_lock = threading.Lock()
_pipeline: Optional[Any] = None
_load_error: Optional[str] = None


def _build_pipeline(model_path: str, use_triton: bool) -> Any:
    """Load WizardCoder GPTQ model and return a text-generation pipeline."""
    try:
        from transformers import AutoTokenizer, pipeline, logging as hf_logging
        from auto_gptq import AutoGPTQForCausalLM
    except ImportError as exc:
        raise ImportError(
            "مكتبات auto-gptq وtransformers غير مثبتة. "
            "ثبّتها باستخدام: pip install auto-gptq transformers"
        ) from exc

    logger.info("تحميل نموذج GPTQ من: %s (triton=%s)", model_path, use_triton)

    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
    model = AutoGPTQForCausalLM.from_quantized(
        model_path,
        use_safetensors=True,
        device="cuda:0",
        use_triton=use_triton,
        quantize_config=None,
    )

    # Suppress spurious transformers warnings when used inside a pipeline
    hf_logging.set_verbosity(hf_logging.CRITICAL)

    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    logger.info("تم تحميل نموذج GPTQ بنجاح")
    return pipe


def get_pipeline(model_path: str, use_triton: bool = False) -> Any:
    """Return the shared text-generation pipeline, loading it on first call."""
    global _pipeline, _load_error

    with _lock:
        if _pipeline is not None:
            return _pipeline
        if _load_error is not None:
            raise RuntimeError(_load_error)

        try:
            _pipeline = _build_pipeline(model_path, use_triton)
            return _pipeline
        except Exception as exc:
            _load_error = str(exc)
            logger.error("فشل تحميل نموذج GPTQ: %s", exc, exc_info=True)
            raise


def reset_pipeline() -> None:
    """Release the loaded pipeline (used in tests)."""
    global _pipeline, _load_error
    with _lock:
        _pipeline = None
        _load_error = None


def generate(
    query: str,
    model_path: str,
    use_triton: bool = False,
    max_new_tokens: int = 512,
    temperature: float = 0.2,
    top_k: int = 50,
    top_p: float = 0.95,
) -> str:
    """Generate an Arabic Quranic guidance answer using the local GPTQ model.

    Args:
        query: The user's question (already Arabic).
        model_path: HuggingFace repo ID or local path to the GPTQ model.
        use_triton: Enable Triton kernels for faster inference.
        max_new_tokens: Maximum tokens to generate.
        temperature: Sampling temperature.
        top_k: Top-k sampling parameter.
        top_p: Nucleus sampling probability.

    Returns:
        The generated text (everything after the assistant prompt).
    """
    pipe = get_pipeline(model_path, use_triton)
    prompt = _PROMPT_TEMPLATE.format(system=_SYSTEM_PROMPT, query=query)

    outputs = pipe(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        eos_token_id=_EOS_TOKEN_ID,
    )

    full_text: str = outputs[0]["generated_text"]
    # Both `prompt` and `full_text` are Python str (Unicode) objects, so slicing
    # by len(prompt) is character-accurate even for multi-codepoint Arabic text.
    if full_text.startswith(prompt):
        return full_text[len(prompt):].strip()
    return full_text.strip()
