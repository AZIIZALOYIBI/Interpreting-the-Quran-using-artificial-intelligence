"""
AI Service — Handles AI-powered Quranic guidance.

Provider priority (highest → lowest):
  1. vLLM server (GLM-4.7-FP8) — set VLLM_BASE_URL in environment
  2. OpenAI API             — set OPENAI_API_KEY in environment
  3. Local GPTQ model       — set GPTQ_MODEL_PATH in environment
  4. Demo / fallback        — always available, uses real Quran corpus
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

from config import settings
from services import gptq_service
from services.quran_text_service import Ayah, search_ayahs

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Category keywords — used for automatic question classification
# ---------------------------------------------------------------------------

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "medicine": ["صحة", "طب", "مرض", "علاج", "شفاء", "دواء", "جسم", "غذاء", "صيام", "صيدلة", "حمية"],
    "work": ["عمل", "مال", "رزق", "تجارة", "كسب", "ربا", "اقتصاد", "وظيفة", "أموال", "راتب", "مهنة", "بيع"],
    "science": ["علم", "بحث", "تكنولوجيا", "اكتشاف", "عقل", "تفكر", "كون", "فلك", "خلق", "طبيعة", "كيمياء"],
    "family": ["أسرة", "زواج", "والدين", "أبناء", "أولاد", "رحم", "نساء", "مودة", "أسرتي", "أم", "أب", "طفل"],
    "self_development": ["نفس", "تطوير", "صبر", "شكر", "توكل", "إيمان", "تغيير", "هدف", "شخصية", "تحفيز", "إرادة"],
    "law": ["عدل", "حق", "قانون", "حكم", "شريعة", "قضاء", "حلال", "حرام", "ظلم", "عقوبة", "حقوق"],
    "environment": ["بيئة", "أرض", "طبيعة", "ماء", "شجر", "حيوان", "فساد", "حفاظ", "نبات", "تلوث", "مناخ"],
    "ethics": ["أخلاق", "صدق", "أمانة", "كذب", "غيبة", "حسد", "كرم", "عفو", "تواضع", "قيم", "فضيلة"],
    "general": ["قرآن", "إسلام", "دين", "سؤال", "إرشاد", "هداية", "حياة"],
}

# ---------------------------------------------------------------------------
# Practical steps per category (included in every response)
# ---------------------------------------------------------------------------

_PRACTICAL_STEPS: dict[str, list[str]] = {
    "medicine": [
        "استشر طبيبًا مختصًا لأي حالة طبية",
        "الحفاظ على النظام الغذائي الصحي المعتدل",
        "الدعاء بالشفاء والتوكل على الله مع الأخذ بالأسباب",
        "الاهتمام بالصحة النفسية والروحية جنبًا إلى جنب مع البدنية",
    ],
    "work": [
        "احرص على الكسب الحلال في جميع معاملاتك",
        "الوفاء بالعقود والالتزامات المهنية",
        "إتقان العمل والتفاني فيه كعبادة",
        "إخراج الزكاة والصدقة من الرزق الحلال",
    ],
    "science": [
        "السعي الدائم في طلب العلم والمعرفة",
        "التفكر في آيات الله في الكون",
        "الجمع بين العلم الشرعي والعلوم الطبيعية",
        "نشر العلم النافع ومشاركته مع الآخرين",
    ],
    "family": [
        "تعزيز الحوار والمودة بين أفراد الأسرة",
        "بر الوالدين والحفاظ على صلة الرحم",
        "التربية الإسلامية القائمة على القدوة الحسنة",
        "حل النزاعات الأسرية بالحكمة والرفق",
    ],
    "self_development": [
        "مداومة الذكر والدعاء لتقوية الصلة بالله",
        "وضع أهداف واضحة ومراجعتها باستمرار",
        "الصبر على المصاعب واعتبارها فرصًا للنمو",
        "قراءة سير الصالحين واستلهام العبر منها",
    ],
    "law": [
        "التحلي بالعدل في جميع معاملاتك",
        "الدفاع عن الحق وإقامة الشهادة بالصدق",
        "احترام حقوق الآخرين وأداء الواجبات",
        "اللجوء إلى أهل العلم والخبرة في المسائل المعقدة",
    ],
    "environment": [
        "ترشيد استهلاك الموارد الطبيعية كالماء والطاقة",
        "تجنب الإسراف والتبذير في جميع جوانب الحياة",
        "المشاركة في مبادرات حماية البيئة المحلية",
        "تعليم الأجيال القادمة قيمة الحفاظ على الأرض",
    ],
    "ethics": [
        "الالتزام بالصدق والأمانة في القول والفعل",
        "تجنب الغيبة والنميمة وسائر آفات اللسان",
        "التواضع ونبذ الكبر والغرور",
        "العفو والصفح عند المقدرة والتسامح مع الآخرين",
    ],
    "general": [
        "تدبر آيات القرآن الكريم يوميًا",
        "الرجوع إلى العلماء الثقات في الأمور الدينية",
        "تطبيق القيم القرآنية في الحياة اليومية",
        "المداومة على الاستغفار والذكر",
    ],
}

_DISCLAIMER = (
    "هذا الرد للتوجيه العام فقط وليس فتوى شرعية. "
    "يُرجى الرجوع إلى العلماء المختصين في المسائل الدينية الدقيقة."
)

_SYSTEM_PROMPT = (
    "أنت مساعد قرآني متخصص يُجيب باللغة العربية الفصحى.\n"
    "يجب أن تستند في إجاباتك إلى آيات القرآن الكريم مع ذكر اسم السورة ورقم الآية.\n"
    "لا تخترع آيات غير موجودة في القرآن الكريم.\n"
    "قدم خطوات عملية قابلة للتطبيق في الحياة اليومية.\n\n"
    "الفئة: {category}\n\n"
    "الآيات المرجعية:\n{context}"
)


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------


def classify_question(question: str) -> str:
    """Return the best matching category for *question* based on keyword overlap."""
    if not question:
        return "general"
    words = question.split()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if category == "general":
            continue
        for keyword in keywords:
            for word in words:
                # Exact match OR substring match for keywords ≥ 3 chars (avoids
                # false positives from very short Arabic function words).
                if keyword == word or (len(keyword) >= 3 and keyword in word):
                    return category
    return "general"


def _format_ayah_context(ayahs: List[Ayah]) -> str:
    """Render *ayahs* as a numbered Arabic context block for AI prompts."""
    if not ayahs:
        return "لم يُعثَر على آيات مطابقة."
    lines: list[str] = []
    for ayah in ayahs:
        lines.append(
            f"الآية {ayah.ayah_number} من سورة {ayah.surah_name_ar} ({ayah.surah_name_en}):"
        )
        lines.append(ayah.text)
        lines.append("")
    return "\n".join(lines)


def _build_demo_response(question: str, category: str, ayahs: List[Ayah]) -> dict:
    """Construct a demo response using real Quran corpus data (no AI required)."""
    if not ayahs:
        answer = (
            f"بخصوص سؤالك: {question}\n\n"
            "لم يُعثَر على آيات قرآنية مطابقة مباشرة لهذا السؤال. "
            "يُنصح بالرجوع إلى العلماء والمفسرين المتخصصين."
        )
        return {
            "answer": answer,
            "category": category,
            "ayahs": [],
            "practical_steps": _PRACTICAL_STEPS.get(category, _PRACTICAL_STEPS["general"]),
            "disclaimer": _DISCLAIMER,
        }

    parts: list[str] = [f"بخصوص سؤالك: {question}\n"]
    parts.append("إليك ما وجدناه في القرآن الكريم المتعلق بموضوع سؤالك:\n")
    for ayah in ayahs:
        parts.append(
            f"• سورة {ayah.surah_name_ar} ({ayah.surah_name_en})، الآية {ayah.ayah_number}:"
        )
        parts.append(f"  ﴿{ayah.text}﴾\n")

    return {
        "answer": "\n".join(parts),
        "category": category,
        "ayahs": [a.to_dict() for a in ayahs],
        "practical_steps": _PRACTICAL_STEPS.get(category, _PRACTICAL_STEPS["general"]),
        "disclaimer": _DISCLAIMER,
    }


# ---------------------------------------------------------------------------
# Provider-specific solution helpers
# ---------------------------------------------------------------------------


async def _get_vllm_solution(
    question: str,
    category: str,
    base_url: str,
    model_name: str,
    ayahs: List[Ayah],
) -> dict:
    """Query a vLLM server (OpenAI-compatible) for a Quranic guidance answer.

    The server is expected to be started with::

        vllm serve zai-org/GLM-4.7-FP8 \\
            --tensor-parallel-size 4 \\
            --speculative-config.method mtp \\
            --speculative-config.num_speculative_tokens 1 \\
            --tool-call-parser glm47 \\
            --reasoning-parser glm45 \\
            --enable-auto-tool-choice \\
            --served-model-name glm-4.7-fp8
    """
    from openai import AsyncOpenAI  # lazy import — not required unless vLLM is used

    client = AsyncOpenAI(api_key="EMPTY", base_url=base_url)
    context = _format_ayah_context(ayahs)
    system_prompt = _SYSTEM_PROMPT.format(category=category, context=context)

    response = await client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.7,
        max_tokens=2000,
    )
    answer = response.choices[0].message.content or ""
    return {
        "answer": answer,
        "category": category,
        "ayahs": [a.to_dict() for a in ayahs],
        "practical_steps": _PRACTICAL_STEPS.get(category, _PRACTICAL_STEPS["general"]),
        "disclaimer": _DISCLAIMER,
    }


async def _get_openai_solution(
    question: str,
    category: str,
    api_key: str,
    ayahs: List[Ayah],
) -> dict:
    """Query OpenAI for a Quranic guidance answer."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)
    context = _format_ayah_context(ayahs)
    system_prompt = _SYSTEM_PROMPT.format(category=category, context=context)

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.7,
        max_tokens=2000,
    )
    answer = response.choices[0].message.content or ""
    return {
        "answer": answer,
        "category": category,
        "ayahs": [a.to_dict() for a in ayahs],
        "practical_steps": _PRACTICAL_STEPS.get(category, _PRACTICAL_STEPS["general"]),
        "disclaimer": _DISCLAIMER,
    }


async def _get_gptq_solution(
    question: str,
    category: str,
    model_path: str,
    ayahs: List[Ayah],
) -> dict:
    """Generate an answer using a locally loaded GPTQ model."""
    context = _format_ayah_context(ayahs)
    query = f"{question}\n\nالسياق القرآني:\n{context}"
    answer = gptq_service.generate(
        query=query,
        model_path=model_path,
        use_triton=settings.GPTQ_USE_TRITON,
    )
    return {
        "answer": answer,
        "category": category,
        "ayahs": [a.to_dict() for a in ayahs],
        "practical_steps": _PRACTICAL_STEPS.get(category, _PRACTICAL_STEPS["general"]),
        "disclaimer": _DISCLAIMER,
    }


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


async def get_quran_solution(
    question: str,
    category: Optional[str] = None,
) -> dict:
    """Return a Quranic guidance answer for *question*.

    Provider priority:
      vLLM (GLM-4.7-FP8) → OpenAI → GPTQ → Demo fallback

    When *category* is ``None`` or ``"general"`` the question is automatically
    classified using keyword matching before searching the corpus.
    """
    if not category or category == "general":
        category = classify_question(question)

    ayahs = search_ayahs(question, category)

    # 1. vLLM server (GLM-4.7-FP8 or any OpenAI-compatible model)
    vllm_url = os.getenv("VLLM_BASE_URL", "")
    if vllm_url:
        vllm_model = os.getenv("VLLM_MODEL_NAME", "glm-4.7-fp8")
        try:
            return await _get_vllm_solution(question, category, vllm_url, vllm_model, ayahs)
        except Exception as exc:
            logger.error("vLLM error — falling back to next provider: %s", exc)

    # 2. OpenAI API
    openai_key = os.getenv("OPENAI_API_KEY", "")
    if openai_key:
        try:
            return await _get_openai_solution(question, category, openai_key, ayahs)
        except Exception as exc:
            logger.error("OpenAI error — falling back to next provider: %s", exc)

    # 3. Local GPTQ model
    gptq_path = os.getenv("GPTQ_MODEL_PATH", "")
    if gptq_path:
        try:
            return await _get_gptq_solution(question, category, gptq_path, ayahs)
        except Exception as exc:
            logger.error("GPTQ error — falling back to demo mode: %s", exc)

    # 4. Demo / corpus-only fallback
    return _build_demo_response(question, category, ayahs)
