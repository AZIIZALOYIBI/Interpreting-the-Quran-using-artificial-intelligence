---
name: github-actions-failure-debugging
description: دليل لتشخيص وإصلاح أخطاء GitHub Actions في هذا المستودع. استخدمه عند طلب إصلاح Workflows فاشلة أو مشاكل في CI/CD.
---

# إصلاح أخطاء GitHub Actions

لإصلاح workflows فاشلة في هذا المستودع، اتبع هذه الخطوات:

## 1. اكتشاف المشكلة

استخدم `list_workflow_runs` للبحث عن آخر التشغيلات الفاشلة:

```
list_workflow_runs(repo, status="failed")
```

ثم استخدم `get_job_logs` أو `summarize_job_log_failures` لفهم سبب الفشل.

## 2. الأسباب الشائعة في هذا المستودع

### مشاكل الـ Frontend (Next.js)
- فشل `npm ci` بسبب تعارض في `package-lock.json`
- أخطاء TypeScript أو ESLint في مرحلة `npm run lint`
- فشل `npm run build` بسبب متغيرات بيئة مفقودة (مثل `NEXT_PUBLIC_API_URL`)
- تعذّر تشغيل standalone server على المنفذ 3000

### مشاكل الـ Backend (Python/FastAPI)
- تعارض في إصدارات المكتبات في `requirements.txt`
- أخطاء import بسبب module مفقود
- فشل الاتصال بـ PostgreSQL أو Redis أو Pinecone

### مشاكل Docker
- فشل `docker-compose up` بسبب port conflict
- image غير موجودة أو تحتاج إعادة بناء

## 3. إجراءات الإصلاح

### للـ Frontend:
```bash
cd frontend
npm ci                          # إعادة تثبيت الحزم
npm run lint                    # فحص أخطاء ESLint
npm run build                   # التحقق من نجاح البناء
```

### للـ Backend:
```bash
cd backend
pip install -r requirements.txt
python -m pytest                # تشغيل الاختبارات
uvicorn main:app --reload       # التحقق من تشغيل التطبيق
```

## 4. التحقق من الإصلاح

- تأكد من أن smoke tests تنجح: homepage تعيد HTTP 200
- تحقق من أن الصفحة تحتوي على النص العربي: `حلول الحياة من القرآن الكريم`
- أعد تشغيل الـ workflow بعد الإصلاح للتأكد
