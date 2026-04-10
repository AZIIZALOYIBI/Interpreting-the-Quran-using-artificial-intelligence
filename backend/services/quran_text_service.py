"""
محرك البحث في نص القرآن الكريم.

يُحمِّل كامل المصحف (6236 آية) من الملفات المُرفقة محلياً
ويوفر دوال بحث مستندة إلى مطابقة الكلمات العربية بعد تطبيع النص.

لا يُولِّد هذا الوحدة أي نص من تلقاء نفسها، ولا تستخدم ذكاءً اصطناعياً.
كل آية مُرجَعة مأخوذة حرفياً من مصحف مُرفق في المستودع.
"""
from __future__ import annotations

import json
import logging
import re
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_DATA_DIR = Path(__file__).parent.parent / "data" / "quran_corpus"
_QURAN_JSON = _DATA_DIR / "quran.json"
_CHAPTERS_JSON = _DATA_DIR / "chapters.json"

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Ayah:
    surah_number: int
    ayah_number: int
    text: str               # النص بالرسم العثماني
    surah_name_ar: str      # اسم السورة بالعربية
    surah_name_en: str      # الاسم بالحروف اللاتينية
    surah_type: str         # "meccan" | "medinan"

    def to_dict(self) -> dict:
        return {
            "id": self.surah_number * 1000 + self.ayah_number,
            "surah_id": self.surah_number,
            "surah_name": self.surah_name_en,
            "surah_name_ar": self.surah_name_ar,
            "ayah_number": self.ayah_number,
            "text_uthmani": self.text,
            "text_simple": _strip_diacritics(self.text),
        }


# ---------------------------------------------------------------------------
# Arabic text normalisation (used for search only, never for display)
# ---------------------------------------------------------------------------

_DIACRITICS = re.compile(r"[\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]")
_TATWEEL = re.compile(r"\u0640")
_SUPERSCRIPT_ALEF = re.compile(r"\u0670")

_ALEF_VARIANTS = re.compile(r"[أإآٱ]")
_YA_VARIANTS = re.compile(r"ى")
_HA_VARIANTS = re.compile(r"ة")


def _strip_diacritics(text: str) -> str:
    """Remove Arabic diacritics (tashkeel) from *text*."""
    return _DIACRITICS.sub("", _TATWEEL.sub("", text))


def _normalize(text: str) -> str:
    """Normalise Arabic text for approximate keyword matching."""
    text = _strip_diacritics(text)
    text = _ALEF_VARIANTS.sub("ا", text)
    text = _YA_VARIANTS.sub("ي", text)
    text = _HA_VARIANTS.sub("ه", text)
    return text


def _tokenize(text: str) -> List[str]:
    """Split normalised Arabic text into tokens (words ≥ 3 chars)."""
    return [w for w in re.split(r"\s+|[،؛.؟!٫٪\-–—()[\]{}<>«»\"']+", _normalize(text)) if len(w) >= 3]


# ---------------------------------------------------------------------------
# Category keyword index for boosting relevant surahs/ayahs
# ---------------------------------------------------------------------------

_CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "medicine": ["شفاء", "مرض", "صحة", "طب", "علاج", "دواء", "صيام", "غذاء", "عسل", "ماء"],
    "work": ["رزق", "عمل", "بيع", "تجارة", "ربا", "مال", "اقتصاد", "كسب", "انتشروا"],
    "science": ["علم", "اقرا", "عقل", "فكر", "بحث", "كون", "سماء", "ارض", "خلق", "تفكر"],
    "family": ["زواج", "اسره", "والدين", "ابناء", "ارحام", "نساء", "مودة", "رحمة", "اطفال"],
    "self_development": ["صبر", "شكر", "نفس", "ايمان", "توكل", "اراده", "هدى", "تقوى"],
    "law": ["عدل", "حق", "حكم", "قضاء", "شهادة", "ظلم", "حلال", "حرام", "امانة", "ميثاق"],
    "environment": ["ارض", "ماء", "نبات", "حيوان", "فساد", "بحر", "ريح", "مطر", "شجر"],
    "ethics": ["اخلاق", "تواضع", "كبر", "صدق", "كذب", "امانة", "غيبه", "حسد", "عفو", "كرم"],
    "general": [],
}

# ---------------------------------------------------------------------------
# Corpus singleton
# ---------------------------------------------------------------------------

_lock = threading.Lock()
_ayahs: Optional[List[Ayah]] = None          # flat list of all 6236 ayahs
_normalized: Optional[List[str]] = None       # parallel normalised-text list


def _load_corpus() -> None:
    """Load ayahs from bundled JSON files into memory (called once)."""
    global _ayahs, _normalized

    if not _QURAN_JSON.exists() or not _CHAPTERS_JSON.exists():
        raise FileNotFoundError(
            f"بيانات القرآن غير موجودة في {_DATA_DIR}. "
            "شغّل scripts/download_quran.py لتحميلها."
        )

    with _QURAN_JSON.open(encoding="utf-8") as f:
        quran_raw: Dict[str, list] = json.load(f)

    with _CHAPTERS_JSON.open(encoding="utf-8") as f:
        chapters_raw: list = json.load(f)

    # Build surah metadata lookup: surah_number → (name_ar, name_en, type)
    surah_meta: Dict[int, tuple] = {}
    for ch in chapters_raw:
        sid = int(ch["id"])
        surah_meta[sid] = (ch["name"], ch["transliteration"], ch.get("type", ""))

    ayahs: List[Ayah] = []
    for surah_str, verses in quran_raw.items():
        sid = int(surah_str)
        name_ar, name_en, s_type = surah_meta.get(sid, ("", "", ""))
        for v in verses:
            text = v["text"].lstrip("\ufeff")   # strip BOM if present
            ayahs.append(
                Ayah(
                    surah_number=sid,
                    ayah_number=int(v["verse"]),
                    text=text,
                    surah_name_ar=name_ar,
                    surah_name_en=name_en,
                    surah_type=s_type,
                )
            )

    _ayahs = ayahs
    _normalized = [_normalize(a.text) for a in ayahs]
    logger.info("تم تحميل القرآن الكريم: %d آية من 114 سورة", len(_ayahs))


def _ensure_loaded() -> None:
    global _ayahs
    if _ayahs is None:
        with _lock:
            if _ayahs is None:
                _load_corpus()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def search_ayahs(query: str, category: Optional[str] = None, top_k: int = 5) -> List[Ayah]:
    """Search the Quran corpus for ayahs relevant to *query*.

    Uses token-overlap scoring between the normalised query and each ayah's
    normalised text, boosted by category-specific keywords.

    Args:
        query: Arabic search query (the user's question).
        category: Optional category ID for boosting relevant keywords.
        top_k: Maximum number of ayahs to return.

    Returns:
        Up to *top_k* :class:`Ayah` objects ordered by relevance score (desc).
        Returns an empty list only when no query tokens matched any ayah.
    """
    _ensure_loaded()
    assert _ayahs is not None and _normalized is not None

    query_tokens = set(_tokenize(query))

    # Merge in category keywords for richer matching
    if category and category in _CATEGORY_KEYWORDS:
        cat_tokens = set(_normalize(kw) for kw in _CATEGORY_KEYWORDS[category])
        query_tokens |= cat_tokens

    if not query_tokens:
        return []

    scores: List[float] = []
    for norm_text in _normalized:
        ayah_tokens = set(_tokenize(norm_text))
        # Soft overlap: a query token matches an ayah token if one is a substring
        # of the other (handles ال definite article prefix, e.g. شفاء ↔ الشفاء).
        # Both tokens must be ≥ 3 chars to prevent spurious short-string matches.
        overlap_count = 0
        for qt in query_tokens:
            if len(qt) < 3:
                continue
            for at in ayah_tokens:
                if len(at) < 3 and (qt in at or at in qt):
                    continue
                if qt in at or at in qt:
                    overlap_count += 1
                    break
        score = overlap_count / (len(ayah_tokens) + 1)
        score += overlap_count * 0.1
        scores.append(score)

    # Pick top_k indices with score > 0
    ranked = sorted(
        (i for i, s in enumerate(scores) if s > 0),
        key=lambda i: scores[i],
        reverse=True,
    )[:top_k]

    return [_ayahs[i] for i in ranked]


def get_ayah(surah: int, verse: int) -> Optional[Ayah]:
    """Return a single :class:`Ayah` by surah and verse number, or None."""
    _ensure_loaded()
    assert _ayahs is not None
    for a in _ayahs:
        if a.surah_number == surah and a.ayah_number == verse:
            return a
    return None


def total_ayahs() -> int:
    """Return the total number of loaded ayahs."""
    _ensure_loaded()
    assert _ayahs is not None
    return len(_ayahs)


def reset_corpus() -> None:
    """Unload the corpus from memory (used in tests)."""
    global _ayahs, _normalized
    with _lock:
        _ayahs = None
        _normalized = None
