"""
Tests for security headers, enhanced health endpoint, global error handlers,
rate limiting, and input-validation edge cases.
"""
import time
import pytest


class TestSecurityHeaders:
    """Verify OWASP security headers are present on every response."""

    def test_security_headers_on_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert "max-age=" in response.headers.get("Strict-Transport-Security", "")

    def test_security_headers_on_health(self, client):
        response = client.get("/health")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"

    def test_security_headers_on_api_endpoint(self, client):
        response = client.get("/api/categories")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"

    def test_referrer_policy_header(self, client):
        response = client.get("/")
        assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    def test_permissions_policy_header(self, client):
        response = client.get("/")
        assert "geolocation=()" in response.headers.get("Permissions-Policy", "")


class TestEnhancedHealth:
    """Verify the enhanced /health endpoint returns system information."""

    def test_health_status_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_has_uptime(self, client):
        response = client.get("/health")
        data = response.json()
        assert "uptime_seconds" in data
        assert isinstance(data["uptime_seconds"], (int, float))
        assert data["uptime_seconds"] >= 0

    def test_health_has_memory_info(self, client):
        response = client.get("/health")
        data = response.json()
        assert "memory" in data
        assert isinstance(data["memory"], dict)

    def test_health_has_dependencies(self, client):
        response = client.get("/health")
        data = response.json()
        assert "dependencies" in data
        deps = data["dependencies"]
        assert deps.get("ai_service") == "ok"
        assert deps.get("data") == "ok"

    def test_health_uptime_increases(self, client):
        r1 = client.get("/health").json()
        time.sleep(0.05)
        r2 = client.get("/health").json()
        assert r2["uptime_seconds"] >= r1["uptime_seconds"]


class TestErrorHandlers:
    """Verify custom global error handlers return Arabic error messages."""

    def test_404_unknown_path_returns_arabic(self, client):
        response = client.get("/api/nonexistent-endpoint-xyz")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        # Response should contain Arabic characters
        assert any(ord(c) > 0x0600 for c in data["detail"])

    def test_404_unknown_category_has_detail(self, client):
        response = client.get("/api/categories/totally_unknown_99")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_422_validation_error_returns_arabic(self, client):
        # Sending a question that is too short triggers 422
        response = client.post("/api/ask-quran", json={"question": "ما"})
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_422_invalid_category_returns_error(self, client):
        response = client.post(
            "/api/ask-quran",
            json={"question": "ما إرشاد القرآن في الصحة؟", "category": "bad_cat"},
        )
        assert response.status_code == 422

    def test_404_path_included_in_response(self, client):
        response = client.get("/api/does-not-exist")
        assert response.status_code == 404
        data = response.json()
        assert "path" in data


class TestRateLimiting:
    """Verify that the /api/ask-quran rate limiter works correctly."""

    def test_rate_limit_allows_normal_traffic(self, client):
        """A small burst of requests should all succeed."""
        for _ in range(5):
            response = client.post(
                "/api/ask-quran",
                json={"question": "ما إرشاد القرآن في الصبر؟", "category": "self_development"},
            )
            assert response.status_code == 200

    def test_rate_limit_exceeded_returns_429(self, client):
        """Exceeding 20 requests from the same IP in < 1 min should return 429."""
        from routers.chat import _ip_request_times

        # Inject 20 recent timestamps for the test-client IP to simulate hitting the limit
        test_ip = "testclient"  # TestClient uses "testclient" as host
        now = time.time()
        for i in range(20):
            _ip_request_times[test_ip].append(now - i * 0.1)

        response = client.post(
            "/api/ask-quran",
            json={"question": "ما إرشاد القرآن في الصبر والشكر؟"},
        )
        assert response.status_code == 429
        data = response.json()
        assert "detail" in data
    def test_rate_limit_window_expires(self, client):
        """After clearing old timestamps the request should succeed again."""
        from routers.chat import _ip_request_times

        test_ip = "testclient"
        _ip_request_times[test_ip].clear()

        response = client.post(
            "/api/ask-quran",
            json={"question": "ما هو الصبر في الإسلام؟", "category": "self_development"},
        )
        assert response.status_code == 200


class TestInputValidationEdgeCases:
    """Additional edge cases for input validation beyond existing tests."""

    def test_question_exactly_five_chars(self, client):
        response = client.post("/api/ask-quran", json={"question": "الصبر"})
        assert response.status_code == 200

    def test_question_exactly_2000_chars(self, client):
        response = client.post("/api/ask-quran", json={"question": "أ" * 2000})
        assert response.status_code == 200

    def test_question_2001_chars_rejected(self, client):
        response = client.post("/api/ask-quran", json={"question": "أ" * 2001})
        assert response.status_code == 422

    def test_missing_question_field(self, client):
        response = client.post("/api/ask-quran", json={"category": "medicine"})
        assert response.status_code == 422

    def test_null_question_rejected(self, client):
        response = client.post("/api/ask-quran", json={"question": None})
        assert response.status_code == 422

    def test_whitespace_only_question_too_short(self, client):
        """Pure whitespace shorter than 5 chars should be rejected."""
        response = client.post("/api/ask-quran", json={"question": "   "})
        assert response.status_code == 422

    def test_response_answer_non_empty(self, client):
        response = client.post(
            "/api/ask-quran",
            json={"question": "ما إرشاد القرآن في الأخلاق؟", "category": "ethics"},
        )
        assert response.status_code == 200
        assert len(response.json()["answer"]) > 0
