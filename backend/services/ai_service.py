"""
خدمة الذكاء الاصطناعي — توجيه قرآني بمصادر حقيقية وتعليمات صارمة.

ترتيب الأولوية:
  1. OpenAI GPT-3.5-turbo (إن وُجد OPENAI_API_KEY)
  2. نموذج GPTQ المحلي      (إن وُجد GPTQ_MODEL_PATH)
  3. بحث مباشر في نص القرآن (وضع Demo — بدون أي تعليق مُخترَع)

في جميع الأحوال تُستخدم الآيات من مصحف محلي موثَّق (6236 آية).
لا يُولَّد أي نص باسم الآيات من خارج هذا المصحف.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

from config import settings
from services.quran_text_service import Ayah, search_ayahs

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Category keyword classifier (unchanged)
# ---------------------------------------------------------------------------

CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "medicine":        ["طب", "صحة", "مرض", "علاج", "شفاء", "دواء", "صيام", "غذاء", "جسم"],
    "work":            ["عمل", "مال", "رزق", "تجارة", "وظيفة", "ربح", "خسارة", "اقتصاد", "بيع", "شراء"],
    "science":         ["علم", "بحث", "اكتشاف", "تكنولوجيا", "فلك", "فيزياء", "كيمياء", "رياضيات"],
    "family":          ["أسرة", "زواج", "طلاق", "أطفال", "والدين", "أبناء", "زوج", "زوجة", "مجتمع"],
    "self_development":["نفس", "تطوير", "إيمان", "صبر", "شكر", "تفكير", "عقل", "إرادة", "هدف"],
    "law":             ["عدل", "قانون", "حق", "حكم", "قضاء", "حلال", "حرام", "فتوى", "شريعة"],
    "environment":     ["بيئة", "طبيعة", "أرض", "ماء", "نبات", "حيوان", "إفساد", "حفاظ"],
    "ethics":          ["أخلاق", "خلق", "تواضع", "كرم", "صدق", "أمانة", "عفو", "كبر", "غيبة", "حسد"],
}

# ---------------------------------------------------------------------------
# Strict system prompt — shared by all AI backends
# ---------------------------------------------------------------------------

_STRICT_SYSTEM_PROMPT = """\
أنت مساعد قرآني متخصص. مهمتك الوحيدة هي تقديم الإرشاد من القرآن الكريم.

══════════════════════════════════════════
⚠️  تعليمات صارمة لا يمكن تجاوزها:
══════════════════════════════════════════

1. لا تذكر أي آية قرآنية إلا إذا كانت مدرجة حرفياً في قائمة [الآيات المُرجَعة] أدناه.
2. لا تخترع أرقام سور أو أرقام آيات أو أسماء سور غير موجودة في القائمة.
3. اقتبس نص الآيات حرفياً كما هو في القائمة دون أي تعديل أو زيادة.
4. إن لم تجد آية مناسبة في القائمة المقدمة، قل بصراحة:
   "لم أجد آية مقيدة بموضوع سؤالك في النتائج المتاحة، أنصحك بالرجوع إلى عالم متخصص."
5. لا تُفتِ في المسائل الشرعية المعقدة.
6. أجب باللغة العربية الفصحى دائماً.
7. يجب أن تذكر اسم السورة ورقم الآية مع كل اقتباس.
8. لا تزيد عدد الآيات المُستشهَد بها على ما هو في القائمة.
9. اختتم دائماً بتنبيه أن هذا للتوجيه العام ولا يُغني عن الرجوع إلى العلماء.

{ayah_context}
"""

_AYAH_CONTEXT_TEMPLATE = """\
══════════════════════════════════════════
[الآيات المُرجَعة من مصحف موثَّق — هذه هي الآيات الوحيدة التي يمكنك الاستشهاد بها]
══════════════════════════════════════════
{ayah_list}
══════════════════════════════════════════"""


def _format_ayah_context(ayahs: List[Ayah]) -> str:
    if not ayahs:
        return (
            "[الآيات المُرجَعة]\n"
            "لم يُعثَر على آيات ذات صلة مباشرة. "
            "أخبر المستخدم بذلك بصراحة."
        )
    lines = []
    for i, a in enumerate(ayahs, 1):
        lines.append(
            f"{i}. ﴿{a.text}﴾\n"
            f"   — سورة {a.surah_name_ar} ({a.surah_name_en})، الآية {a.ayah_number}"
        )
    return _AYAH_CONTEXT_TEMPLATE.format(ayah_list="\n".join(lines))


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------


def classify_question(question: str) -> str:
    """Classify a question into one of the known categories using keyword matching."""
    question_lower = question.lower()
    scores: Dict[str, int] = {cat: 0 for cat in CATEGORY_KEYWORDS}
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in question_lower:
                scores[category] += 1
    best: str = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "general"


async def get_quran_solution(
    question: str, category: Optional[str] = None
) -> Dict[str, Any]:
    """Return a Quranic guidance response grounded in the real Quran corpus.

    Priority:
      1. OpenAI (if OPENAI_API_KEY is set)
      2. Local GPTQ model (if GPTQ_MODEL_PATH is set)
      3. Direct Quran search result (no AI commentary)

    In all cases the ayahs are fetched from the local verified corpus.

    Args:
        question: The user's question (5–2000 chars).
        category: Optional category ID.  Auto-classified when omitted.

    Returns:
        Dict with ``answer``, ``category``, ``ayahs``, and ``practical_steps``.
    """
    if not category:
        category = classify_question(question)
        logger.debug("Auto-classified question to category: %s", category)

    # Fetch real ayahs from the corpus — used as context in ALL paths
    found_ayahs = search_ayahs(question, category=category, top_k=5)
    logger.info(
        "Quran search for '%s' (category=%s): %d ayahs found",
        question[:60],
        category,
        len(found_ayahs),
    )

    # Try OpenAI
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key:
        try:
            logger.info("Using OpenAI for category: %s", category)
            return await _get_openai_solution(question, category, api_key, found_ayahs)
        except Exception as exc:
            logger.warning("OpenAI call failed, falling back to GPTQ/demo: %s", exc)

    # Try local GPTQ
    gptq_model_path = settings.GPTQ_MODEL_PATH.strip()
    if gptq_model_path:
        try:
            logger.info("Using GPTQ model '%s' for category: %s", gptq_model_path, category)
            return await _get_gptq_solution(question, category, gptq_model_path, found_ayahs)
        except Exception as exc:
            logger.warning("GPTQ call failed, falling back to demo: %s", exc)

    # Demo fallback — present real Quran results without AI commentary
    return _build_demo_response(question, category, found_ayahs)


# ---------------------------------------------------------------------------
# AI backends
# ---------------------------------------------------------------------------


async def _get_openai_solution(
    question: str,
    category: str,
    api_key: str,
    found_ayahs: List[Ayah],
) -> Dict[str, Any]:
    """Call OpenAI with strict anti-hallucination instructions."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)
    ayah_context = _format_ayah_context(found_ayahs)
    system_prompt = _STRICT_SYSTEM_PROMPT.format(ayah_context=ayah_context)

    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        max_tokens=1200,
        temperature=0.3,   # Lower temperature → less hallucination
    )

    answer = completion.choices[0].message.content or ""
    return {
        "answer": answer,
        "category": category,
        "ayahs": [a.to_dict() for a in found_ayahs],
        "practical_steps": [],
    }


async def _get_gptq_solution(
    question: str,
    category: str,
    model_path: str,
    found_ayahs: List[Ayah],
) -> Dict[str, Any]:
    """Call local GPTQ model with strict anti-hallucination instructions."""
    import asyncio
    from services import gptq_service

    ayah_context = _format_ayah_context(found_ayahs)
    full_query = (
        f"{question}\n\n"
        f"[التعليمات الصارمة]\n"
        f"استخدم فقط الآيات التالية من القرآن الكريم ولا تخترع غيرها:\n{ayah_context}"
    )

    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(
        None,
        lambda: gptq_service.generate(
            query=full_query,
            model_path=model_path,
            use_triton=settings.GPTQ_USE_TRITON,
        ),
    )

    return {
        "answer": answer,
        "category": category,
        "ayahs": [a.to_dict() for a in found_ayahs],
        "practical_steps": [],
    }


def _build_demo_response(
    question: str,
    category: str,
    found_ayahs: List[Ayah],
) -> Dict[str, Any]:
    """Build a response using only verified Quran search results (no AI text)."""
    if not found_ayahs:
        answer = (
            f"بناءً على سؤالك: \"{question}\"\n\n"
            "لم يُعثَر على آيات قرآنية مرتبطة مباشرةً بهذا السؤال في قاعدة البيانات المتاحة.\n\n"
            "⚠️ للحصول على إجابة دقيقة وموثَّقة، يُرجى الرجوع إلى عالم متخصص أو "
            "مراجعة كتب التفسير المعتمدة مثل تفسير ابن كثير أو تفسير السعدي."
        )
    else:
        lines = [f"بناءً على سؤالك: \"{question}\"\n\nإليك الآيات القرآنية ذات الصلة من المصحف الكريم:\n"]
        for a in found_ayahs:
            lines.append(
                f"• ﴿{a.text}﴾\n"
                f"  — سورة {a.surah_name_ar} ({a.surah_name_en})، الآية {a.ayah_number}\n"
            )
        lines.append(
            "\n⚠️ هذه الآيات مُستخرَجة مباشرةً من المصحف الكريم. "
            "للتفسير الدقيق والإرشاد الشرعي، يُرجى الرجوع إلى العلماء المتخصصين."
        )
        answer = "\n".join(lines)

    return {
        "answer": answer,
        "category": category,
        "ayahs": [a.to_dict() for a in found_ayahs],
        "practical_steps": [
            "مراجعة تفسير الآيات في كتب التفسير المعتمدة",
            "الرجوع إلى عالم متخصص للإرشاد الشرعي الدقيق",
            "قراءة القرآن الكريم بتدبر وتأمل",
        ],
    }
