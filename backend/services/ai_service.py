import os
from typing import Dict, Any, List, Optional
from data.sample_ayahs import SAMPLE_AYAHS

CATEGORY_KEYWORDS = {
    "medicine": ["طب", "صحة", "مرض", "علاج", "شفاء", "دواء", "صيام", "غذاء", "جسم"],
    "work": ["عمل", "مال", "رزق", "تجارة", "وظيفة", "ربح", "خسارة", "اقتصاد", "بيع", "شراء"],
    "science": ["علم", "بحث", "اكتشاف", "تكنولوجيا", "فلك", "فيزياء", "كيمياء", "رياضيات"],
    "family": ["أسرة", "زواج", "طلاق", "أطفال", "والدين", "أبناء", "زوج", "زوجة", "مجتمع"],
    "self_development": ["نفس", "تطوير", "إيمان", "صبر", "شكر", "تفكير", "عقل", "إرادة", "هدف"],
    "law": ["عدل", "قانون", "حق", "حكم", "قضاء", "حلال", "حرام", "فتوى", "شريعة"],
    "environment": ["بيئة", "طبيعة", "أرض", "ماء", "نبات", "حيوان", "إفساد", "حفاظ"],
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
    question_lower = question.lower()
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in question_lower:
                scores[category] += 1
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "general"


async def get_quran_solution(question: str, category: Optional[str] = None) -> Dict[str, Any]:
    if not category:
        category = classify_question(question)

    # Try OpenAI if key is available
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and api_key != "your_openai_api_key_here":
        try:
            return await _get_openai_solution(question, category, api_key)
        except Exception:
            pass

    # Fallback to mock response
    response = MOCK_RESPONSES.get(category, DEFAULT_RESPONSE).copy()
    response["answer"] = f"بناءً على سؤالك: \"{question}\"\n\n" + response["answer"]
    return response


async def _get_openai_solution(question: str, category: str, api_key: str) -> Dict[str, Any]:
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=api_key)

    system_prompt = f"""أنت مساعد قرآني متخصص يساعد المسلمين في إيجاد الإرشاد والتوجيه من القرآن الكريم.
مجال تخصصك الآن: {category}
يجب أن تُجيب باللغة العربية الفصحى.
أذكر الآيات القرآنية ذات الصلة مع ذكر اسم السورة ورقم الآية.
قدم خطوات عملية مستوحاة من التعاليم الإسلامية."""

    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        max_tokens=1000,
    )

    answer = completion.choices[0].message.content or ""
    return {
        "answer": answer,
        "category": category,
        "ayahs": SAMPLE_AYAHS.get(category, []),
        "practical_steps": [],
    }
