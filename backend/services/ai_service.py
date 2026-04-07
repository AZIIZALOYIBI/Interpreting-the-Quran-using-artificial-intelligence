import logging
import os
from typing import Any, Dict, List, Optional

from data.sample_ayahs import SAMPLE_AYAHS

logger = logging.getLogger(__name__)

CATEGORY_KEYWORDS = {
    "medicine": ["طب", "صحة", "مرض", "علاج", "شفاء", "دواء", "صيام", "غذاء", "جسم"],
    "work": ["عمل", "مال", "رزق", "تجارة", "وظيفة", "ربح", "خسارة", "اقتصاد", "بيع", "شراء"],
    "science": ["علم", "بحث", "اكتشاف", "تكنولوجيا", "فلك", "فيزياء", "كيمياء", "رياضيات"],
    "family": ["أسرة", "زواج", "طلاق", "أطفال", "والدين", "أبناء", "زوج", "زوجة", "مجتمع"],
    "self_development": ["نفس", "تطوير", "إيمان", "صبر", "شكر", "تفكير", "عقل", "إرادة", "هدف"],
    "law": ["عدل", "قانون", "حق", "حكم", "قضاء", "حلال", "حرام", "فتوى", "شريعة"],
    "environment": ["بيئة", "طبيعة", "أرض", "ماء", "نبات", "حيوان", "إفساد", "حفاظ"],
    "ethics": ["أخلاق", "خلق", "تواضع", "كرم", "صدق", "أمانة", "عفو", "كبر", "غيبة", "حسد"],
}

MOCK_RESPONSES = {
    "medicine": {
        "answer": """القرآن الكريم يرشدنا في موضوع الصحة والطب بشكل شامل ومتكامل.

الله سبحانه وتعالى هو الشافي الحقيقي، والطب وسيلة من وسائل الأخذ بالأسباب التي أمرنا الله بها.

يُرشدنا القرآن إلى:
• أن الشفاء بيد الله وحده، والطب أسباب نأخذ بها
• الوقاية خير من العلاج (الصيام، الأكل المعتدل)
• أن بعض الأغذية كالعسل فيها شفاء للناس
• أهمية نظافة الجسم والبدن في الإسلام""",
        "category": "medicine",
        "ayahs": SAMPLE_AYAHS.get("medicine", []),
        "practical_steps": [
            "الأخذ بالعلاج مع التوكل على الله",
            "الصيام لما له من فوائد صحية ثابتة",
            "تناول الغذاء الصحي والمعتدل",
            "الدعاء بالشفاء والتضرع إلى الله",
            "عدم الإسراف في الأكل والشرب",
        ],
    },
    "work": {
        "answer": """القرآن الكريم يحث على العمل والكسب الحلال ويُرشد إلى إدارة المال بحكمة.

الإسلام دين العمل والإنتاج، ويعدّ الكسب الحلال من أفضل العبادات عندما تصاحبه النية الصالحة.

الإسلام يرشدنا إلى:
• الكسب من الحلال وتجنب الحرام (الربا، الغش، الاحتكار)
• الانتشار في الأرض وابتغاء رزق الله
• الأمانة والصدق في التعامل
• الإنفاق في وجوه الخير""",
        "category": "work",
        "ayahs": SAMPLE_AYAHS.get("work", []),
        "practical_steps": [
            "السعي في طلب الرزق بعد الصلاة",
            "الابتعاد عن الربا وكل كسب محرم",
            "الصدق والأمانة في كل المعاملات",
            "إخراج الزكاة والصدقة لتبارك في المال",
            "الادخار والتخطيط المالي الحكيم",
        ],
    },
    "science": {
        "answer": """القرآن الكريم يحث على طلب العلم والتفكر في آيات الله في الكون.

أول كلمة نزلت في القرآن كانت "اقرأ"، مما يدل على منزلة العلم والمعرفة في الإسلام.

القرآن يرشدنا إلى:
• أن طلب العلم فريضة على كل مسلم
• التفكر في خلق الله والتأمل في الكون
• الإعجاز العلمي الذي يدل على صدق القرآن
• أن العلم والإيمان لا تعارض بينهما""",
        "category": "science",
        "ayahs": SAMPLE_AYAHS.get("science", []),
        "practical_steps": [
            "القراءة والتعلم المستمر في شتى العلوم",
            "التفكر في آيات الله في الكون والطبيعة",
            "الجمع بين العلم الشرعي والعلم التجريبي",
            "نشر العلم النافع والمشاركة في البحث",
            "توظيف العلم في خدمة الإنسانية",
        ],
    },
    "family": {
        "answer": """القرآن الكريم يُرسي منظومة أسرية متكاملة مبنية على المودة والرحمة والمسؤولية.

الأسرة في الإسلام هي النواة الأساسية للمجتمع، ويُوليها القرآن الكريم عناية بالغة.

القرآن يرشدنا إلى:
• أن الزواج آية من آيات الله وسكينة ومودة
• وجوب بر الوالدين والإحسان إليهما
• التربية الإيمانية للأبناء
• حل النزاعات الأسرية بالحكمة والحسنى""",
        "category": "family",
        "ayahs": SAMPLE_AYAHS.get("family", []),
        "practical_steps": [
            "بناء الأسرة على الود والرحمة والاحترام",
            "بر الوالدين والإحسان إليهما دائماً",
            "تربية الأبناء على القرآن والأخلاق الحميدة",
            "حل الخلافات بالحوار الهادئ والحكمة",
            "صلة الرحم والحفاظ على الروابط الأسرية",
        ],
    },
    "law": {
        "answer": """القرآن الكريم يُقيم منظومة عدل شاملة تكفل حقوق الجميع وتُحدد الواجبات.

العدل في الإسلام ليس مجرد مبدأ قانوني، بل هو قيمة إيمانية عليا يأمر بها القرآن بشكل مطلق.

القرآن يرشدنا إلى:
• وجوب إقامة العدل ولو على النفس والأقارب
• حفظ حقوق الإنسان والكرامة الإنسانية
• تحريم الظلم والاعتداء على حقوق الآخرين
• الشورى والتشاور في اتخاذ القرارات""",
        "category": "law",
        "ayahs": SAMPLE_AYAHS.get("law", []),
        "practical_steps": [
            "إقامة العدل في التعامل مع الجميع",
            "أداء الحقوق لأصحابها كاملةً غير منقوصة",
            "التشاور واحترام آراء الآخرين",
            "الابتعاد عن الظلم والاعتداء",
            "الرجوع إلى أهل العلم في المسائل الفقهية",
        ],
    },
    "environment": {
        "answer": """القرآن الكريم يجعل الإنسان خليفة في الأرض مسؤولاً عن صونها وعمارتها.

الحفاظ على البيئة في الإسلام واجب ديني، ويُعدّ الإفساد في الأرض من كبائر الذنوب.

القرآن يرشدنا إلى:
• أن الإنسان مستخلف في الأرض ومسؤول عنها
• النهي الصريح عن الإفساد في الأرض
• أن الماء أصل كل حياة ويجب المحافظة عليه
• الاعتدال وعدم الإسراف في استخدام الموارد""",
        "category": "environment",
        "ayahs": SAMPLE_AYAHS.get("environment", []),
        "practical_steps": [
            "الحفاظ على الماء والموارد الطبيعية",
            "الابتعاد عن كل ما يُفسد البيئة أو يُلوّثها",
            "زراعة الأشجار وتشجير الأماكن الجرداء",
            "ترشيد الاستهلاك وتجنب الإسراف",
            "التوعية البيئية في المجتمع",
        ],
    },
    "ethics": {
        "answer": """القرآن الكريم يُرسي منظومة أخلاقية متكاملة تُسمو بالإنسان وتُعلي من شأنه.

الأخلاق الحسنة في الإسلام ليست مجرد آداب اجتماعية، بل هي قيم إيمانية أمر بها القرآن الكريم.

القرآن يرشدنا إلى:
• أن التواضع والرحمة من أسمى الصفات
• تحريم الكبر والغرور والسخرية من الآخرين
• الصدق والأمانة في القول والعمل
• العفو والتسامح وإصلاح ذات البين""",
        "category": "ethics",
        "ayahs": SAMPLE_AYAHS.get("ethics", []),
        "practical_steps": [
            "التحلي بالتواضع والابتعاد عن الكبر",
            "الصدق في القول والوفاء بالعهد",
            "العفو عن المسيئين والتسامح معهم",
            "الابتعاد عن الغيبة والنميمة وسوء الظن",
            "التخلق بأخلاق القرآن في كل الأحوال",
        ],
    },
    "self_development": {
        "answer": """القرآن الكريم يدعو إلى تطوير النفس وبناء الشخصية المتكاملة في جميع جوانبها.

التطوير الذاتي في الإسلام شامل للروح والعقل والجسد، ويرتكز على القيم الإسلامية الراسخة.

القرآن يرشدنا إلى:
• مراجعة النفس والمحاسبة المستمرة
• التعلم وطلب العلم في كل الأحوال
• الصبر على المصاعب وشكر النعم
• التوكل على الله مع الأخذ بالأسباب""",
        "category": "self_development",
        "ayahs": SAMPLE_AYAHS.get("self_development", []),
        "practical_steps": [
            "محاسبة النفس يومياً قبل النوم",
            "قراءة القرآن وتدبره كل يوم",
            "طلب العلم النافع في الدنيا والآخرة",
            "الصحبة الصالحة التي تُعين على الخير",
            "التخطيط للمستقبل مع التوكل على الله",
        ],
    },
}

DEFAULT_RESPONSE = {
    "answer": """القرآن الكريم يُرشدنا في جميع شؤون الحياة بشكل شامل ومتكامل.

قال تعالى: ﴿وَنَزَّلْنَا عَلَيْكَ الْكِتَابَ تِبْيَانًا لِّكُلِّ شَيْءٍ﴾ [النحل: 89]

القرآن الكريم كتاب هداية شاملة يتناول جميع جوانب الحياة الإنسانية، من الجانب الروحي إلى الاجتماعي إلى الاقتصادي والعلمي.

للحصول على إرشاد أكثر تخصصاً، يُنصح بالرجوع إلى تفسيرات العلماء المتخصصين.""",
    "category": "general",
    "ayahs": [],
    "practical_steps": [
        "قراءة القرآن الكريم بتدبر وتأمل",
        "الرجوع إلى تفسيرات العلماء الموثوقين",
        "سؤال أهل العلم في المسائل الدقيقة",
        "تطبيق التعاليم الإسلامية في الحياة اليومية",
    ],
}


def classify_question(question: str) -> str:
    """Classify a question into one of the known categories using keyword matching.

    Args:
        question: The Arabic question text to classify.

    Returns:
        The category ID string (e.g. "medicine") or "general" when no match.
    """
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
    """Return a Quranic guidance response for the given question.

    Tries OpenAI GPT-3.5-turbo when ``OPENAI_API_KEY`` is configured; falls
    back to pre-built mock responses otherwise.

    Args:
        question: The user's question (5–2000 chars).
        category: Optional category ID.  Auto-classified when omitted.

    Returns:
        A dict containing ``answer``, ``category``, ``ayahs``, and
        ``practical_steps`` keys.
    """
    if not category:
        category = classify_question(question)
        logger.debug("Auto-classified question to category: %s", category)

    # Try OpenAI if key is available
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key:
        try:
            logger.info("Using OpenAI for category: %s", category)
            return await _get_openai_solution(question, category, api_key)
        except Exception as exc:
            logger.warning("OpenAI call failed, falling back to mock: %s", exc)

    # Fallback to mock response
    logger.debug("Returning mock response for category: %s", category)
    response = MOCK_RESPONSES.get(category, DEFAULT_RESPONSE).copy()
    response["answer"] = f"بناءً على سؤالك: \"{question}\"\n\n" + response["answer"]
    return response


async def _get_openai_solution(
    question: str, category: str, api_key: str
) -> Dict[str, Any]:
    """Fetch a Quranic guidance answer from OpenAI GPT-3.5-turbo.

    Args:
        question: The user's question.
        category: The resolved category ID.
        api_key: A valid OpenAI API key.

    Returns:
        Response dict with ``answer``, ``category``, ``ayahs``, and
        ``practical_steps``.
    """
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)

    system_prompt = f"""أنت مساعد قرآني متخصص يساعد المسلمين في إيجاد الإرشاد والتوجيه من القرآن الكريم.
مجال تخصصك الآن: {category}

قواعد يجب الالتزام بها:
1. أجب باللغة العربية الفصحى دائماً.
2. اذكر الآيات القرآنية بنصها الكامل مع اسم السورة ورقم الآية.
3. لا تخترع أو تنسب آيات غير موجودة في القرآن الكريم. إن لم تجد آية مناسبة، قل ذلك صراحةً.
4. قدم تفسيراً مختصراً مستنداً إلى كبار المفسرين (ابن كثير، الطبري، السعدي).
5. أضف خطوات عملية قابلة للتطبيق في الحياة اليومية.
6. اختتم بتنبيه بأن هذا للتوجيه العام، وأن المسائل الدقيقة تستوجب الرجوع إلى العلماء.
7. لا تُفتِ في المسائل الشرعية المعقدة."""

    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        max_tokens=1200,
        temperature=0.5,
    )

    answer = completion.choices[0].message.content or ""
    return {
        "answer": answer,
        "category": category,
        "ayahs": SAMPLE_AYAHS.get(category, []),
        "practical_steps": [],
    }
