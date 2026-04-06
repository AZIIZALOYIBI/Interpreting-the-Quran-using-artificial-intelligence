from typing import List, Dict, Any

SCHOLARS = [
    {"name": "Ibn Kathir", "name_ar": "ابن كثير", "source": "تفسير القرآن العظيم"},
    {"name": "Al-Tabari", "name_ar": "الطبري", "source": "جامع البيان"},
    {"name": "Al-Qurtubi", "name_ar": "القرطبي", "source": "الجامع لأحكام القرآن"},
    {"name": "Al-Saadi", "name_ar": "السعدي", "source": "تيسير الكريم الرحمن"},
]

SAMPLE_TAFSIR = [
    {
        "id": 1,
        "ayah_id": 1,
        "scholar_name": "Ibn Kathir",
        "scholar_name_ar": "ابن كثير",
        "text": "هذه الآية الكريمة تُبيِّن عظيم فضل الله ورحمته بعباده وإحاطة علمه بجميع أحوالهم.",
        "source": "تفسير القرآن العظيم",
    },
    {
        "id": 2,
        "ayah_id": 1,
        "scholar_name": "Al-Tabari",
        "scholar_name_ar": "الطبري",
        "text": "قال الطبري رحمه الله: يعني بذلك الإخبار عن كمال صفاته وجلال أسمائه الحسنى.",
        "source": "جامع البيان",
    },
    {
        "id": 3,
        "ayah_id": 1,
        "scholar_name": "Al-Qurtubi",
        "scholar_name_ar": "القرطبي",
        "text": "استنبط القرطبي من هذه الآية أحكاماً فقهية تتعلق بمعاملات الناس وتنظيم حياتهم.",
        "source": "الجامع لأحكام القرآن",
    },
]


def get_tafsir(ayah_id: int, scholar: str = "all") -> List[Dict[str, Any]]:
    if scholar == "all":
        return [dict(t, ayah_id=ayah_id) for t in SAMPLE_TAFSIR]
    return [dict(t, ayah_id=ayah_id) for t in SAMPLE_TAFSIR if t["scholar_name_ar"] == scholar]


def get_available_scholars() -> List[Dict[str, Any]]:
    return SCHOLARS
