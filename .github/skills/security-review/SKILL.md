---
name: security-review
description: دليل لمراجعة الأمان في هذا المستودع. استخدمه عند طلب فحص الكود أمنياً أو قبل إصدار نسخة جديدة.
---

# مراجعة أمان منصة القرآن الكريم بالذكاء الاصطناعي

## نقاط الفحص الأمني الأساسية

### 1. إدارة مفاتيح API والأسرار

- [ ] تأكد من أن `.env` مُدرج في `.gitignore` ولا يُرفع إلى المستودع
- [ ] تحقق من أن `.env.example` لا يحتوي على مفاتيح حقيقية
- [ ] تأكد من أن `OPENAI_API_KEY` و`PINECONE_API_KEY` لا تظهر في الكود
- [ ] راجع GitHub Secrets للتأكد من إعدادها بشكل صحيح

```bash
# فحص الأسرار المسربة
git log --all --full-history -- "*.env"
grep -r "sk-" . --include="*.py" --include="*.ts"
grep -r "OPENAI_API_KEY\s*=" . --include="*.py"
```

### 2. أمان FastAPI Backend

- [ ] التحقق من صحة المدخلات (Pydantic schemas)
- [ ] CORS مُعرَّف بشكل محدود (ليس `*` في الإنتاج)
- [ ] Rate limiting على endpoints الـ AI
- [ ] عدم تسريب stack traces في responses الإنتاج

```python
# التحقق من إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # وليس ["*"]
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
```

### 3. أمان قاعدة البيانات

- [ ] استخدام ORM (SQLAlchemy) وعدم كتابة SQL خام
- [ ] كلمات مرور PostgreSQL قوية في `.env`
- [ ] عدم تشغيل قاعدة البيانات بصلاحيات root

### 4. أمان الـ Frontend (Next.js)

- [ ] عدم تضمين مفاتيح API في كود الـ client (متغيرات `NEXT_PUBLIC_` تكون مرئية)
- [ ] التحقق من المدخلات قبل إرسالها إلى الـ Backend
- [ ] استخدام Content Security Policy headers

### 5. أمان Docker

- [ ] عدم تشغيل containers بصلاحيات root
- [ ] المنافذ المكشوفة محددة (لا تكشف PostgreSQL على الإنترنت)
- [ ] استخدام `.dockerignore` لاستبعاد الملفات الحساسة

## الأدوات المستخدمة

```bash
# فحص ثغرات Python
pip install safety
safety check -r backend/requirements.txt

# فحص ثغرات Node.js
cd frontend && npm audit

# فحص أمني بـ Bandit
pip install bandit
bandit -r backend/
```

## مستوى الخطورة والتصنيف

| المستوى | الإجراء |
|---------|---------|
| Critical | إصلاح فوري قبل أي merge |
| High | إصلاح قبل إصدار النسخة |
| Medium | إصلاح في الدورة القادمة |
| Low | توثيق والإصلاح عند الفرصة |
