"use client";
import { useState, useCallback, useMemo } from "react";
import type { Ayah, SurahInfo } from "@/types";

const SURAHS: SurahInfo[] = [
  { id: 1, nameAr: "الفاتحة", nameEn: "Al-Fatihah", ayahCount: 7, revelationType: "meccan" },
  { id: 2, nameAr: "البقرة", nameEn: "Al-Baqarah", ayahCount: 286, revelationType: "medinan" },
  { id: 3, nameAr: "آل عمران", nameEn: "Ali 'Imran", ayahCount: 200, revelationType: "medinan" },
  { id: 4, nameAr: "النساء", nameEn: "An-Nisa", ayahCount: 176, revelationType: "medinan" },
  { id: 5, nameAr: "المائدة", nameEn: "Al-Maidah", ayahCount: 120, revelationType: "medinan" },
  { id: 6, nameAr: "الأنعام", nameEn: "Al-An'am", ayahCount: 165, revelationType: "meccan" },
  { id: 7, nameAr: "الأعراف", nameEn: "Al-A'raf", ayahCount: 206, revelationType: "meccan" },
  { id: 9, nameAr: "التوبة", nameEn: "At-Tawbah", ayahCount: 129, revelationType: "medinan" },
  { id: 10, nameAr: "يونس", nameEn: "Yunus", ayahCount: 109, revelationType: "meccan" },
  { id: 12, nameAr: "يوسف", nameEn: "Yusuf", ayahCount: 111, revelationType: "meccan" },
  { id: 13, nameAr: "الرعد", nameEn: "Ar-Ra'd", ayahCount: 43, revelationType: "medinan" },
  { id: 14, nameAr: "إبراهيم", nameEn: "Ibrahim", ayahCount: 52, revelationType: "meccan" },
  { id: 15, nameAr: "الحجر", nameEn: "Al-Hijr", ayahCount: 99, revelationType: "meccan" },
  { id: 17, nameAr: "الإسراء", nameEn: "Al-Isra", ayahCount: 111, revelationType: "meccan" },
  { id: 18, nameAr: "الكهف", nameEn: "Al-Kahf", ayahCount: 110, revelationType: "meccan" },
  { id: 19, nameAr: "مريم", nameEn: "Maryam", ayahCount: 98, revelationType: "meccan" },
  { id: 20, nameAr: "طه", nameEn: "Taha", ayahCount: 135, revelationType: "meccan" },
  { id: 23, nameAr: "المؤمنون", nameEn: "Al-Mu'minun", ayahCount: 118, revelationType: "meccan" },
  { id: 24, nameAr: "النور", nameEn: "An-Nur", ayahCount: 64, revelationType: "medinan" },
  { id: 25, nameAr: "الفرقان", nameEn: "Al-Furqan", ayahCount: 77, revelationType: "meccan" },
  { id: 31, nameAr: "لقمان", nameEn: "Luqman", ayahCount: 34, revelationType: "meccan" },
  { id: 36, nameAr: "يس", nameEn: "Ya-Sin", ayahCount: 83, revelationType: "meccan" },
  { id: 39, nameAr: "الزمر", nameEn: "Az-Zumar", ayahCount: 75, revelationType: "meccan" },
  { id: 40, nameAr: "غافر", nameEn: "Ghafir", ayahCount: 85, revelationType: "meccan" },
  { id: 41, nameAr: "فصلت", nameEn: "Fussilat", ayahCount: 54, revelationType: "meccan" },
  { id: 44, nameAr: "الدخان", nameEn: "Ad-Dukhan", ayahCount: 59, revelationType: "meccan" },
  { id: 45, nameAr: "الجاثية", nameEn: "Al-Jathiyah", ayahCount: 37, revelationType: "meccan" },
  { id: 46, nameAr: "الأحقاف", nameEn: "Al-Ahqaf", ayahCount: 35, revelationType: "meccan" },
  { id: 47, nameAr: "محمد", nameEn: "Muhammad", ayahCount: 38, revelationType: "medinan" },
  { id: 48, nameAr: "الفتح", nameEn: "Al-Fath", ayahCount: 29, revelationType: "medinan" },
  { id: 49, nameAr: "الحجرات", nameEn: "Al-Hujurat", ayahCount: 18, revelationType: "medinan" },
  { id: 50, nameAr: "ق", nameEn: "Qaf", ayahCount: 45, revelationType: "meccan" },
  { id: 51, nameAr: "الذاريات", nameEn: "Adh-Dhariyat", ayahCount: 60, revelationType: "meccan" },
  { id: 55, nameAr: "الرحمن", nameEn: "Ar-Rahman", ayahCount: 78, revelationType: "medinan" },
  { id: 56, nameAr: "الواقعة", nameEn: "Al-Waqi'ah", ayahCount: 96, revelationType: "meccan" },
  { id: 57, nameAr: "الحديد", nameEn: "Al-Hadid", ayahCount: 29, revelationType: "medinan" },
  { id: 59, nameAr: "الحشر", nameEn: "Al-Hashr", ayahCount: 24, revelationType: "medinan" },
  { id: 62, nameAr: "الجمعة", nameEn: "Al-Jumu'ah", ayahCount: 11, revelationType: "medinan" },
  { id: 67, nameAr: "الملك", nameEn: "Al-Mulk", ayahCount: 30, revelationType: "meccan" },
  { id: 71, nameAr: "نوح", nameEn: "Nuh", ayahCount: 28, revelationType: "meccan" },
  { id: 73, nameAr: "المزمل", nameEn: "Al-Muzzammil", ayahCount: 20, revelationType: "meccan" },
  { id: 74, nameAr: "المدثر", nameEn: "Al-Muddaththir", ayahCount: 56, revelationType: "meccan" },
  { id: 76, nameAr: "الإنسان", nameEn: "Al-Insan", ayahCount: 31, revelationType: "medinan" },
  { id: 78, nameAr: "النبأ", nameEn: "An-Naba", ayahCount: 40, revelationType: "meccan" },
  { id: 79, nameAr: "النازعات", nameEn: "An-Nazi'at", ayahCount: 46, revelationType: "meccan" },
  { id: 80, nameAr: "عبس", nameEn: "'Abasa", ayahCount: 42, revelationType: "meccan" },
  { id: 84, nameAr: "الانشقاق", nameEn: "Al-Inshiqaq", ayahCount: 25, revelationType: "meccan" },
  { id: 87, nameAr: "الأعلى", nameEn: "Al-A'la", ayahCount: 19, revelationType: "meccan" },
  { id: 89, nameAr: "الفجر", nameEn: "Al-Fajr", ayahCount: 30, revelationType: "meccan" },
  { id: 93, nameAr: "الضحى", nameEn: "Ad-Duha", ayahCount: 11, revelationType: "meccan" },
  { id: 94, nameAr: "الشرح", nameEn: "Ash-Sharh", ayahCount: 8, revelationType: "meccan" },
  { id: 95, nameAr: "التين", nameEn: "At-Tin", ayahCount: 8, revelationType: "meccan" },
  { id: 96, nameAr: "العلق", nameEn: "Al-'Alaq", ayahCount: 19, revelationType: "meccan" },
  { id: 97, nameAr: "القدر", nameEn: "Al-Qadr", ayahCount: 5, revelationType: "meccan" },
  { id: 98, nameAr: "البينة", nameEn: "Al-Bayyinah", ayahCount: 8, revelationType: "medinan" },
  { id: 99, nameAr: "الزلزلة", nameEn: "Az-Zalzalah", ayahCount: 8, revelationType: "medinan" },
  { id: 100, nameAr: "العاديات", nameEn: "Al-'Adiyat", ayahCount: 11, revelationType: "meccan" },
  { id: 101, nameAr: "القارعة", nameEn: "Al-Qari'ah", ayahCount: 11, revelationType: "meccan" },
  { id: 102, nameAr: "التكاثر", nameEn: "At-Takathur", ayahCount: 8, revelationType: "meccan" },
  { id: 103, nameAr: "العصر", nameEn: "Al-'Asr", ayahCount: 3, revelationType: "meccan" },
  { id: 104, nameAr: "الهمزة", nameEn: "Al-Humazah", ayahCount: 9, revelationType: "meccan" },
  { id: 105, nameAr: "الفيل", nameEn: "Al-Fil", ayahCount: 5, revelationType: "meccan" },
  { id: 106, nameAr: "قريش", nameEn: "Quraysh", ayahCount: 4, revelationType: "meccan" },
  { id: 107, nameAr: "الماعون", nameEn: "Al-Ma'un", ayahCount: 7, revelationType: "meccan" },
  { id: 108, nameAr: "الكوثر", nameEn: "Al-Kawthar", ayahCount: 3, revelationType: "meccan" },
  { id: 109, nameAr: "الكافرون", nameEn: "Al-Kafirun", ayahCount: 6, revelationType: "meccan" },
  { id: 110, nameAr: "النصر", nameEn: "An-Nasr", ayahCount: 3, revelationType: "medinan" },
  { id: 111, nameAr: "المسد", nameEn: "Al-Masad", ayahCount: 5, revelationType: "meccan" },
  { id: 112, nameAr: "الإخلاص", nameEn: "Al-Ikhlas", ayahCount: 4, revelationType: "meccan" },
  { id: 113, nameAr: "الفلق", nameEn: "Al-Falaq", ayahCount: 5, revelationType: "meccan" },
  { id: 114, nameAr: "الناس", nameEn: "An-Nas", ayahCount: 6, revelationType: "meccan" },
];

const SAMPLE_AYAHS: Record<number, Ayah[]> = {
  1: [
    { id: 1, surah_id: 1, surah_name: "Al-Fatihah", surah_name_ar: "الفاتحة", ayah_number: 1, text_uthmani: "بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ", text_simple: "بسم الله الرحمن الرحيم" },
    { id: 2, surah_id: 1, surah_name: "Al-Fatihah", surah_name_ar: "الفاتحة", ayah_number: 2, text_uthmani: "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", text_simple: "الحمد لله رب العالمين" },
    { id: 3, surah_id: 1, surah_name: "Al-Fatihah", surah_name_ar: "الفاتحة", ayah_number: 3, text_uthmani: "الرَّحْمَـٰنِ الرَّحِيمِ", text_simple: "الرحمن الرحيم" },
    { id: 4, surah_id: 1, surah_name: "Al-Fatihah", surah_name_ar: "الفاتحة", ayah_number: 4, text_uthmani: "مَالِكِ يَوْمِ الدِّينِ", text_simple: "مالك يوم الدين" },
    { id: 5, surah_id: 1, surah_name: "Al-Fatihah", surah_name_ar: "الفاتحة", ayah_number: 5, text_uthmani: "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ", text_simple: "إياك نعبد وإياك نستعين" },
    { id: 6, surah_id: 1, surah_name: "Al-Fatihah", surah_name_ar: "الفاتحة", ayah_number: 6, text_uthmani: "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ", text_simple: "اهدنا الصراط المستقيم" },
    { id: 7, surah_id: 1, surah_name: "Al-Fatihah", surah_name_ar: "الفاتحة", ayah_number: 7, text_uthmani: "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ", text_simple: "صراط الذين أنعمت عليهم غير المغضوب عليهم ولا الضالين" },
  ],
};

export default function QuranReader() {
  const [selectedSurah, setSelectedSurah] = useState<SurahInfo>(SURAHS[0]);
  const [ayahs, setAyahs] = useState<Ayah[]>(SAMPLE_AYAHS[1] || []);
  const [loading, setLoading] = useState(false);
  const [fontSize, setFontSize] = useState(1.5);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredSurahs = useMemo(() => {
    const q = searchQuery.trim().replace(/[\u064B-\u065F]/g, "");
    if (!q) return SURAHS;
    return SURAHS.filter((s) => s.nameAr.replace(/[\u064B-\u065F]/g, "").includes(q));
  }, [searchQuery]);

  const loadSurah = useCallback(async (surah: SurahInfo) => {
    setSelectedSurah(surah);
    setLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/quran/surah/${surah.id}`);
      if (res.ok) {
        const data = await res.json();
        setAyahs(data.ayahs || []);
      } else {
        setAyahs(SAMPLE_AYAHS[surah.id] || []);
      }
    } catch {
      setAyahs(SAMPLE_AYAHS[surah.id] || []);
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div className="flex flex-col lg:flex-row gap-6 min-h-screen">
      {/* Surah list */}
      <aside
        className="lg:w-72 rounded-xl overflow-hidden flex-shrink-0"
        style={{ backgroundColor: "white", border: "1px solid var(--claude-border)", boxShadow: "0 2px 8px rgba(28,25,23,0.06)" }}
      >
        <div
          className="p-4"
          style={{ backgroundColor: "var(--claude-dark)", borderBottom: "1px solid var(--claude-dark-3)" }}
        >
          <h2 className="font-bold text-lg text-white mb-3">فهرس السور</h2>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="ابحث عن سورة..."
            dir="rtl"
            className="w-full rounded-lg px-3 py-2 text-sm focus:outline-none"
            style={{
              backgroundColor: "var(--claude-dark-2)",
              border: "1px solid var(--claude-dark-3)",
              color: "white",
            }}
          />
        </div>
        <div className="overflow-y-auto max-h-[calc(100vh-260px)]">
          {filteredSurahs.map((surah) => (
            <button
              key={surah.id}
              onClick={() => loadSurah(surah)}
              className="surah-item w-full text-right px-4 py-3 flex items-center justify-between transition-colors"
              style={{
                borderBottom: "1px solid var(--claude-border-light)",
                backgroundColor: selectedSurah.id === surah.id ? "var(--claude-accent-light)" : "transparent",
                color: selectedSurah.id === surah.id ? "var(--claude-accent-hover)" : "var(--claude-text-secondary)",
                fontWeight: selectedSurah.id === surah.id ? "bold" : "normal",
              }}
            >
              <span className="text-sm ltr" style={{ color: "var(--claude-text-subtle)" }}>
                {surah.id}
              </span>
              <div className="text-right">
                <div className="font-bold">{surah.nameAr}</div>
                <div className="text-xs" style={{ color: "var(--claude-text-muted)" }}>
                  {surah.ayahCount} آية
                </div>
              </div>
            </button>
          ))}
        </div>
      </aside>

      {/* Reader area */}
      <main
        className="flex-1 rounded-xl overflow-hidden"
        style={{ backgroundColor: "white", border: "1px solid var(--claude-border)", boxShadow: "0 2px 8px rgba(28,25,23,0.06)" }}
      >
        {/* Surah header */}
        <div
          className="p-6 text-center"
          style={{ backgroundColor: "var(--claude-dark)", borderBottom: "1px solid var(--claude-dark-3)" }}
        >
          <h2 className="text-3xl font-bold text-white mb-1">{selectedSurah.nameAr}</h2>
          <p className="text-sm" style={{ color: "var(--claude-text-subtle)" }}>
            {selectedSurah.ayahCount} آية
          </p>
          <div className="flex items-center justify-center gap-3 mt-4">
            <button
              onClick={() => setFontSize((f) => Math.min(f + 0.2, 2.5))}
              className="px-4 py-1.5 rounded-lg text-sm font-medium transition-colors text-white"
              style={{ backgroundColor: "var(--claude-accent)" }}
            >
              أ+
            </button>
            <span className="text-sm" style={{ color: "var(--claude-text-subtle)" }}>
              حجم الخط
            </span>
            <button
              onClick={() => setFontSize((f) => Math.max(f - 0.2, 1))}
              className="px-4 py-1.5 rounded-lg text-sm font-medium transition-colors text-white"
              style={{ backgroundColor: "var(--claude-dark-3)" }}
            >
              أ-
            </button>
          </div>
        </div>

        {/* Bismillah */}
        {selectedSurah.id !== 9 && (
          <div className="text-center py-6 border-b" style={{ borderColor: "var(--claude-gold-border)" }}>
            <p className="quran-font" style={{ color: "var(--claude-gold)", fontSize: `${fontSize}rem` }}>
              بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ
            </p>
          </div>
        )}

        {/* Ayahs */}
        <div className="p-6">
          {loading ? (
            <div className="flex items-center justify-center py-16">
              <div
                className="animate-spin w-12 h-12 border-4 border-t-transparent rounded-full"
                style={{ borderColor: "var(--claude-accent)", borderTopColor: "transparent" }}
              />
            </div>
          ) : ayahs.length > 0 ? (
            <div className="space-y-4">
              {ayahs.map((ayah) => (
                <div key={ayah.ayah_number} className="ayah-card">
                  <p className="quran-font mb-3" style={{ fontSize: `${fontSize}rem`, color: "var(--claude-text)" }}>
                    {ayah.text_uthmani}
                    <span className="text-base mr-2" style={{ color: "var(--claude-gold)" }}>
                      ﴿{ayah.ayah_number}﴾
                    </span>
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-16" style={{ color: "var(--claude-text-muted)" }}>
              <p className="text-2xl mb-3">📖</p>
              <p>اختر سورة من القائمة لعرض آياتها</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
