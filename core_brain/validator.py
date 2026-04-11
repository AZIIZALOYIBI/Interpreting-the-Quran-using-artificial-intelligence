"""
العقل الرابع: المُدقِّق (Validator)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
يُنفِّذ فحوصات متعددة الطبقات على الكود المُولَّد:

  الطبقة 1 — فحص الصياغة (Syntax):
    - Python  : py_compile على كل ملف .py
    - TypeScript: tsc --noEmit على مجلد frontend

  الطبقة 2 — فحص الجودة (Lint):
    - Python  : flake8 (إن كان مثبَّتاً)
    - Frontend: next lint (إن كان متاحاً)

  الطبقة 3 — تشغيل الاختبارات (Tests):
    - pytest على backend/tests/ مع timeout
    - يُعيد (is_valid: bool, errors: list[str])

حلقة التصحيح الذاتي:
  main.py يستدعي run_local_checks() في حلقة while
  وعند الفشل يُمرِّر الأخطاء لـ Coder.fix_errors()
"""

from __future__ import annotations

import logging
import os
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

# جذر المستودع المُستنسَخ داخل بيئة GitHub Actions
REPO_ROOT = Path(os.getenv("GITHUB_WORKSPACE", "."))

# أوامر التحقق
_PYTEST_CMD = ["python", "-m", "pytest", "backend/tests/", "-v", "--tb=short", "-q"]
_PY_COMPILE_CMD = ["python", "-m", "py_compile"]
_FLAKE8_CMD = [
    "python",
    "-m",
    "flake8",
    "backend/",
    "core_brain/",
    "--max-line-length=100",
    "--extend-ignore=E501,W503",
    "--exclude=__pycache__,.venv,node_modules",
]
_TSC_CMD = ["npx", "tsc", "--noEmit", "--project", "frontend/tsconfig.json"]
_NEXT_LINT_CMD = ["npx", "next", "lint", "--dir", "frontend/src"]


class Validator:
    """يُنفِّذ فحوصات الكود ويُعيد قائمة الأخطاء."""

    def __init__(self, repo, branch: str) -> None:
        """
        Parameters
        ----------
        repo : github.Repository.Repository
            كائن المستودع (غير مُستخدَم حالياً — مُخصَّص للتوسعة المستقبلية).
        branch : str
            اسم الفرع الذي يُفحَص (يُستخدَم في السجلات).
        """
        self.repo = repo
        self.branch = branch

    # ──────────────────────────────────────────────────────
    # الواجهة العامة
    # ──────────────────────────────────────────────────────

    def run_local_checks(self) -> tuple[bool, list[str]]:
        """
        يُشغِّل جميع طبقات الفحص ويُجمِّع الأخطاء.

        Returns
        -------
        tuple[bool, list[str]]
            (True, []) إذا نجح كل شيء.
            (False, [رسائل الخطأ]) إذا وُجد خطأ.
        """
        all_errors: list[str] = []

        # ── الطبقة 1: فحص الصياغة لملفات Python ──
        py_errors = self._check_python_syntax()
        if py_errors:
            all_errors.extend(py_errors)
            # إذا كانت هناك أخطاء صياغة → لا فائدة من تشغيل pytest
            return False, all_errors

        # ── الطبقة 2أ: Flake8 ──
        flake_errors = self._run_flake8()
        all_errors.extend(flake_errors)

        # ── الطبقة 2ب: TypeScript (اختياري) ──
        ts_errors = self._check_typescript()
        all_errors.extend(ts_errors)

        # ── الطبقة 3: pytest ──
        test_errors = self._run_pytest()
        all_errors.extend(test_errors)

        is_valid = len(all_errors) == 0
        if is_valid:
            logger.info("Validator ✅ [%s]: جميع الفحوصات اجتازت بنجاح.", self.branch)
        else:
            logger.warning(
                "Validator ❌ [%s]: %d خطأ/أخطاء وُجدت.", self.branch, len(all_errors)
            )
        return is_valid, all_errors

    # ──────────────────────────────────────────────────────
    # الطبقة 1 — فحص صياغة Python
    # ──────────────────────────────────────────────────────

    def _check_python_syntax(self) -> list[str]:
        """يتحقق من صياغة جميع ملفات .py في backend/ و core_brain/."""
        errors: list[str] = []
        dirs_to_scan = [REPO_ROOT / "backend", REPO_ROOT / "core_brain"]

        for directory in dirs_to_scan:
            if not directory.exists():
                continue
            for py_file in directory.rglob("*.py"):
                if "__pycache__" in str(py_file):
                    continue
                result = subprocess.run(
                    _PY_COMPILE_CMD + [str(py_file)],
                    capture_output=True,
                    text=True,
                    cwd=str(REPO_ROOT),
                )
                if result.returncode != 0:
                    errors.append(
                        f"[SyntaxError] {py_file.relative_to(REPO_ROOT)}\n"
                        f"{result.stderr.strip()}"
                    )

        return errors

    # ──────────────────────────────────────────────────────
    # الطبقة 2أ — Flake8
    # ──────────────────────────────────────────────────────

    def _run_flake8(self) -> list[str]:
        """يُشغِّل flake8 (يتجاهل إن لم يكن مثبَّتاً)."""
        result = subprocess.run(
            _FLAKE8_CMD,
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        if result.returncode == 0:
            return []
        if "No module named flake8" in result.stderr:
            logger.debug("Validator: flake8 غير مثبَّت — تجاهل الطبقة الثانية.")
            return []
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        return [f"[Flake8] {line}" for line in lines if line]

    # ──────────────────────────────────────────────────────
    # الطبقة 2ب — TypeScript
    # ──────────────────────────────────────────────────────

    def _check_typescript(self) -> list[str]:
        """يُشغِّل tsc --noEmit إن كان tsconfig.json موجوداً."""
        tsconfig = REPO_ROOT / "frontend" / "tsconfig.json"
        if not tsconfig.exists():
            return []

        result = subprocess.run(
            _TSC_CMD,
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            timeout=120,
        )
        if result.returncode == 0:
            return []
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        return [f"[TypeScript] {line}" for line in lines if line]

    # ──────────────────────────────────────────────────────
    # الطبقة 3 — pytest
    # ──────────────────────────────────────────────────────

    def _run_pytest(self) -> list[str]:
        """يُشغِّل pytest ويُعيد رسائل الخطأ عند الفشل."""
        tests_dir = REPO_ROOT / "backend" / "tests"
        if not tests_dir.exists():
            logger.debug("Validator: لا يوجد مجلد tests/ — تجاهل pytest.")
            return []

        # نُضيف backend/ لـ PYTHONPATH لضمان الاستيرادات الصحيحة
        env = os.environ.copy()
        backend_path = str(REPO_ROOT / "backend")
        env["PYTHONPATH"] = backend_path + os.pathsep + env.get("PYTHONPATH", "")

        result = subprocess.run(
            _PYTEST_CMD,
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT / "backend"),
            timeout=300,
            env=env,
        )

        if result.returncode == 0:
            logger.info("Validator: pytest ✅ — جميع الاختبارات اجتازت.")
            return []

        # نُعيد آخر 100 سطر من المخرجات لتجنب الإطالة
        output = (result.stdout + "\n" + result.stderr).strip()
        lines = output.split("\n")
        tail = lines[-100:] if len(lines) > 100 else lines
        return ["[pytest] " + line for line in tail if line]
