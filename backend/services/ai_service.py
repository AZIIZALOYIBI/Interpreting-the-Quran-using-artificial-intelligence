"""
AI Service — Handles AI-powered Quranic guidance.
Falls back to demo responses when API keys are not configured.
"""

import os
from typing import Optional

try:
    from openai import AsyncOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

from data.quran_data import QURAN_VERSES
from data.categories_data import CATEGORY_PROMPTS

DEMO_MODE = not os.getenv("OPENAI_API_KEY")

DEMO_RESPONSES = {
    "medicine": {
        "answer": "القرآن الكريم يقدم إرشادات شاملة حول الصحة والعافية. يشير القرآن إلى أهمية الاعتدال في الأكل والشرب، كما يؤكد على الطهارة والنظافة كأساس للصحة. يقول الله تعالى: ﴿وَكُلُوا وَاشْرَبُوا وَلَا تُسْرِفُوا﴾ (الأعراف: 31). كما يشير القرآن إلى العسل كشفاء: ﴿يَخْرُجُ مِن بُطُونِهَا شَرَابٌ مُّخْتَلِفٌ أَلْوَانُهُ فِيهِ شِفَاءٌ لِّلنَّاسِ﴾ (النحل: 69). والقرآن نفسه وُصف بأنه شفاء: ﴿وَنُنَزِّلُ مِنَ الْقُرْآنِ مَا هُوَ شِفَاءٌ وَرَحْمَةٌ لِّلْمُؤْمِنِينَ﴾ (الإسراء: 82).",
        "related_topics": ["الصحة النفسية", "الغذاء الصحي", "الطهارة", "العسل والشفاء", "الصبر على المرض"],
        "tafsir_notes": ["الاعتدال في الطعام والشراب من أعظم أسباب الصحة كما أشار إليه العلماء", "وصف القرآن بالشفاء يشمل شفاء القلوب والأبدان عند كثير من المفسرين", "العسل ثبت علمياً أنه يحتوي على مضادات حيوية طبيعية ومضادات أكسدة"],
    },
    "business": {
        "answer": "يضع القرآن الكريم أسساً متينة للتجارة والعمل المبني على الصدق والأمانة. يقول الله تعالى: ﴿يَا أَيُّهَا الَّذِينَ آمَنُوا لَا تَأْكُلُوا أَمْوَالَكُم بَيْنَكُم بِالْبَاطِلِ إِلَّا أَن تَكُونَ تِجَارَةً عَن تَرَاضٍ مِّنكُمْ﴾ (النساء: 29). كما يؤكد على الوفاء بالعقود: ﴿يَا أَيُّهَا الَّذِينَ آمَنُوا أَوْفُوا بِالْعُقُودِ﴾ (المائدة: 1).",
        "related_topics": ["التجارة الحلال", "الأمانة", "الوفاء بالعقود", "الربا", "الزكاة"],
        "tafsir_notes": ["التراضي في التجارة أساس المعاملات الإسلامية كما أكد المفسرون", "آية الدين (البقرة 282) هي أطول آية في القرآن وتفصل أحكام التوثيق المالي", "النهي عن أكل المال بالباطل يشمل الغش والتدليس وجميع أشكال الظلم المالي"],
    },
    "general": {
        "answer": "القرآن الكريم كتاب هداية شامل يقدم إرشادات لجميع جوانب الحياة. يقول الله تعالى: ﴿إِنَّ هَٰذَا الْقُرْآنَ يَهْدِي لِلَّتِي هِيَ أَقْوَمُ﴾ (الإسراء: 9). ويقول أيضاً: ﴿وَنَزَّلْنَا عَلَيْكَ الْكِتَابَ تِبْيَانًا لِّكُلِّ شَيْءٍ وَهُدًى وَرَحْمَةً وَبُشْرَىٰ لِلْمُسْلِمِينَ﴾ (النحل: 89).",
        "related_topics": ["التدبر", "الهداية", "الحكمة", "الرحمة", "العلم"],
        "tafsir_notes": ["القرآن يهدي للتي هي أقوم في جميع شؤون الحياة الدينية والدنيوية", "التبيان لكل شيء يعني أن القرآن يشمل أصول كل ما يحتاجه الإنسان من هداية", "التدبر هو التأمل العميق في معاني الآيات واستخراج الحكم والعبر منها"],
    },
    "family": {
        "answer": "يولي القرآن الكريم اهتماماً كبيراً بالأسرة باعتبارها نواة المجتمع. يقول الله تعالى: ﴿وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا لِّتَسْكُنُوا إِلَيْهَا وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً﴾ (الروم: 21).",
        "related_topics": ["الزواج", "بر الوالدين", "تربية الأبناء", "صلة الرحم", "المودة والرحمة"],
        "tafsir_notes": ["السكن والمودة والرحمة ثلاثة أركان أساسية للحياة الزوجية في الإسلام", "بر الوالدين قُرن بالتوحيد مما يدل على عظم مكانته في الإسلام", "التربية في الإسلام تشمل الجانب الروحي والعلمي والأخلاقي والبدني"],
    },
    "science": {
        "answer": "يحث القرآن الكريم على العلم والتعلم والتفكر في الكون. يقول الله تعالى: ﴿اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ﴾ (العلق: 1) - وهي أول آية نزلت. ويقول: ﴿قُلْ هَلْ يَسْتَوِي الَّذِينَ يَعْلَمُونَ وَالَّذِينَ لَا يَعْلَمُونَ﴾ (الزمر: 9).",
        "related_topics": ["طلب العلم", "التفكر في الخلق", "المعجزات العلمية", "العقل والتفكير"],
        "tafsir_notes": ["أول كلمة نزلت من القرآن هي 'اقرأ' مما يدل على مكانة العلم في الإسلام", "رفع القرآن مكانة العلماء وجعل العلم طريقاً إلى خشية الله", "الدعوة للنظر والتأمل في المخلوقات هي أساس المنهج العلمي التجريبي"],
    },
    "self-development": {
        "answer": "يقدم القرآن الكريم منهجاً متكاملاً لتطوير الذات وتزكية النفس. يقول الله تعالى: ﴿قَدْ أَفْلَحَ مَن زَكَّاهَا ● وَقَدْ خَابَ مَن دَسَّاهَا﴾ (الشمس: 9-10). ويحث على الصبر: ﴿يَا أَيُّهَا الَّذِينَ آمَنُوا اصْبِرُوا وَصَابِرُوا﴾ (آل عمران: 200).",
        "related_topics": ["تزكية النفس", "الصبر", "التوكل", "الإيجابية", "التغيير"],
        "tafsir_notes": ["تزكية النفس هي تطهيرها من الرذائل وتحليتها بالفضائل", "الصبر في الإسلام ثلاثة أنواع: صبر على الطاعة، وعن المعصية، وعلى أقدار الله", "التوكل لا يعني ترك الأسباب بل الأخذ بها مع تعليق القلب بالله"],
    },
    "law": {
        "answer": "يؤسس القرآن الكريم لمبادئ العدل والمساواة بين الناس. يقول الله تعالى: ﴿إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ وَالْإِحْسَانِ﴾ (النحل: 90). ويأمر بالشهادة بالحق: ﴿يَا أَيُّهَا الَّذِينَ آمَنُوا كُونُوا قَوَّامِينَ بِالْقِسْطِ شُهَدَاءَ لِلَّهِ وَلَوْ عَلَىٰ أَنفُسِكُمْ﴾ (النساء: 135).",
        "related_topics": ["العدل", "المساواة", "حقوق الإنسان", "الشورى", "الحقوق والواجبات"],
        "tafsir_notes": ["العدل في الإسلام مطلوب حتى مع الأعداء كما أمر القرآن", "الشهادة بالحق واجبة ولو كانت على النفس أو الأقارب", "مبدأ الشورى في القرآن يؤسس لحكم رشيد قائم على المشاركة"],
    },
    "environment": {
        "answer": "يدعو القرآن الكريم إلى الحفاظ على البيئة وعدم الإفساد في الأرض. يقول الله تعالى: ﴿وَلَا تُفْسِدُوا فِي الْأَرْضِ بَعْدَ إِصْلَاحِهَا﴾ (الأعراف: 56). ويخبر عن عواقب الفساد: ﴿ظَهَرَ الْفَسَادُ فِي الْبَرِّ وَالْبَحْرِ بِمَا كَسَبَتْ أَيْدِي النَّاسِ﴾ (الروم: 41).",
        "related_topics": ["حماية البيئة", "الماء", "عدم الإسراف", "الخلافة في الأرض", "النظام البيئي"],
        "tafsir_notes": ["الإنسان مستخلف في الأرض ومسؤول عن حفظها وعمارتها", "الإفساد في الأرض يشمل التلوث وتدمير الموارد الطبيعية", "القرآن ربط بين أعمال الإنسان السيئة وظهور الفساد في البر والبحر"],
    },
}


async def get_ai_response(question: str, category: str = "general") -> dict:
    if DEMO_MODE or not HAS_OPENAI:
        return _get_demo_response(question, category)
    try:
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        system_prompt = CATEGORY_PROMPTS.get(category, CATEGORY_PROMPTS["general"])
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": question}],
            temperature=0.7,
            max_tokens=2000,
        )
        answer_text = response.choices[0].message.content
        relevant_verses = _find_relevant_verses(question)
        return {
            "answer": answer_text,
            "verses": relevant_verses,
            "category": category,
            "confidence": 0.85,
            "related_topics": _get_related_topics(category),
            "tafsir_notes": _get_tafsir_notes(category),
        }
    except Exception as e:
        print(f"AI Error: {e}")
        return _get_demo_response(question, category)


def _get_demo_response(question: str, category: str) -> dict:
    cat_data = DEMO_RESPONSES.get(category, DEMO_RESPONSES["general"])
    relevant_verses = _find_relevant_verses(question)
    return {
        "answer": cat_data["answer"],
        "verses": relevant_verses,
        "category": category,
        "confidence": 0.92,
        "related_topics": cat_data["related_topics"],
        "tafsir_notes": cat_data["tafsir_notes"],
    }


def _find_relevant_verses(question: str) -> list:
    keywords = question.split()
    relevant = []
    for verse in QURAN_VERSES:
        for keyword in keywords:
            if len(keyword) > 2 and keyword in verse.get("text_simple", ""):
                relevant.append(verse)
                break
    if relevant:
        return relevant[:5]
    return QURAN_VERSES[:3]


def _get_related_topics(category: str) -> list:
    data = DEMO_RESPONSES.get(category, DEMO_RESPONSES["general"])
    return data.get("related_topics", [])


def _get_tafsir_notes(category: str) -> list:
    data = DEMO_RESPONSES.get(category, DEMO_RESPONSES["general"])
    return data.get("tafsir_notes", [])
