---
name: quran-ai-development
description: دليل متخصص لتطوير منصة القرآن الكريم بالذكاء الاصطناعي. استخدمه عند إضافة ميزات AI جديدة أو تحسين محرك البحث والإجابات القرآنية.
---

# تطوير منصة القرآن الكريم بالذكاء الاصطناعي

## هيكل المشروع

```
.
├── frontend/          # Next.js 14 + TypeScript + Tailwind CSS (RTL)
├── backend/           # Python FastAPI
│   ├── routers/       # ask-quran, categories, miracles, search
│   ├── services/      # business logic
│   └── data/          # static Quran data
├── ai-engine/         # LangChain + OpenAI RAG pipeline
│   ├── quran_solver.py
│   ├── prompts/       # domain-specific prompts per category
│   └── data/          # miracle maps
└── database/          # PostgreSQL schema
```

## إضافة فئة إسلامية جديدة

الفئات الحالية: `medicine`, `work`, `science`, `family`, `self-development`, `law`, `environment`, `general`

لإضافة فئة جديدة:

1. **أضف الفئة في الـ Backend** (`backend/data/categories.py`):
```python
NEW_CATEGORY = {
    "id": "ethics",
    "name": "الأخلاق",
    "name_en": "Ethics",
    "icon": "⚖️",
    "description": "الأخلاق الإسلامية والقيم القرآنية"
}
```

2. **أنشئ Prompt خاصاً** (`ai-engine/prompts/ethics.txt`):
```
أنت مساعد متخصص في الأخلاق الإسلامية من القرآن الكريم.
ابحث في الآيات القرآنية المتعلقة بالأخلاق والقيم.
قدم إجابات مبنية على الآيات مع ذكر رقم السورة والآية.
```

3. **أضف الفئة في الـ Frontend** (`frontend/src/types/index.ts`):
```typescript
type Category = 'medicine' | 'work' | 'science' | 'family' |
                'self-development' | 'law' | 'environment' |
                'general' | 'ethics';  // أضف هنا
```

## تحسين جودة إجابات AI

### مبادئ الـ Prompts الجيدة للمحتوى القرآني:

1. **الدقة الدينية**: دائماً اطلب من النموذج ذكر رقم السورة والآية
2. **التعدد**: اطلب إجابات من عدة مفسرين (تفسير ابن كثير، الطبري، السعدي)
3. **التحقق**: اطلب من النموذج التأكيد على صحة الآيات قبل إرسالها
4. **الإخلاء**: دائماً اشمل تنبيه بأن هذا للتوجيه وليس فتوى شرعية

### مثال على Prompt محسّن:

```python
QURAN_PROMPT = """
أنت مساعد متخصص في تفسير القرآن الكريم.

السؤال: {question}
الفئة: {category}

التعليمات:
1. ابحث في القرآن الكريم عن آيات ذات صلة بالموضوع
2. اذكر الآيات بالنص الكامل مع رقم السورة والآية
3. قدم تفسيراً مختصراً من كبار المفسرين
4. وضح الحكمة والإرشاد القرآني للسؤال المطروح
5. اختتم بتنبيه بأن هذا للتوجيه العام فقط

ملاحظة مهمة: لا تخترع آيات. إذا لم تجد آية مناسبة، قل ذلك صراحةً.
"""
```

## أفضل ممارسات الـ Frontend العربي

```typescript
// دائماً استخدم dir="rtl" للمحتوى العربي
<div dir="rtl" className="font-arabic text-right">
  {arabicContent}
</div>

// استخدم خط مناسب للقرآن (مثل Amiri أو Uthmanic)
className="font-['Amiri'] text-xl leading-loose"

// للأرقام العربية
const arabicNumerals = (n: number) =>
  n.toString().replace(/\d/g, d => '٠١٢٣٤٥٦٧٨٩'[+d]);
```

## وضع Demo Mode

المنصة تعمل بدون API keys في وضع Demo. عند تطوير ميزة جديدة:

```python
# في backend/services/
class NewService:
    def __init__(self, demo_mode: bool = False):
        self.demo_mode = demo_mode

    def process(self, query: str):
        if self.demo_mode:
            return self._get_demo_response(query)
        return self._call_ai_api(query)

    def _get_demo_response(self, query: str):
        # إرجاع استجابة نموذجية مسبقة التجهيز
        return DEMO_RESPONSES.get("default")
```

## اختبار المحتوى العربي

```python
# تأكد دائماً من اختبار النصوص العربية
def test_arabic_content():
    response = client.post("/api/ask-quran", json={
        "question": "ما معنى الصبر في القرآن؟"
    })
    assert response.status_code == 200
    data = response.json()
    # تحقق من وجود محتوى عربي في الإجابة
    assert any(ord(c) > 0x0600 for c in data["answer"])
```
