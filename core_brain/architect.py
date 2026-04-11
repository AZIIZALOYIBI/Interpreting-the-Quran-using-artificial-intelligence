"""
العقل الثاني: المعماري (Architect)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
يُحوِّل متطلب المستخدم (Issue) + سياق المشروع (ProjectContext)
إلى مخطط معماري دقيق (Blueprint) يصف:
  - أي ملفات يجب تعديلها أو إنشاؤها.
  - ماذا يجب أن يحتوي كل ملف.
  - ترتيب التعديلات لتفادي التعارضات.

يستخدم GPT-4o مع استجابة JSON منظَّمة.

🧬 يدمج الذاكرة الجينية:
  قبل أي استدعاء لـ GPT-4o، يستعلم الذاكرة عن أخطاء سابقة مشابهة
  ويُدرجها في الـ prompt كـ "قواعد لا تكسرها".
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from typing import Literal

from openai import OpenAI

from analyst import ProjectContext
from memory import GeneticMemory

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────
# نماذج البيانات
# ──────────────────────────────────────────────────────────

FileAction = Literal["create", "update", "delete"]


@dataclass
class FileChange:
    """وصف تعديل ملف واحد."""

    file_path: str
    action: FileAction
    description: str          # وصف التغيير بالعربية للـ PR body
    expected_content_hint: str  # ملخص ما يجب أن يحتويه الملف


@dataclass
class Blueprint:
    """المخطط المعماري الكامل للحل."""

    task_summary: str
    rationale: str                            # سبب اختيار هذه الخطوات
    file_changes: list[FileChange] = field(default_factory=list)
    test_strategy: str = ""                   # كيف يجب اختبار الحل
    risks: str = ""                           # مخاطر محتملة

    def to_markdown(self) -> str:
        """يُنتج وصف PR بصيغة Markdown."""
        lines = [
            f"## 📋 المهمة\n{self.task_summary}",
            f"## 🏗️ المنطق المعماري\n{self.rationale}",
            "## 📂 الملفات المعدَّلة",
        ]
        for fc in self.file_changes:
            emoji = {"create": "🆕", "update": "✏️", "delete": "🗑️"}.get(
                fc.action, "📄"
            )
            lines.append(f"- {emoji} `{fc.file_path}` — {fc.description}")
        if self.test_strategy:
            lines.append(f"## 🧪 استراتيجية الاختبار\n{self.test_strategy}")
        if self.risks:
            lines.append(f"## ⚠️ المخاطر المحتملة\n{self.risks}")
        return "\n\n".join(lines)


# ──────────────────────────────────────────────────────────
# الموجّه الرئيسي للمعماري
# ──────────────────────────────────────────────────────────

_ARCHITECT_SYSTEM_PROMPT = """
أنت كبير مهندسي البرمجيات المتخصص في مشاريع FastAPI + Next.js.
مهمتك تصميم مخطط معماري دقيق (blueprint) لتنفيذ متطلب معين في مشروع موجود.

القواعد الحديدية:
1. لا تخترع ملفات غير موجودة بلا داعٍ.
2. التغييرات يجب أن تكون الحد الأدنى اللازم لتحقيق المتطلب.
3. كن واضحاً بشأن ترتيب التعديلات (أيها يعتمد على الآخر).
4. فكّر في التأثير على الاختبارات الموجودة وإن كان يلزم تحديثها.
5. راعِ بنية المشروع: backend/ (FastAPI, pytest) و frontend/ (Next.js, TypeScript).

أجب فقط بـ JSON بالشكل التالي:
{
  "task_summary": "وصف موجز للمهمة",
  "rationale": "شرح المنطق المعماري للحل",
  "file_changes": [
    {
      "file_path": "backend/routers/example.py",
      "action": "update",
      "description": "إضافة نقطة نهاية جديدة",
      "expected_content_hint": "دالة async def example() تُعيد JSON"
    }
  ],
  "test_strategy": "وصف كيفية اختبار الحل",
  "risks": "أي مخاطر أو تعارضات محتملة"
}
"""


class Architect:
    """يُصمِّم خطة الحل المعمارية باستخدام GPT-4o مُعزَّزاً بالذاكرة الجينية."""

    def __init__(self, api_key: str | None = None) -> None:
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.memory = GeneticMemory()
        logger.info(
            "Architect: الذاكرة الجينية تحتوي على %d جين/جينات.", self.memory.gene_count
        )

    def design_solution(self, task: str, context: ProjectContext) -> Blueprint:
        """
        يُنتج مخططاً معمارياً بناءً على المتطلب وسياق المشروع.

        Parameters
        ----------
        task : str
            وصف المهمة (من عنوان Issue وتفاصيله).
        context : ProjectContext
            السياق الكامل للمشروع من Analyst.

        Returns
        -------
        Blueprint
            المخطط المعماري الكامل.
        """
        # ── 🧬 استعادة الأخطاء السابقة من الذاكرة الجينية ──
        past_mistakes = self.memory.remember_past_mistakes(task)
        memory_block = ""
        if past_mistakes:
            memory_block = (
                "\n\n## ⚠️ تحذير من الذاكرة الجينية — أخطاء حدثت في مهام مشابهة:\n"
                + past_mistakes
                + "\n**لا تكرر هذه الأخطاء أبداً. اقرأها بعناية قبل التصميم.**\n"
            )

        user_message = (
            f"## المتطلب\n{task}\n"
            f"{memory_block}\n"
            f"## سياق المشروع الحالي\n{context.to_prompt_block()}"
        )

        logger.info("Architect: يُرسل المتطلب لـ GPT-4o للتصميم المعماري...")

        response = self.client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": _ARCHITECT_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
        )

        raw = response.choices[0].message.content or "{}"
        return self._parse_blueprint(raw, task)

    # ──────────────────────────────────────────────────────
    # دوال داخلية
    # ──────────────────────────────────────────────────────

    @staticmethod
    def _parse_blueprint(raw_json: str, fallback_task: str) -> Blueprint:
        """يُحوِّل الـ JSON الخام إلى كائن Blueprint."""
        try:
            data = json.loads(raw_json)
        except json.JSONDecodeError as exc:
            logger.error("Architect: فشل تحليل JSON: %s", exc)
            return Blueprint(
                task_summary=fallback_task,
                rationale="فشل تحليل استجابة المعماري.",
            )

        file_changes = [
            FileChange(
                file_path=fc.get("file_path", ""),
                action=fc.get("action", "update"),
                description=fc.get("description", ""),
                expected_content_hint=fc.get("expected_content_hint", ""),
            )
            for fc in data.get("file_changes", [])
            if fc.get("file_path")
        ]

        return Blueprint(
            task_summary=data.get("task_summary", fallback_task),
            rationale=data.get("rationale", ""),
            file_changes=file_changes,
            test_strategy=data.get("test_strategy", ""),
            risks=data.get("risks", ""),
        )
