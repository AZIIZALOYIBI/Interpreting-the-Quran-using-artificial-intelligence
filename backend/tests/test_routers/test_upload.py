"""
اختبارات نقطة نهاية /api/upload-pdf.
"""
import io
import pytest


# Minimal valid PDF (1-page, text-free) used across multiple tests.
_MINIMAL_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n"
    b"xref\n0 4\n"
    b"0000000000 65535 f \n"
    b"0000000009 00000 n \n"
    b"0000000058 00000 n \n"
    b"0000000115 00000 n \n"
    b"trailer\n<< /Size 4 /Root 1 0 R >>\n"
    b"startxref\n190\n%%EOF"
)


class TestUploadPDF:
    def test_upload_valid_pdf(self, client):
        """ملف PDF صالح يجب أن يُرجع 200 مع حقل markdown."""
        response = client.post(
            "/api/upload-pdf",
            files={"file": ("test.pdf", io.BytesIO(_MINIMAL_PDF), "application/pdf")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "markdown" in data
        assert "filename" in data
        assert "char_count" in data
        assert data["filename"] == "test.pdf"
        assert data["content_type"] == "application/pdf"
        assert isinstance(data["char_count"], int)

    def test_upload_wrong_content_type(self, client):
        """ملف غير PDF يجب أن يُرجع 415."""
        response = client.post(
            "/api/upload-pdf",
            files={"file": ("doc.txt", io.BytesIO(b"hello"), "text/plain")},
        )
        assert response.status_code == 415

    def test_upload_empty_file(self, client):
        """ملف فارغ يجب أن يُرجع 400."""
        response = client.post(
            "/api/upload-pdf",
            files={"file": ("empty.pdf", io.BytesIO(b""), "application/pdf")},
        )
        assert response.status_code == 400

    def test_upload_too_large_file(self, client):
        """ملف يتجاوز 10 ميجابايت يجب أن يُرجع 413."""
        big_data = b"%PDF-1.4\n" + b"x" * (10 * 1024 * 1024 + 1)
        response = client.post(
            "/api/upload-pdf",
            files={"file": ("big.pdf", io.BytesIO(big_data), "application/pdf")},
        )
        assert response.status_code == 413

    def test_upload_no_file(self, client):
        """طلب بدون ملف يجب أن يُرجع 422."""
        response = client.post("/api/upload-pdf")
        assert response.status_code == 422

    def test_upload_response_schema(self, client):
        """التحقق من مطابقة مخطط الاستجابة الكامل."""
        response = client.post(
            "/api/upload-pdf",
            files={"file": ("quran.pdf", io.BytesIO(_MINIMAL_PDF), "application/pdf")},
        )
        assert response.status_code == 200
        data = response.json()
        assert set(data.keys()) == {"filename", "content_type", "markdown", "char_count"}
        assert data["char_count"] == len(data["markdown"])
