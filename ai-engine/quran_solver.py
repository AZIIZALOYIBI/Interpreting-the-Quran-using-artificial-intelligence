"""
QuranSolver: Main AI class for finding Quranic solutions to life questions.
"""
import os
from typing import Optional, List, Dict, Any
from prompts.domain_prompts import DOMAIN_PROMPTS, SYSTEM_PROMPT_TEMPLATE
from data.scientific_miracles_map import SCIENTIFIC_MIRACLES_MAP

CATEGORY_KEYWORDS = {
    "medicine": ["طب", "صحة", "مرض", "علاج", "شفاء", "دواء"],
    "work": ["عمل", "مال", "رزق", "تجارة", "وظيفة", "ربح"],
    "science": ["علم", "بحث", "اكتشاف", "تكنولوجيا", "فلك"],
    "family": ["أسرة", "زواج", "طلاق", "أطفال", "والدين"],
    "self_development": ["نفس", "تطوير", "إيمان", "صبر", "شكر"],
    "law": ["عدل", "قانون", "حق", "حكم", "شريعة"],
    "environment": ["بيئة", "طبيعة", "أرض", "ماء", "إفساد"],
    "ethics": ["أخلاق", "خلق", "تواضع", "صدق", "أمانة", "عفو", "كبر", "غيبة"],
}


class QuranSolver:
    def __init__(self, openai_api_key: Optional[str] = None):
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY", "")
        self.client = None
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                pass

    def classify_question(self, question: str) -> str:
        question_lower = question.lower()
        scores: Dict[str, int] = {cat: 0 for cat in CATEGORY_KEYWORDS}
        for category, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in question_lower:
                    scores[category] += 1
        best = max(scores, key=lambda k: scores[k])
        return best if scores[best] > 0 else "general"

    def get_quran_solution(
        self,
        question: str,
        category: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not category:
            category = self.classify_question(question)

        if self.client:
            try:
                return self._openai_solution(question, category)
            except Exception as e:
                print(f"OpenAI error: {e}")

        return self._fallback_solution(question, category)

    def _openai_solution(self, question: str, category: str) -> Dict[str, Any]:
        domain_prompt = DOMAIN_PROMPTS.get(category, DOMAIN_PROMPTS["general"])
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(domain_prompt=domain_prompt)

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            max_tokens=1200,
            temperature=0.7,
        )

        answer = response.choices[0].message.content or ""
        return {
            "question": question,
            "category": category,
            "answer": answer,
            "ayahs": [],
            "practical_steps": [],
            "source": "openai",
        }

    def _fallback_solution(self, question: str, category: str) -> Dict[str, Any]:
        return {
            "question": question,
            "category": category,
            "answer": f"""القرآن الكريم يرشدنا في موضوع سؤالك: "{question}"

قال تعالى: ﴿وَنَزَّلْنَا عَلَيْكَ الْكِتَابَ تِبْيَانًا لِّكُلِّ شَيْءٍ﴾ [النحل: 89]

يُرشدنا القرآن الكريم في مجال {category} بشكل شامل ومتكامل.
للحصول على إرشاد أدق، يُنصح بالرجوع إلى العلماء المتخصصين.""",
            "ayahs": [],
            "practical_steps": [
                "قراءة القرآن الكريم بتدبر وتأمل",
                "الرجوع إلى تفسيرات العلماء الموثوقين",
                "سؤال أهل العلم في المسائل الدقيقة",
            ],
            "source": "fallback",
        }

    def get_scientific_miracles(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        if category and category in SCIENTIFIC_MIRACLES_MAP:
            return SCIENTIFIC_MIRACLES_MAP[category]
        all_miracles = []
        for cat_miracles in SCIENTIFIC_MIRACLES_MAP.values():
            all_miracles.extend(cat_miracles)
        return all_miracles
