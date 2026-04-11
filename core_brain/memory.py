"""
الذاكرة الجينية (Genetic Memory)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
قاعدة بيانات متجهة (Vector DB) تحفظ خبرات النواة الواعية عبر الزمن.
تعمل مع ChromaDB محلياً، وتبقى ذاكرتها حية عبر دورة git commit.

دورة الحياة:
  1. قبل التصميم   → remember_past_mistakes()  يجلب تجارب مشابهة
  2. أثناء التصحيح → encode_experience()        يحفظ الخطأ + الحل
  3. نهاية الدورة  → persist_to_repo()          يحفظ الذاكرة في المستودع

الفائدة:
  - لا تكرار للأخطاء التي وقعت فيها مسبقاً.
  - كل دورة تصحيح تُغني الجينوم بمعرفة جديدة.
  - تُقلِّص الاعتماد على GPT-4o بمرور الوقت (استرجاع محلي أولاً).
"""

from __future__ import annotations

import hashlib
import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# مجلد الجينوم داخل المستودع
GENOME_DIR = Path(os.getenv("GITHUB_WORKSPACE", ".")) / "ai_genome"
COLLECTION_NAME = "code_experiences"
MAX_RESULTS = 3  # أكثر تجارب ذات صلة يتم استرجاعها


class GeneticMemory:
    """
    ذاكرة جينية تستخدم ChromaDB كقاعدة بيانات متجهة محلية.
    تتقهقر بسلاسة (graceful degradation) عند غياب chromadb.
    """

    def __init__(self) -> None:
        self._collection = None
        self._available = False
        self._init_chromadb()

    # ──────────────────────────────────────────────────────
    # التهيئة
    # ──────────────────────────────────────────────────────

    def _init_chromadb(self) -> None:
        """يُهيِّئ ChromaDB بشكل دفاعي — يستمر إن فشل."""
        try:
            import chromadb  # type: ignore

            GENOME_DIR.mkdir(parents=True, exist_ok=True)
            client = chromadb.PersistentClient(path=str(GENOME_DIR))
            self._collection = client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )
            self._available = True
            count = self._collection.count()
            logger.info(
                "🧬 Genetic Memory: تم تحميل الجينوم بنجاح (%d تجربة مخزَّنة).", count
            )
        except ImportError:
            logger.warning(
                "🧬 Genetic Memory: chromadb غير مثبَّت — الذاكرة الجينية معطَّلة. "
                "ثبِّته بـ: pip install chromadb"
            )
        except Exception as exc:
            logger.warning("🧬 Genetic Memory: فشل التهيئة: %s", exc)

    # ──────────────────────────────────────────────────────
    # الاسترجاع
    # ──────────────────────────────────────────────────────

    def remember_past_mistakes(self, current_task: str) -> str:
        """
        يبحث في الجينوم عن تجارب سابقة مشابهة للمهمة الحالية.

        Returns
        -------
        str
            نص مُنسَّق يحتوي على التجارب المشابهة، أو سلسلة فارغة.
        """
        if not self._available or not self._collection:
            return ""

        try:
            count = self._collection.count()
            if count == 0:
                return ""

            results = self._collection.query(
                query_texts=[current_task],
                n_results=min(MAX_RESULTS, count),
                include=["documents", "distances"],
            )

            docs = results.get("documents", [[]])[0]
            distances = results.get("distances", [[]])[0]

            # نُصفِّي النتائج البعيدة (تشابه منخفض)
            relevant = [
                doc
                for doc, dist in zip(docs, distances)
                if dist < 0.6  # عتبة التشابه (cosine distance)
            ]

            if not relevant:
                return ""

            logger.info(
                "🧬 Genetic Memory: وجدت %d تجربة ذات صلة في الجينوم.",
                len(relevant),
            )
            memory_block = "\n\n---\n\n".join(relevant)
            return (
                "### ⚠️ أخطاء سابقة من الذاكرة الجينية — لا تكررها:\n\n"
                + memory_block
            )
        except Exception as exc:
            logger.warning("🧬 Genetic Memory: فشل الاستعلام: %s", exc)
            return ""

    # ──────────────────────────────────────────────────────
    # التخزين
    # ──────────────────────────────────────────────────────

    def encode_experience(
        self,
        task: str,
        error_report: str,
        final_fix: str,
        attempt_number: int = 1,
    ) -> None:
        """
        يُرمِّز تجربة تصحيح خطأ كـ "جين" جديد في الذاكرة.

        Parameters
        ----------
        task : str
            وصف المهمة التي كانت قيد التنفيذ.
        error_report : str
            رسالة الخطأ الكاملة من Validator.
        final_fix : str
            وصف التصحيح الذي نجح.
        attempt_number : int
            رقم محاولة التصحيح (للسياق).
        """
        if not self._available or not self._collection:
            return

        experience_text = (
            f"المهمة: {task[:500]}\n\n"
            f"الخطأ (المحاولة {attempt_number}):\n{error_report[:800]}\n\n"
            f"الإصلاح الناجح:\n{final_fix[:500]}"
        )

        # معرِّف فريد قابل للتكرار (idempotent)
        doc_id = "exp_" + hashlib.md5(experience_text.encode()).hexdigest()[:12]

        try:
            # تجنُّب الإضافة المكررة
            existing = self._collection.get(ids=[doc_id])
            if existing["ids"]:
                logger.debug("🧬 Genetic Memory: التجربة موجودة مسبقاً (%s).", doc_id)
                return

            self._collection.add(
                documents=[experience_text],
                ids=[doc_id],
                metadatas=[{"attempt": attempt_number, "task_hash": doc_id[:8]}],
            )
            logger.info("🧬 Genetic Memory: تجربة جديدة رُمِّزت في الجينوم ✓ (%s).", doc_id)
        except Exception as exc:
            logger.warning("🧬 Genetic Memory: فشل التخزين: %s", exc)

    # ──────────────────────────────────────────────────────
    # الحفظ الدائم في المستودع
    # ──────────────────────────────────────────────────────

    def persist_to_repo(self) -> None:
        """
        يُثبِّت ملفات الجينوم في المستودع عبر git commit.
        هذا يضمن بقاء الذاكرة عبر دورات GitHub Actions المختلفة.
        """
        if not self._available or not GENOME_DIR.exists():
            return

        workspace = str(GENOME_DIR.parent)
        cmds = [
            ["git", "-C", workspace, "config", "--local", "user.email", "sentient-core@ai.quran"],
            ["git", "-C", workspace, "config", "--local", "user.name", "Sentient Core"],
            ["git", "-C", workspace, "add", str(GENOME_DIR)],
            [
                "git",
                "-C",
                workspace,
                "commit",
                "-m",
                "🧬 Genetic Memory: تحديث الجينوم بتجارب جديدة [skip ci]",
                "--allow-empty",
            ],
            ["git", "-C", workspace, "push", "origin", "HEAD"],
        ]

        for cmd in cmds:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0 and "nothing to commit" not in result.stdout:
                logger.debug("genome-persist: %s → %s", " ".join(cmd[3:]), result.stderr.strip())

        logger.info("🧬 Genetic Memory: الجينوم محفوظ في المستودع.")

    @property
    def gene_count(self) -> int:
        """عدد الجينات المخزَّنة في الذاكرة."""
        if not self._available or not self._collection:
            return 0
        try:
            return self._collection.count()
        except Exception:
            return 0
