"""
العقل الثالث: الكاتب (Coder)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
يُنفِّذ المخطط المعماري من Architect بدقة متناهية:
  - يقرأ الملف الحالي من المستودع (سياق كامل).
  - يطلب من GPT-4o كتابة الكود الكامل للملف.
  - يُنشئ أو يُحدِّث الملف في الفرع المحدد عبر GitHub API.
  - يمتلك دالة fix_errors() لحلقة التصحيح الذاتي.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Optional

from openai import OpenAI

from architect import Blueprint, FileChange

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────
# Prompts
# ──────────────────────────────────────────────────────────

_CODER_SYSTEM_PROMPT = """
أنت مبرمج من النخبة متخصص في Python/FastAPI و TypeScript/Next.js.
مهمتك كتابة كود إنتاجي نظيف وآمن ومُختبَر.

القواعد الحديدية:
1. أعد الكود الكامل للملف (ليس مقتطفات أو تعليقات فقط).
2. لا تُزيل كوداً قائماً إلا إذا كانت التعليمات صريحة بذلك.
3. لا تضف تعليقات مُفرطة — فقط ما هو ضروري.
4. تأكد من التوافق مع الكود المحيط (imports، نماذج البيانات، الأنماط).
5. للبايثون: التزم بـ PEP 8 واستخدم type hints.
6. للـ TypeScript: التزم بـ strict types وتجنب `any`.

أجب فقط بـ JSON:
{"code": "<الكود الكامل للملف>"}
"""

_FIXER_SYSTEM_PROMPT = """
أنت مُحقِّق أخطاء من النخبة. تلقيت رسائل خطأ من أدوات التحقق.
مهمتك تصحيح الكود مع الحفاظ على وظيفته الأصلية.

اقرأ الخطأ بعناية، حدِّد السبب الجذري، وأصلح الكود.
أجب فقط بـ JSON:
{"code": "<الكود المُصحَّح الكامل>", "fix_explanation": "شرح موجز للإصلاح"}
"""


class Coder:
    """يُنفِّذ المخطط المعماري ويُحدِّث المستودع."""

    def __init__(self, repo) -> None:
        """
        Parameters
        ----------
        repo : github.Repository.Repository
            كائن المستودع من PyGithub.
        """
        self.repo = repo
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # ──────────────────────────────────────────────────────
    # الواجهة العامة
    # ──────────────────────────────────────────────────────

    def implement_blueprint(self, blueprint: Blueprint, branch: str) -> None:
        """
        يُنفِّذ كل تعديل في المخطط المعماري ملفاً بملف.

        Parameters
        ----------
        blueprint : Blueprint
            المخطط الصادر من Architect.
        branch : str
            اسم الفرع الذي ستُطبَّق عليه التعديلات.
        """
        for change in blueprint.file_changes:
            if change.action == "delete":
                self._delete_file(change.file_path, branch)
                continue

            current_code = self._fetch_current_code(change.file_path, branch)
            new_code = self._generate_code(change, blueprint.task_summary, current_code)

            if new_code:
                self._write_file(change.file_path, new_code, branch, change.description)
            else:
                logger.warning("Coder: لم يُنتج GPT-4o كوداً للملف %s", change.file_path)

    def fix_errors(
        self,
        errors: list[str],
        branch: str,
        changed_files: list[str],
    ) -> None:
        """
        يُصحِّح الأخطاء التي أبلغ عنها Validator.

        Parameters
        ----------
        errors : list[str]
            قائمة رسائل الخطأ من أدوات التحقق.
        branch : str
            اسم الفرع الذي يحتوي على الكود المعيب.
        changed_files : list[str]
            مسارات الملفات التي ربما تحتوي على الأخطاء.
        """
        error_report = "\n".join(errors)
        logger.info("Coder: يبدأ حلقة التصحيح الذاتي للأخطاء:\n%s", error_report)

        for file_path in changed_files:
            current_code = self._fetch_current_code(file_path, branch)
            if not current_code:
                continue

            fixed_code, explanation = self._fix_code(file_path, current_code, error_report)
            if fixed_code:
                logger.info("Coder: إصلاح %s — %s", file_path, explanation)
                self._write_file(file_path, fixed_code, branch, f"🔁 تصحيح ذاتي: {explanation}")

    # ──────────────────────────────────────────────────────
    # دوال توليد الكود
    # ──────────────────────────────────────────────────────

    def _generate_code(
        self,
        change: FileChange,
        task_summary: str,
        current_code: Optional[str],
    ) -> Optional[str]:
        """يطلب من GPT-4o كتابة الكود الكامل لملف محدد."""
        context_block = (
            f"### الكود الحالي للملف\n```\n{current_code}\n```\n"
            if current_code
            else "### الملف جديد (لا يوجد كود حالي)\n"
        )

        prompt = (
            f"## المهمة الكلية\n{task_summary}\n\n"
            f"## التعديل المطلوب على `{change.file_path}`\n"
            f"الإجراء: {change.action}\n"
            f"الوصف: {change.description}\n"
            f"ما يجب أن يحتويه الملف: {change.expected_content_hint}\n\n"
            f"{context_block}"
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": _CODER_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
            )
            raw = response.choices[0].message.content or "{}"
            return json.loads(raw).get("code")
        except Exception as exc:
            logger.error("Coder: خطأ في توليد كود %s: %s", change.file_path, exc)
            return None

    def _fix_code(
        self,
        file_path: str,
        current_code: str,
        error_report: str,
    ) -> tuple[Optional[str], str]:
        """يطلب من GPT-4o إصلاح كود معيب بناءً على رسائل الخطأ."""
        prompt = (
            f"## الملف المعيب: `{file_path}`\n"
            f"```\n{current_code}\n```\n\n"
            f"## رسائل الخطأ\n```\n{error_report}\n```"
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": _FIXER_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
            )
            raw = response.choices[0].message.content or "{}"
            data = json.loads(raw)
            return data.get("code"), data.get("fix_explanation", "إصلاح تلقائي")
        except Exception as exc:
            logger.error("Coder: خطأ في إصلاح %s: %s", file_path, exc)
            return None, ""

    # ──────────────────────────────────────────────────────
    # عمليات GitHub
    # ──────────────────────────────────────────────────────

    def _fetch_current_code(self, path: str, branch: str) -> Optional[str]:
        """يجلب محتوى الملف الحالي من المستودع."""
        try:
            obj = self.repo.get_contents(path, ref=branch)
            if isinstance(obj, list):
                return None
            return obj.decoded_content.decode("utf-8", errors="replace")
        except Exception:
            return None  # الملف غير موجود بعد

    def _write_file(self, path: str, code: str, branch: str, message: str) -> None:
        """يُنشئ أو يُحدِّث ملفاً في الفرع المحدد."""
        commit_message = f"🧬 [Sentient Core] {message[:72]}"
        try:
            existing = self.repo.get_contents(path, ref=branch)
            if isinstance(existing, list):
                raise ValueError("المسار مجلد وليس ملفاً")
            self.repo.update_file(
                path, commit_message, code, existing.sha, branch=branch
            )
            logger.info("Coder: تحديث ✏️  %s", path)
        except Exception:
            # الملف غير موجود → إنشاء جديد
            self.repo.create_file(path, commit_message, code, branch=branch)
            logger.info("Coder: إنشاء 🆕 %s", path)

    def _delete_file(self, path: str, branch: str) -> None:
        """يحذف ملفاً من الفرع المحدد إن وجد."""
        try:
            obj = self.repo.get_contents(path, ref=branch)
            if isinstance(obj, list):
                return
            self.repo.delete_file(
                path,
                f"🧬 [Sentient Core] حذف {path}",
                obj.sha,
                branch=branch,
            )
            logger.info("Coder: حذف 🗑️  %s", path)
        except Exception:
            logger.debug("Coder: لم يُعثر على %s للحذف.", path)
