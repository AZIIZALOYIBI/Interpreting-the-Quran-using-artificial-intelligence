"""
صياد الديون التقنية (Tech-Debt Predator)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
يستيقظ استباقياً (cron) ويتجول في ملفات المشروع بحثاً عن:
  - Code Smells: دوال طويلة، تكرار كود، تعقيد مرتفع
  - الاستيرادات غير المُستخدَمة (unused imports)
  - المكتبات القديمة (outdated dependencies)
  - TODO/FIXME المتراكمة
  - الملفات الميتة (لا تُستورَد من أي مكان)

لكل مشكلة مكتشَفة:
  1. ينشئ Issue في GitHub بتوصيف المشكلة والأثر
  2. يرفق اقتراح كود أولي للإصلاح (من GPT-4o)
  3. يضع عليه label: 'tech-debt' و priority تلقائية

هذا يُحوِّل الأداة من Reactive → Proactive.
"""

from __future__ import annotations

import ast
import logging
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

REPO_ROOT = Path(os.getenv("GITHUB_WORKSPACE", "."))

# حد أقصى للأسطر لكي تُعتبَر الدالة "طويلة"
MAX_FUNCTION_LINES = 60

# حد أقصى للتعقيد الدوري (Cyclomatic Complexity)
MAX_COMPLEXITY = 10

# أنماط TODO/FIXME
TODO_PATTERN = re.compile(r"#\s*(TODO|FIXME|HACK|XXX|BUG)[\s:]", re.IGNORECASE)

# label الديون التقنية في GitHub
TECH_DEBT_LABEL = "tech-debt"


@dataclass
class DebtItem:
    """عنصر دين تقني مكتشَف."""

    file_path: str
    line_number: int
    smell_type: str        # "long_function", "todo", "unused_import", "complexity"
    description: str
    severity: str          # "high", "medium", "low"
    code_snippet: str = ""
    suggested_fix: str = ""
    priority_label: str = "medium"
    extra: dict = field(default_factory=dict)


class TechDebtPredator:
    """يصطاد الديون التقنية استباقياً ويُبلِّغ عنها كـ Issues."""

    def __init__(self, repo) -> None:
        self.repo = repo
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._debts: list[DebtItem] = []

    # ──────────────────────────────────────────────────────
    # الواجهة العامة
    # ──────────────────────────────────────────────────────

    def hunt(self) -> int:
        """
        يُشغِّل جميع عمليات الصيد ويُنشئ Issues للديون المكتشَفة.

        Returns
        -------
        int
            عدد Issues التي تم إنشاؤها.
        """
        logger.info("🎯 Tech-Debt Predator: بدأ الصيد الاستباقي...")

        self._scan_python_files()
        self._scan_todos()
        self._scan_outdated_deps()

        if not self._debts:
            logger.info("🎯 Predator: لم تُكتشَف ديون تقنية ملحوظة. المشروع نظيف!")
            return 0

        logger.info("🎯 Predator: اكتشف %d دين تقني/ديون. يُنشئ Issues...", len(self._debts))

        created = 0
        for debt in self._debts[:5]:  # حد أقصى 5 Issues لكل دورة (لتجنب الإغراق)
            if self._create_issue(debt):
                created += 1

        logger.info("🎯 Predator: أنشأ %d Issue/Issues.", created)
        return created

    # ──────────────────────────────────────────────────────
    # عمليات المسح
    # ──────────────────────────────────────────────────────

    def _scan_python_files(self) -> None:
        """يفحص ملفات Python بحثاً عن Smells باستخدام AST."""
        dirs = [REPO_ROOT / "backend", REPO_ROOT / "core_brain", REPO_ROOT / "ai-engine"]
        for directory in dirs:
            if not directory.exists():
                continue
            for py_file in directory.rglob("*.py"):
                if "__pycache__" in str(py_file):
                    continue
                self._analyze_python_file(py_file)

    def _analyze_python_file(self, path: Path) -> None:
        """يُحلِّل ملف Python باستخدام AST."""
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source)
        except SyntaxError:
            return  # لا نُبلِّغ عن ملفات ذات أخطاء صياغة — ذلك عمل Validator

        lines = source.splitlines()
        rel_path = str(path.relative_to(REPO_ROOT))

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._check_function_length(node, lines, rel_path)
                self._check_complexity(node, rel_path)

        # فحص الاستيرادات غير المُستخدَمة (بسيط — flake8 F401)
        self._check_unused_imports(source, lines, rel_path)

    def _check_function_length(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        lines: list[str],
        rel_path: str,
    ) -> None:
        """يُبلِّغ عن الدوال التي تتجاوز MAX_FUNCTION_LINES سطراً."""
        start = node.lineno
        end = getattr(node, "end_lineno", start)
        length = end - start

        if length > MAX_FUNCTION_LINES:
            snippet = "\n".join(lines[start - 1 : min(start + 5, len(lines))])
            self._debts.append(
                DebtItem(
                    file_path=rel_path,
                    line_number=start,
                    smell_type="long_function",
                    description=(
                        f"الدالة `{node.name}` تمتد على {length} سطراً "
                        f"(الحد الموصى به: {MAX_FUNCTION_LINES}). "
                        "الدوال الطويلة تُصعِّب الاختبار والصيانة."
                    ),
                    severity="medium" if length < 100 else "high",
                    code_snippet=snippet,
                    priority_label="medium",
                    extra={"function_name": node.name, "lines": length},
                )
            )

    def _check_complexity(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        rel_path: str,
    ) -> None:
        """يحسب التعقيد الدوري تقديرياً (عدد نقاط التفرع)."""
        branch_nodes = (
            ast.If, ast.For, ast.While, ast.ExceptHandler,
            ast.With, ast.Assert, ast.comprehension,
        )
        complexity = 1 + sum(1 for _ in ast.walk(node) if isinstance(_, branch_nodes))

        if complexity > MAX_COMPLEXITY:
            self._debts.append(
                DebtItem(
                    file_path=rel_path,
                    line_number=node.lineno,
                    smell_type="high_complexity",
                    description=(
                        f"الدالة `{node.name}` لديها تعقيد دوري تقديري = {complexity} "
                        f"(الحد الموصى به: {MAX_COMPLEXITY}). "
                        "يُقترح تفكيكها إلى دوال أصغر."
                    ),
                    severity="high",
                    priority_label="high",
                    extra={"function_name": node.name, "complexity": complexity},
                )
            )

    def _check_unused_imports(
        self, source: str, lines: list[str], rel_path: str
    ) -> None:
        """يكتشف استيرادات مُعلَّقة باستخدام flake8 F401."""
        try:
            result = subprocess.run(
                ["python", "-m", "flake8", "--select=F401", "--format=%(row)d:%(text)s", "-"],
                input=source,
                capture_output=True,
                text=True,
                timeout=10,
            )
            for line in result.stdout.splitlines():
                if ":" not in line:
                    continue
                row_str, msg = line.split(":", 1)
                try:
                    row = int(row_str)
                except ValueError:
                    continue
                self._debts.append(
                    DebtItem(
                        file_path=rel_path,
                        line_number=row,
                        smell_type="unused_import",
                        description=f"استيراد غير مُستخدَم في السطر {row}: {msg.strip()}",
                        severity="low",
                        code_snippet=lines[row - 1] if row <= len(lines) else "",
                        priority_label="low",
                    )
                )
        except Exception:
            pass  # flake8 ربما غير مثبَّت

    def _scan_todos(self) -> None:
        """يبحث عن تعليقات TODO/FIXME المتراكمة في كل الملفات."""
        dirs = [REPO_ROOT / "backend", REPO_ROOT / "frontend" / "src", REPO_ROOT / "core_brain"]
        for directory in dirs:
            if not directory.exists():
                continue
            for src_file in directory.rglob("*"):
                if src_file.is_dir() or src_file.stat().st_size > 200_000:
                    continue
                if src_file.suffix not in {".py", ".ts", ".tsx", ".js", ".md"}:
                    continue
                try:
                    content = src_file.read_text(encoding="utf-8", errors="replace")
                    for i, line in enumerate(content.splitlines(), 1):
                        if TODO_PATTERN.search(line):
                            rel_path = str(src_file.relative_to(REPO_ROOT))
                            self._debts.append(
                                DebtItem(
                                    file_path=rel_path,
                                    line_number=i,
                                    smell_type="todo",
                                    description=f"تعليق {TODO_PATTERN.search(line).group(1)} قديم في السطر {i}: {line.strip()[:120]}",
                                    severity="low",
                                    code_snippet=line.strip(),
                                    priority_label="low",
                                )
                            )
                except Exception:
                    continue

    def _scan_outdated_deps(self) -> None:
        """يفحص requirements.txt بحثاً عن إصدارات مُثبَّتة بشكل صارم جداً."""
        req_file = REPO_ROOT / "backend" / "requirements.txt"
        if not req_file.exists():
            return

        try:
            result = subprocess.run(
                ["pip", "list", "--outdated", "--format=columns"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            outdated = {}
            for line in result.stdout.splitlines()[2:]:  # تخطي رأس الجدول
                parts = line.split()
                if len(parts) >= 3:
                    outdated[parts[0].lower()] = {"current": parts[1], "latest": parts[2]}

            req_content = req_file.read_text()
            for i, line in enumerate(req_content.splitlines(), 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                pkg = re.split(r"[>=<!]", line)[0].strip().lower()
                if pkg in outdated:
                    info = outdated[pkg]
                    self._debts.append(
                        DebtItem(
                            file_path="backend/requirements.txt",
                            line_number=i,
                            smell_type="outdated_dependency",
                            description=(
                                f"المكتبة `{pkg}` إصدارها الحالي {info['current']} "
                                f"والإصدار الأحدث {info['latest']}. "
                                "التحديث قد يُصلح ثغرات أمنية ويُحسِّن الأداء."
                            ),
                            severity="medium",
                            code_snippet=line,
                            priority_label="medium",
                        )
                    )
        except Exception as exc:
            logger.debug("Predator: فشل فحص المكتبات القديمة: %s", exc)

    # ──────────────────────────────────────────────────────
    # إنشاء Issues
    # ──────────────────────────────────────────────────────

    def _create_issue(self, debt: DebtItem) -> bool:
        """يُنشئ Issue في GitHub ويرفق اقتراح إصلاح من GPT-4o."""
        suggested_fix = self._suggest_fix(debt)

        severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(debt.severity, "⚪")
        title = f"🎯 [Tech-Debt] {severity_emoji} {debt.smell_type.replace('_', ' ').title()} في {debt.file_path}:{debt.line_number}"

        body = (
            f"## 🎯 صائد الديون التقنية اكتشف مشكلة\n\n"
            f"**النوع:** `{debt.smell_type}`  \n"
            f"**الخطورة:** {severity_emoji} {debt.severity}  \n"
            f"**الملف:** `{debt.file_path}` السطر {debt.line_number}\n\n"
            f"### 📋 الوصف\n{debt.description}\n\n"
        )

        if debt.code_snippet:
            body += f"### 💻 الكود الحالي\n```\n{debt.code_snippet[:500]}\n```\n\n"

        if suggested_fix:
            body += f"### ✅ الإصلاح المقترح\n{suggested_fix}\n\n"

        body += (
            "---\n"
            "> 🤖 تم اكتشاف هذه المشكلة تلقائياً بواسطة **صائد الديون التقنية (Tech-Debt Predator)**  \n"
            "> وهو جزء من نظام **النواة الواعية (Sentient Core)**.\n"
            "> ضع عليه علامة `evolve` لتتولى النواة إصلاحه تلقائياً."
        )

        try:
            # تأكد من وجود الـ label
            self._ensure_label(TECH_DEBT_LABEL, "d4c5f7", "ديون تقنية مكتشَفة بواسطة Predator")
            self._ensure_label(f"priority:{debt.priority_label}", "f9a825", f"أولوية {debt.priority_label}")

            issue = self.repo.create_issue(
                title=title[:256],
                body=body,
                labels=[TECH_DEBT_LABEL, f"priority:{debt.priority_label}"],
            )
            logger.info("🎯 Predator: Issue #%d أُنشئ — %s", issue.number, debt.description[:60])
            return True
        except Exception as exc:
            logger.error("🎯 Predator: فشل إنشاء Issue: %s", exc)
            return False

    def _suggest_fix(self, debt: DebtItem) -> str:
        """يطلب من GPT-4o اقتراح إصلاح موجز للدين التقني."""
        prompt = (
            f"أنت مستشار جودة كود. اقترح إصلاحاً موجزاً (بالعربية أو بالكود) لهذه المشكلة:\n\n"
            f"النوع: {debt.smell_type}\n"
            f"الملف: {debt.file_path}\n"
            f"الوصف: {debt.description}\n"
            f"الكود الحالي:\n```\n{debt.code_snippet[:300]}\n```\n\n"
            "قدِّم اقتراحاً مختصراً (5-10 أسطر) مع مثال كود إذا أمكن."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            logger.debug("Predator: فشل GPT-4o-mini: %s", exc)
            return ""

    def _ensure_label(self, name: str, color: str, description: str) -> None:
        """يُنشئ الـ label إن لم يكن موجوداً."""
        try:
            self.repo.get_label(name)
        except Exception:
            try:
                self.repo.create_label(name=name, color=color, description=description[:100])
            except Exception:
                pass
