"""
العقل الأول: المحلل (Analyst)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
يجلب الفهم الكامل لهيكل المشروع قبل أن يُكتب أي كود.
يستخدم:
  - GitHub Trees API  → هيكل الملفات الكامل
  - GitHub Contents API → محتوى الملفات الجوهرية
  - تحليل الملفات المهمة (backend, frontend, tests, config)
  - بناء سياق دلالي (RAG-ready context) يُمرَّر للمعماري
"""

from __future__ import annotations

import base64
import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

# الملفات الجوهرية التي تعطي فهماً عميقاً للمشروع
CORE_FILE_PATHS: list[str] = [
    # إعدادات المشروع
    "README.md",
    "CLAUDE.md",
    "pyproject.toml",
    "Makefile",
    "docker-compose.yml",
    # Backend
    "backend/main.py",
    "backend/requirements.txt",
    "backend/config.py",
    "backend/routers/quran.py",
    "backend/routers/chat.py",
    "backend/services/ai_service.py",
    "backend/services/quran_service.py",
    "backend/data/categories.py",
    "backend/data/sample_ayahs.py",
    "backend/tests/conftest.py",
    # Frontend
    "frontend/package.json",
    "frontend/src/types/index.ts",
    "frontend/src/lib/api.ts",
    "frontend/src/app/page.tsx",
    "frontend/src/components/AskQuranChat.tsx",
    # AI Engine
    "ai-engine/quran_solver.py",
]

# حجم أقصى للمحتوى لتفادي تجاوز نافذة السياق
MAX_CONTENT_CHARS = 4_000


@dataclass
class ProjectContext:
    """السياق الكامل للمشروع الذي يُمرَّر بين العقول."""

    file_tree: str = ""
    core_files: dict[str, str] = field(default_factory=dict)
    test_runner_cmd: str = "cd backend && python -m pytest tests/ -v"
    lint_cmd: str = "cd backend && python -m py_compile"
    frontend_build_cmd: str = "cd frontend && npm run build"
    branch_default: str = "main"
    languages: list[str] = field(default_factory=lambda: ["Python", "TypeScript"])

    def to_prompt_block(self) -> str:
        """يحوّل السياق إلى نص مُنسَّق يصلح كـ prompt للـ LLM."""
        parts: list[str] = [
            "## هيكل المشروع\n```\n" + self.file_tree + "\n```",
        ]
        for path, content in self.core_files.items():
            parts.append(f"## {path}\n```\n{content}\n```")
        return "\n\n".join(parts)


class Analyst:
    """يحلل المستودع ويبني سياقاً دلالياً شاملاً."""

    def __init__(self, repo) -> None:
        """
        Parameters
        ----------
        repo : github.Repository.Repository
            كائن المستودع من PyGithub.
        """
        self.repo = repo

    # ──────────────────────────────────────────────────────
    # الواجهة العامة
    # ──────────────────────────────────────────────────────

    def get_context(self, ref: str = "main") -> ProjectContext:
        """
        يبني ويُعيد سياق المشروع الكامل.

        Parameters
        ----------
        ref : str
            اسم الفرع أو commit SHA المراد تحليله.

        Returns
        -------
        ProjectContext
            كائن يحتوي على شجرة الملفات ومحتوى الملفات الجوهرية.
        """
        ctx = ProjectContext(branch_default=ref)
        ctx.file_tree = self._build_file_tree(ref)
        ctx.core_files = self._read_core_files(ref)
        logger.info(
            "Analyst: جمعت %d ملفاً جوهرياً من المستودع.", len(ctx.core_files)
        )
        return ctx

    # ──────────────────────────────────────────────────────
    # الدوال الداخلية
    # ──────────────────────────────────────────────────────

    def _build_file_tree(self, ref: str) -> str:
        """يُنشئ قائمة بجميع ملفات المستودع (blobs فقط)."""
        try:
            tree = self.repo.get_git_tree(ref, recursive=True)
            lines = [
                item.path
                for item in tree.tree
                if item.type == "blob"
                # استبعاد الملفات الثنائية والمولَّدة تلقائياً
                and not item.path.startswith(
                    (
                        "frontend/node_modules/",
                        "frontend/.next/",
                        ".git/",
                        "__pycache__/",
                    )
                )
            ]
            return "\n".join(lines)
        except Exception as exc:  # pragma: no cover
            logger.warning("Analyst: فشل جلب شجرة الملفات: %s", exc)
            return ""

    def _read_core_files(self, ref: str) -> dict[str, str]:
        """يقرأ محتوى الملفات الجوهرية ويختصرها إذا كانت طويلة."""
        contents: dict[str, str] = {}
        for path in CORE_FILE_PATHS:
            content = self._fetch_file(path, ref)
            if content is not None:
                contents[path] = self._truncate(content, path)
        return contents

    def _fetch_file(self, path: str, ref: str) -> Optional[str]:
        """يجلب محتوى ملف واحد من GitHub ويُرجع نصاً أو None عند الفشل."""
        try:
            file_obj = self.repo.get_contents(path, ref=ref)
            # get_contents يُعيد قائمة إذا كان المسار مجلداً
            if isinstance(file_obj, list):
                return None
            raw: bytes = (
                file_obj.decoded_content
                if file_obj.encoding == "base64"
                else base64.b64decode(file_obj.content)
            )
            return raw.decode("utf-8", errors="replace")
        except Exception:
            return None

    @staticmethod
    def _truncate(text: str, path: str) -> str:
        """يقطع النص الطويل مع إشارة واضحة للاقتصار."""
        if len(text) <= MAX_CONTENT_CHARS:
            return text
        half = MAX_CONTENT_CHARS // 2
        return (
            text[:half]
            + f"\n\n... [تم اقتصار {path} — {len(text):,} حرف أصلاً] ...\n\n"
            + text[-half:]
        )
