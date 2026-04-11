"""
المنسِّق المركزي — Sentient Core Orchestrator
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ينسِّق بين العقول الأربعة + الذاكرة الجينية + المحاكاة الشبحية:

  [Issue] → Analyst → Architect (🧬Memory) → Coder → Validator ⟳ → Phantom → PR

يُشغَّل داخل GitHub Actions من sentient_core.yml
عبر متغيرات البيئة:
  OPENAI_API_KEY  — مفتاح OpenAI
  GH_TOKEN        — رمز GitHub ذو صلاحيات write
  REPO            — مالك/اسم-المستودع (مثال: org/repo)
  ISSUE_NUMBER    — رقم الـ Issue (0 = فحص صحة استباقي)
  PREDATOR_MODE   — "true" لتشغيل صائد الديون التقنية
"""

from __future__ import annotations

import logging
import os
import sys
import time

from github import Github, GithubException

# إضافة مجلد core_brain لـ sys.path
sys.path.insert(0, os.path.dirname(__file__))

from analyst import Analyst
from architect import Architect
from coder import Coder
from memory import GeneticMemory
from phantom import PhantomSandbox
from predator import TechDebtPredator
from validator import Validator

# ──────────────────────────────────────────────────────────
# إعداد التسجيل
# ──────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("sentient-core")

# ──────────────────────────────────────────────────────────
# الثوابت
# ──────────────────────────────────────────────────────────

MAX_CORRECTION_ATTEMPTS = 3
BRANCH_PREFIX = "sentient-core-issue"
BASE_BRANCH = "main"


# ──────────────────────────────────────────────────────────
# نقطة الدخول الرئيسية
# ──────────────────────────────────────────────────────────


def main() -> None:
    """يُشغِّل دورة الحياة الكاملة للنواة الواعية."""

    # ── 0. تهيئة البيئة ──
    gh_token = os.getenv("GH_TOKEN")
    repo_name = os.getenv("REPO")
    issue_number = int(os.getenv("ISSUE_NUMBER", "0"))
    predator_mode = os.getenv("PREDATOR_MODE", "false").lower() == "true"

    if not gh_token or not repo_name:
        logger.error("يجب ضبط GH_TOKEN و REPO كمتغيرات بيئة.")
        sys.exit(1)

    g = Github(gh_token)
    try:
        repo = g.get_repo(repo_name)
    except GithubException as exc:
        logger.error("فشل الاتصال بالمستودع %s: %s", repo_name, exc)
        sys.exit(1)

    # ── وضع صائد الديون التقنية (Predator Mode) ──
    if predator_mode:
        logger.info("🎯 وضع الصائد الاستباقي مُفعَّل...")
        predator = TechDebtPredator(repo)
        count = predator.hunt()
        logger.info("🎯 انتهى الصائد — أنشأ %d Issue/Issues.", count)
        return

    # ── فحص صحة استباقي (بلا Issue) ──
    if issue_number == 0:
        logger.info("لم يُحدَّد issue. تشغيل فحص صحة المشروع الاستباقي...")
        _run_health_check(repo)
        return

    # جلب الـ Issue
    try:
        issue = repo.get_issue(issue_number)
    except GithubException as exc:
        logger.error("فشل جلب Issue #%d: %s", issue_number, exc)
        sys.exit(1)

    task = f"العنوان: {issue.title}\nالتفاصيل:\n{issue.body or 'لا يوجد وصف.'}"
    logger.info("=" * 60)
    logger.info("🧬 النواة الواعية تعالج Issue #%d: %s", issue_number, issue.title)
    logger.info("=" * 60)

    # تهيئة الذاكرة الجينية
    genome = GeneticMemory()
    logger.info("🧬 الجينوم يحتوي على %d تجربة مُخزَّنة.", genome.gene_count)

    # ── المرحلة 1: التحليل العميق ──
    logger.info("المرحلة 1/6 ▶ التحليل العميق للمستودع...")
    analyst = Analyst(repo)
    context = analyst.get_context(BASE_BRANCH)

    # ── المرحلة 2: التصميم المعماري (مع الذاكرة الجينية) ──
    logger.info("المرحلة 2/6 ▶ التصميم المعماري مع GPT-4o + الذاكرة الجينية...")
    architect = Architect()
    blueprint = architect.design_solution(task, context)
    logger.info("المعماري صمَّم %d تعديل/تعديلات.", len(blueprint.file_changes))

    if not blueprint.file_changes:
        _comment_and_close(issue, "⚠️ لم يتمكن المعماري من تحديد تعديلات ضرورية. يرجى توضيح المتطلب.")
        return

    # ── المرحلة 3: إنشاء الفرع وكتابة الكود ──
    logger.info("المرحلة 3/6 ▶ إنشاء الفرع وكتابة الكود...")
    branch_name = f"{BRANCH_PREFIX}-{issue_number}"
    _create_branch(repo, branch_name)

    coder = Coder(repo)
    coder.implement_blueprint(blueprint, branch_name)

    # ── المرحلة 4: حلقة التصحيح الذاتي (مع تسجيل الخبرات) ──
    logger.info("المرحلة 4/6 ▶ التحقق الذاتي وحلقة التصحيح...")
    validator = Validator(repo, branch_name)
    changed_files = [fc.file_path for fc in blueprint.file_changes if fc.action != "delete"]

    is_valid, errors = validator.run_local_checks()
    attempts = 0

    while not is_valid and attempts < MAX_CORRECTION_ATTEMPTS:
        attempts += 1
        logger.warning(
            "❌ التحقق فشل (محاولة %d/%d). يبدأ التصحيح الذاتي...",
            attempts,
            MAX_CORRECTION_ATTEMPTS,
        )
        # تصحيح الكود
        coder.fix_errors(errors, branch_name, changed_files)

        # 🧬 حفظ التجربة في الذاكرة الجينية
        error_summary = "\n".join(errors[:10])
        genome.encode_experience(
            task=task,
            error_report=error_summary,
            final_fix=f"حلقة تصحيح ذاتي رقم {attempts} — راجع الملفات: {', '.join(changed_files[:3])}",
            attempt_number=attempts,
        )

        time.sleep(5)
        is_valid, errors = validator.run_local_checks()

    # ── المرحلة 5: المحاكاة الشبحية (Docker Integration Test) ──
    logger.info("المرحلة 5/6 ▶ المحاكاة الشبحية — اختبار التطبيق الحقيقي...")
    phantom = PhantomSandbox()
    phantom_ok, phantom_errors = phantom.run()

    if not phantom_ok:
        logger.warning("👻 Phantom: التطبيق يُعطَّل في بيئة حقيقية — يبدأ التصحيح...")
        coder.fix_errors(phantom_errors, branch_name, changed_files)
        # حفظ خبرة Phantom في الجينوم
        genome.encode_experience(
            task=task,
            error_report="\n".join(phantom_errors[:5]),
            final_fix="إصلاح أعطال اكتُشفت بواسطة Phantom Sandbox",
            attempt_number=MAX_CORRECTION_ATTEMPTS + 1,
        )

    # ── حفظ الذاكرة الجينية في المستودع ──
    logger.info("🧬 حفظ الجينوم في المستودع للدورات القادمة...")
    genome.persist_to_repo()

    # ── المرحلة 6: فتح Pull Request ──
    logger.info("المرحلة 6/6 ▶ فتح Pull Request...")

    validation_summary = _build_validation_summary(is_valid, errors, phantom_ok, phantom_errors, attempts)

    pr_body = (
        f"> 🧬 **تم توليد هذا الحل آلياً بواسطة النواة الواعية (Sentient Core)**\n\n"
        f"يُغلق #{issue_number}\n\n"
        f"{blueprint.to_markdown()}\n\n"
        f"---\n## 🛡️ نتيجة التحقق الذاتي\n{validation_summary}\n\n"
        f"---\n## 🧬 الذاكرة الجينية\n"
        f"الجينوم يحتوي الآن على **{genome.gene_count} تجربة مُخزَّنة** تُستخدَم لمنع تكرار الأخطاء."
    )

    try:
        pr = repo.create_pull(
            title=f"🧬 [Sentient Core] {issue.title}",
            body=pr_body,
            head=branch_name,
            base=BASE_BRANCH,
        )
        logger.info("✅ تم فتح PR #%d: %s", pr.number, pr.html_url)
        issue.create_comment(
            f"🧬 **النواة الواعية أتمَّت عملها!**\n\n"
            f"تم تحليل المتطلب وهندسة الحل وكتابة الكود والتحقق منه والمحاكاة الشبحية.\n\n"
            f"📌 طلب السحب جاهز للمراجعة: {pr.html_url}\n\n"
            f"{validation_summary}"
        )
        issue.edit(state="closed")
    except GithubException as exc:
        logger.error("فشل إنشاء PR: %s", exc)
        issue.create_comment(
            f"⚠️ نفَّذت النواة الواعية التعديلات في الفرع `{branch_name}` "
            f"لكن فشل إنشاء PR تلقائياً: {exc}"
        )


# ──────────────────────────────────────────────────────────
# دوال مساعدة
# ──────────────────────────────────────────────────────────


def _create_branch(repo, branch_name: str) -> None:
    """يُنشئ فرعاً جديداً بناءً على main."""
    try:
        main_sha = repo.get_branch(BASE_BRANCH).commit.sha
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_sha)
        logger.info("تم إنشاء الفرع: %s", branch_name)
    except GithubException as exc:
        if exc.status == 422:
            logger.info("الفرع %s موجود مسبقاً.", branch_name)
        else:
            raise


def _run_health_check(repo) -> None:
    """يُجري فحصاً استباقياً للمشروع."""
    validator = Validator(repo, BASE_BRANCH)
    is_valid, errors = validator.run_local_checks()
    if is_valid:
        logger.info("✅ المشروع في حالة صحية ممتازة.")
    else:
        logger.warning("⚠️ وُجدت %d مشكلة/مشكلات:", len(errors))
        for err in errors[:10]:
            logger.warning("  %s", err)


def _comment_and_close(issue, message: str) -> None:
    """يُعلِّق على Issue ويُغلقه."""
    issue.create_comment(message)
    issue.edit(state="closed")


def _build_validation_summary(
    is_valid: bool,
    errors: list[str],
    phantom_ok: bool,
    phantom_errors: list[str],
    correction_attempts: int,
) -> str:
    """يبني ملخصاً شاملاً لنتائج التحقق."""
    lines = []

    if is_valid:
        lines.append("✅ **اختبارات الوحدة:** اجتازت جميعها.")
    else:
        error_snippet = "\n".join(errors[:10])
        lines.append(
            f"⚠️ **اختبارات الوحدة:** لا تزال هناك مشكلات بعد {correction_attempts} محاولة.\n"
            f"```\n{error_snippet}\n```"
        )

    if phantom_ok:
        lines.append("✅ **المحاكاة الشبحية:** التطبيق يعمل بشكل صحيح في بيئة Docker حقيقية.")
    elif phantom_errors:
        lines.append(
            "⚠️ **المحاكاة الشبحية:** وُجدت أعطال في البيئة الحقيقية.\n"
            "```\n" + "\n".join(phantom_errors[:5]) + "\n```"
        )
    else:
        lines.append("ℹ️ **المحاكاة الشبحية:** Docker غير متاح — تم تخطِّيها.")

    return "\n\n".join(lines)


if __name__ == "__main__":
    main()
