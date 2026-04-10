"""
معالجة رفع ملفات PDF وتحويلها إلى Markdown باستخدام markitdown.
"""
import logging
import tempfile
import os

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from markitdown import MarkItDown

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["upload"])

_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
_ALLOWED_CONTENT_TYPES = {"application/pdf"}


class UploadResponse(BaseModel):
    filename: str
    content_type: str
    markdown: str
    char_count: int


@router.post("/upload-pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> UploadResponse:
    """
    تحويل ملف PDF إلى Markdown باستخدام markitdown.

    - يقبل ملفات PDF فقط
    - الحجم الأقصى 10 ميجابايت
    - يعيد المحتوى بصيغة Markdown
    """
    if file.content_type not in _ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail="نوع الملف غير مدعوم. يُرجى رفع ملف PDF فقط.",
        )

    data = await file.read()
    if len(data) > _MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="حجم الملف يتجاوز الحد المسموح به (10 ميجابايت).",
        )

    if not data:
        raise HTTPException(status_code=400, detail="الملف فارغ.")

    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        try:
            md = MarkItDown(enable_plugins=True)
            result = md.convert(tmp_path)
            markdown_text = result.text_content or ""
        finally:
            os.unlink(tmp_path)

    except HTTPException:
        raise
    except Exception as exc:
        logger.error("فشل تحويل PDF إلى Markdown: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="فشل معالجة الملف. يُرجى التحقق من أن الملف صالح والمحاولة مجدداً.",
        ) from exc

    logger.info(
        "تم تحويل PDF '%s' بنجاح — %d حرف",
        file.filename,
        len(markdown_text),
    )

    return UploadResponse(
        filename=file.filename or "unknown.pdf",
        content_type=file.content_type or "application/pdf",
        markdown=markdown_text,
        char_count=len(markdown_text),
    )
