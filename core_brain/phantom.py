"""
المحاكاة الشبحية (Phantom Sandbox)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
تبني حاوية Docker خفيفة وتختبر التطبيق الكامل بطلبات HTTP حقيقية
قبل فتح أي Pull Request.

المراحل:
  1. بناء صورة Docker من docker-compose.yml أو Dockerfile
  2. تشغيل الحاوية مع انتظار جاهزية الخادم (health check)
  3. إرسال طلبات HTTP اختبارية إلى نقاط النهاية الجوهرية
  4. تحليل الاستجابات والسجلات للكشف عن الأعطال
  5. إيقاف الحاوية تنظيفاً

القرار:
  (True, [])           → التطبيق يعمل في العالم الحقيقي ✅
  (False, [أخطاء])     → الكود يُعطِّل شيئاً → يُعاد للـ Coder للإصلاح
"""

from __future__ import annotations

import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

REPO_ROOT = Path(os.getenv("GITHUB_WORKSPACE", "."))
BACKEND_PORT = 18500          # منفذ ثابت غير قياسي لتفادي التعارض مع العمليات الأخرى
STARTUP_TIMEOUT = 60          # ثوانٍ للانتظار حتى يستعد الخادم
HTTP_TIMEOUT = 10             # timeout لكل طلب HTTP

# نقاط النهاية التي تُختبَر مع الاستجابات المتوقَّعة
PROBE_ENDPOINTS: list[dict] = [
    {
        "method": "GET",
        "path": "/health",
        "expected_status": 200,
        "description": "فحص الصحة",
    },
    {
        "method": "GET",
        "path": "/api/categories",
        "expected_status": 200,
        "description": "قائمة الفئات",
    },
    {
        "method": "POST",
        "path": "/api/ask-quran",
        "body": '{"question": "ما معنى الصبر في القرآن؟", "category": "general"}',
        "expected_status": 200,
        "description": "السؤال القرآني",
    },
]


class PhantomSandbox:
    """
    يُنشئ بيئة اختبار Docker مؤقتة ويُجري مسبارات HTTP حقيقية.
    """

    def __init__(self) -> None:
        self._container_id: Optional[str] = None
        self._docker_available = self._check_docker()

    # ──────────────────────────────────────────────────────
    # الواجهة العامة
    # ──────────────────────────────────────────────────────

    def run(self) -> tuple[bool, list[str]]:
        """
        يُشغِّل دورة الاختبار الكاملة.

        Returns
        -------
        tuple[bool, list[str]]
            (True, [])          → التطبيق يعمل بشكل صحيح.
            (False, [أخطاء])    → وُجدت أعطال.
        """
        if not self._docker_available:
            logger.info("👻 Phantom Sandbox: Docker غير متاح — تخطِّي المحاكاة.")
            return True, []

        errors: list[str] = []

        try:
            logger.info("👻 Phantom Sandbox: بناء الحاوية وتشغيلها...")
            self._build_image()
            self._start_container()

            if not self._wait_for_ready():
                logs = self._get_container_logs()
                return False, [
                    "[Phantom] فشل تشغيل الخادم في الوقت المحدد.",
                    f"[Phantom Logs]\n{logs}",
                ]

            logger.info("👻 Phantom Sandbox: الخادم جاهز — يبدأ المسح بالطلبات...")
            probe_errors = self._run_probes()
            errors.extend(probe_errors)

        except Exception as exc:
            logger.warning("👻 Phantom Sandbox: استثناء غير متوقع: %s", exc)
            errors.append(f"[Phantom] استثناء: {exc}")
        finally:
            self._cleanup()

        is_healthy = len(errors) == 0
        if is_healthy:
            logger.info("👻 Phantom Sandbox ✅: التطبيق يعمل بشكل سليم في بيئة حقيقية.")
        else:
            logger.warning("👻 Phantom Sandbox ❌: %d عطل/أعطال مكتشفة.", len(errors))

        return is_healthy, errors

    # ──────────────────────────────────────────────────────
    # Docker helpers
    # ──────────────────────────────────────────────────────

    def _check_docker(self) -> bool:
        """يتحقق من توفُّر Docker في البيئة."""
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10,
        )
        available = result.returncode == 0
        if not available:
            logger.info("👻 Phantom Sandbox: Docker daemon غير متاح.")
        return available

    def _build_image(self) -> None:
        """يبني صورة Docker من Dockerfile الخاصة بالـ Backend."""
        dockerfile = REPO_ROOT / "backend" / "Dockerfile"
        context = REPO_ROOT / "backend"

        if not dockerfile.exists():
            # إنشاء Dockerfile مؤقت خفيف إذا لم يكن موجوداً
            dockerfile.write_text(
                "FROM python:3.11-slim\n"
                "WORKDIR /app\n"
                "COPY requirements.txt .\n"
                "RUN pip install --no-cache-dir -r requirements.txt\n"
                "COPY . .\n"
                "CMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\","
                f" \"--port\", \"{BACKEND_PORT}\"]\n"
            )

        subprocess.run(
            ["docker", "build", "-t", "quran-phantom-test", str(context)],
            capture_output=True,
            check=True,
            cwd=str(REPO_ROOT),
        )
        logger.info("👻 Phantom: تم بناء الصورة quran-phantom-test.")

    def _start_container(self) -> None:
        """يُشغِّل الحاوية في الخلفية."""
        result = subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--rm",
                "-p",
                f"{BACKEND_PORT}:{BACKEND_PORT}",
                "-e",
                "DEMO_MODE=true",
                "--name",
                "quran-phantom",
                "quran-phantom-test",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self._container_id = result.stdout.strip()
        logger.info("👻 Phantom: الحاوية تعمل — ID: %s", self._container_id[:12])

    def _wait_for_ready(self) -> bool:
        """ينتظر حتى يستجيب الخادم على /health."""
        base_url = f"http://localhost:{BACKEND_PORT}"
        deadline = time.time() + STARTUP_TIMEOUT

        while time.time() < deadline:
            try:
                result = subprocess.run(
                    [
                        "curl",
                        "-sf",
                        "--max-time",
                        "3",
                        f"{base_url}/health",
                    ],
                    capture_output=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    logger.info("👻 Phantom: الخادم جاهز على المنفذ %d.", BACKEND_PORT)
                    return True
            except Exception:
                pass
            time.sleep(3)

        return False

    def _run_probes(self) -> list[str]:
        """يُرسل طلبات HTTP اختبارية ويُجمع الأخطاء."""
        errors: list[str] = []
        base_url = f"http://localhost:{BACKEND_PORT}"

        for probe in PROBE_ENDPOINTS:
            method = probe["method"]
            url = base_url + probe["path"]
            description = probe["description"]

            cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", str(HTTP_TIMEOUT)]

            if method == "POST":
                cmd += ["-X", "POST", "-H", "Content-Type: application/json"]
                if "body" in probe:
                    cmd += ["-d", probe["body"]]

            cmd.append(url)

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=HTTP_TIMEOUT + 5)
                status_code = int(result.stdout.strip() or "0")
                expected = probe.get("expected_status", 200)

                if status_code == expected:
                    logger.info("👻 Probe ✅ %s → HTTP %d", description, status_code)
                else:
                    err = f"[Phantom Probe] {description}: توقَّعت {expected}، حصلت على {status_code} — {url}"
                    logger.warning("👻 Probe ❌ %s", err)
                    errors.append(err)
            except Exception as exc:
                errors.append(f"[Phantom Probe] {description}: استثناء — {exc}")

        return errors

    def _get_container_logs(self) -> str:
        """يجلب سجلات الحاوية لمساعدة Coder في التصحيح."""
        if not self._container_id:
            return ""
        try:
            result = subprocess.run(
                ["docker", "logs", "--tail", "50", self._container_id],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.stdout + result.stderr
        except Exception:
            return ""

    def _cleanup(self) -> None:
        """يُوقِف الحاوية ويُزيلها."""
        try:
            subprocess.run(
                ["docker", "stop", "quran-phantom"],
                capture_output=True,
                timeout=15,
            )
            logger.info("👻 Phantom Sandbox: تم إيقاف الحاوية وتنظيفها.")
        except Exception:
            pass
