"""Search Service — Handles Quran search operations."""

from data.quran_data import QURAN_VERSES


def search_quran(query: str) -> dict:
    if not query or len(query) < 2:
        return {"verses": [], "total_count": 0, "query": query, "suggestions": []}

    results = []
    query_lower = query.strip()

    for verse in QURAN_VERSES:
        text = verse.get("text_simple", "")
        uthmani = verse.get("text_uthmani", "")
        translation = verse.get("translation", "")
        if query_lower in text or query_lower in uthmani or query_lower in translation:
            results.append(verse)

    suggestions = _get_search_suggestions(query)

    return {
        "verses": results[:50],
        "total_count": len(results),
        "query": query,
        "suggestions": suggestions,
    }


def _get_search_suggestions(query: str) -> list:
    all_suggestions = ["الصبر", "الرحمة", "التوبة", "العدل", "العلم", "الصلاة", "الزكاة", "الجنة", "التقوى", "الشكر", "الإيمان", "الحكمة", "المغفرة", "النور", "الهداية"]
    return [s for s in all_suggestions if query in s or s in query][:5]
