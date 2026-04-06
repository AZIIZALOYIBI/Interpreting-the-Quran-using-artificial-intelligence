"use client";
import { useState, useCallback } from "react";
import type { Ayah, SurahInfo } from "@/types";

const SURAHS: SurahInfo[] = [
  { id: 1, nameAr: "الفاتحة", nameEn: "Al-Fatihah", ayahCount: 7, revelationType: "meccan" },
  { id: 2, nameAr: "البقرة", nameEn: "Al-Baqarah", ayahCount: 286, revelationType: "medinan" },
  { id: 3, nameAr: "آل عمران", nameEn: "Ali 'Imran", ayahCount: 200, revelationType: "medinan" },
  { id: 18, nameAr: "الكهف", nameEn: "Al-Kahf", ayahCount: 110, revelationType: "meccan" },
  { id: 36, nameAr: "يس", nameEn: "Ya-Sin", ayahCount: 83, revelationType: "meccan" },
  { id: 55, nameAr: "الرحمن", nameEn: "Ar-Rahman", ayahCount: 78, revelationType: "medinan" },
  { id: 67, nameAr: "الملك", nameEn: "Al-Mulk", ayahCount: 30, revelationType: "meccan" },
  { id: 112, nameAr: "الإخلاص", nameEn: "Al-Ikhlas", ayahCount: 4, revelationType: "meccan" },
  { id: 113, nameAr: "الفلق", nameEn: "Al-Falaq", ayahCount: 5, revelationType: "meccan" },
  { id: 114, nameAr: "الناس", nameEn: "An-Nas", ayahCount: 6, revelationType: "meccan" },
];

const SAMPLE_AYAHS: Record<number, Ayah[]> = {
  1: [
    { id: 1, surahId: 1, surahName: "Al-Fatihah", surahNameAr: "الفاتحة", ayahNumber: 1, textUthmani: "بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ", textSimple: "بسم الله الرحمن الرحيم" },
    { id: 2, surahId: 1, surahName: "Al-Fatihah", surahNameAr: "الفاتحة", ayahNumber: 2, textUthmani: "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", textSimple: "الحمد لله رب العالمين" },
    { id: 3, surahId: 1, surahName: "Al-Fatihah", surahNameAr: "الفاتحة", ayahNumber: 3, textUthmani: "الرَّحْمَـٰنِ الرَّحِيمِ", textSimple: "الرحمن الرحيم" },
    { id: 4, surahId: 1, surahName: "Al-Fatihah", surahNameAr: "الفاتحة", ayahNumber: 4, textUthmani: "مَالِكِ يَوْمِ الدِّينِ", textSimple: "مالك يوم الدين" },
    { id: 5, surahId: 1, surahName: "Al-Fatihah", surahNameAr: "الفاتحة", ayahNumber: 5, textUthmani: "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ", textSimple: "إياك نعبد وإياك نستعين" },
    { id: 6, surahId: 1, surahName: "Al-Fatihah", surahNameAr: "الفاتحة", ayahNumber: 6, textUthmani: "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ", textSimple: "اهدنا الصراط المستقيم" },
    { id: 7, surahId: 1, surahName: "Al-Fatihah", surahNameAr: "الفاتحة", ayahNumber: 7, textUthmani: "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ", textSimple: "صراط الذين أنعمت عليهم غير المغضوب عليهم ولا الضالين" },
  ],
};

export default function QuranReader() {
  const [selectedSurah, setSelectedSurah] = useState<SurahInfo>(SURAHS[0]);
  const [ayahs, setAyahs] = useState<Ayah[]>(SAMPLE_AYAHS[1] || []);
  const [loading, setLoading] = useState(false);
  const [fontSize, setFontSize] = useState(1.5);

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
      <aside className="lg:w-72 bg-white rounded-xl shadow-md overflow-hidden flex-shrink-0">
        <div className="bg-emerald-800 text-white p-4">
          <h2 className="font-bold text-lg">فهرس السور</h2>
        </div>
        <div className="overflow-y-auto max-h-[calc(100vh-200px)]">
          {SURAHS.map((surah) => (
            <button
              key={surah.id}
              onClick={() => loadSurah(surah)}
              className={`w-full text-right px-4 py-3 flex items-center justify-between hover:bg-emerald-50 transition-colors border-b border-gray-100 ${
                selectedSurah.id === surah.id ? "bg-emerald-100 text-emerald-800 font-bold" : "text-gray-700"
              }`}
            >
              <span className="text-gray-400 text-sm ltr">{surah.id}</span>
              <div className="text-right">
                <div className="font-bold">{surah.nameAr}</div>
                <div className="text-xs text-gray-500">{surah.ayahCount} آية</div>
              </div>
            </button>
          ))}
        </div>
      </aside>

      {/* Reader area */}
      <main className="flex-1 bg-white rounded-xl shadow-md overflow-hidden">
        {/* Surah header */}
        <div className="bg-emerald-800 text-white p-6 text-center">
          <h2 className="text-3xl font-bold mb-1">{selectedSurah.nameAr}</h2>
          <p className="text-emerald-200 text-sm">{selectedSurah.ayahCount} آية</p>
          <div className="flex items-center justify-center gap-4 mt-4">
            <button
              onClick={() => setFontSize((f) => Math.min(f + 0.2, 2.5))}
              className="bg-emerald-700 hover:bg-emerald-600 px-3 py-1 rounded text-sm"
            >
              أ+
            </button>
            <button
              onClick={() => setFontSize((f) => Math.max(f - 0.2, 1))}
              className="bg-emerald-700 hover:bg-emerald-600 px-3 py-1 rounded text-sm"
            >
              أ-
            </button>
          </div>
        </div>

        {/* Bismillah */}
        {selectedSurah.id !== 9 && (
          <div className="text-center py-6 border-b border-amber-100">
            <p className="quran-font text-emerald-800" style={{ fontSize: `${fontSize}rem` }}>
              بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ
            </p>
          </div>
        )}

        {/* Ayahs */}
        <div className="p-6">
          {loading ? (
            <div className="flex items-center justify-center py-16">
              <div className="animate-spin w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full"></div>
            </div>
          ) : ayahs.length > 0 ? (
            <div className="space-y-4">
              {ayahs.map((ayah) => (
                <div key={ayah.ayahNumber} className="ayah-card">
                  <p
                    className="quran-font text-gray-800 mb-3"
                    style={{ fontSize: `${fontSize}rem` }}
                  >
                    {ayah.textUthmani}
                    <span className="text-amber-600 text-base mr-2">﴿{ayah.ayahNumber}﴾</span>
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-16 text-gray-500">
              <p className="text-xl mb-2">📖</p>
              <p>اختر سورة من القائمة لعرض آياتها</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
