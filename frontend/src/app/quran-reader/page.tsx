"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import LoadingSpinner from "@/components/LoadingSpinner";
import { getSurahVerses } from "@/lib/api";
import { Surah, QuranVerse } from "@/types";

const defaultSurahs: Surah[] = [
  { number: 1, name: "الفاتحة", name_en: "Al-Fatiha", name_translation: "الفاتحة", revelation_type: "مكية", ayah_count: 7 },
  { number: 2, name: "البقرة", name_en: "Al-Baqarah", name_translation: "البقرة", revelation_type: "مدنية", ayah_count: 286 },
  { number: 3, name: "آل عمران", name_en: "Aal-E-Imran", name_translation: "آل عمران", revelation_type: "مدنية", ayah_count: 200 },
  { number: 36, name: "يس", name_en: "Ya-Sin", name_translation: "يس", revelation_type: "مكية", ayah_count: 83 },
  { number: 55, name: "الرحمن", name_en: "Ar-Rahman", name_translation: "الرحمن", revelation_type: "مدنية", ayah_count: 78 },
  { number: 67, name: "الملك", name_en: "Al-Mulk", name_translation: "الملك", revelation_type: "مكية", ayah_count: 30 },
  { number: 112, name: "الإخلاص", name_en: "Al-Ikhlas", name_translation: "الإخلاص", revelation_type: "مكية", ayah_count: 4 },
  { number: 113, name: "الفلق", name_en: "Al-Falaq", name_translation: "الفلق", revelation_type: "مكية", ayah_count: 5 },
  { number: 114, name: "الناس", name_en: "An-Nas", name_translation: "الناس", revelation_type: "مكية", ayah_count: 6 },
];

const sampleVerses: Record<number, QuranVerse[]> = {
  1: [
    { id: 1, surah_number: 1, surah_name: "الفاتحة", surah_name_en: "Al-Fatiha", ayah_number: 1, text_uthmani: "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", text_simple: "بسم الله الرحمن الرحيم", juz_number: 1, hizb_number: 1, page_number: 1 },
    { id: 2, surah_number: 1, surah_name: "الفاتحة", surah_name_en: "Al-Fatiha", ayah_number: 2, text_uthmani: "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", text_simple: "الحمد لله رب العالمين", juz_number: 1, hizb_number: 1, page_number: 1 },
    { id: 3, surah_number: 1, surah_name: "الفاتحة", surah_name_en: "Al-Fatiha", ayah_number: 3, text_uthmani: "الرَّحْمَٰنِ الرَّحِيمِ", text_simple: "الرحمن الرحيم", juz_number: 1, hizb_number: 1, page_number: 1 },
    { id: 4, surah_number: 1, surah_name: "الفاتحة", surah_name_en: "Al-Fatiha", ayah_number: 4, text_uthmani: "مَالِكِ يَوْمِ الدِّينِ", text_simple: "مالك يوم الدين", juz_number: 1, hizb_number: 1, page_number: 1 },
    { id: 5, surah_number: 1, surah_name: "الفاتحة", surah_name_en: "Al-Fatiha", ayah_number: 5, text_uthmani: "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ", text_simple: "إياك نعبد وإياك نستعين", juz_number: 1, hizb_number: 1, page_number: 1 },
    { id: 6, surah_number: 1, surah_name: "الفاتحة", surah_name_en: "Al-Fatiha", ayah_number: 6, text_uthmani: "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ", text_simple: "اهدنا الصراط المستقيم", juz_number: 1, hizb_number: 1, page_number: 1 },
    { id: 7, surah_number: 1, surah_name: "الفاتحة", surah_name_en: "Al-Fatiha", ayah_number: 7, text_uthmani: "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ", text_simple: "صراط الذين أنعمت عليهم غير المغضوب عليهم ولا الضالين", juz_number: 1, hizb_number: 1, page_number: 1 },
  ],
  112: [
    { id: 21, surah_number: 112, surah_name: "الإخلاص", surah_name_en: "Al-Ikhlas", ayah_number: 1, text_uthmani: "قُلْ هُوَ اللَّهُ أَحَدٌ", text_simple: "قل هو الله أحد", juz_number: 30, hizb_number: 60, page_number: 604 },
    { id: 22, surah_number: 112, surah_name: "الإخلاص", surah_name_en: "Al-Ikhlas", ayah_number: 2, text_uthmani: "اللَّهُ الصَّمَدُ", text_simple: "الله الصمد", juz_number: 30, hizb_number: 60, page_number: 604 },
    { id: 23, surah_number: 112, surah_name: "الإخلاص", surah_name_en: "Al-Ikhlas", ayah_number: 3, text_uthmani: "لَمْ يَلِدْ وَلَمْ يُولَدْ", text_simple: "لم يلد ولم يولد", juz_number: 30, hizb_number: 60, page_number: 604 },
    { id: 24, surah_number: 112, surah_name: "الإخلاص", surah_name_en: "Al-Ikhlas", ayah_number: 4, text_uthmani: "وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ", text_simple: "ولم يكن له كفوا أحد", juz_number: 30, hizb_number: 60, page_number: 604 },
  ],
};

export default function QuranReaderPage() {
  const [surahs] = useState<Surah[]>(defaultSurahs);
  const [selectedSurah, setSelectedSurah] = useState<number>(1);
  const [verses, setVerses] = useState<QuranVerse[]>(sampleVerses[1] || []);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  const handleSurahSelect = async (surahNumber: number) => {
    setSelectedSurah(surahNumber); setLoading(true);
    try {
      const data = await getSurahVerses(surahNumber); setVerses(data);
    } catch {
      setVerses(sampleVerses[surahNumber] || []);
    } finally { setLoading(false); }
  };

  const filteredSurahs = surahs.filter((s) => s.name.includes(searchTerm) || s.name_en.toLowerCase().includes(searchTerm.toLowerCase()) || s.number.toString().includes(searchTerm));
  const currentSurah = surahs.find((s) => s.number === selectedSurah);

  return (
    <div className="min-h-screen pt-24 pb-16 px-4">
      <div className="max-w-7xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-10">
          <h1 className="text-3xl sm:text-4xl font-bold font-display gradient-text mb-4">📖 قارئ القرآن الكريم</h1>
          <p className="text-gray-400 font-display">تصفح القرآن الكريم بالخط العثماني مع تصميم طباعي جميل</p>
          <div className="mt-4 h-1 w-24 mx-auto bg-gradient-to-l from-quran-gold to-yellow-600 rounded-full" />
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <div className="lg:col-span-1">
            <div className="glass rounded-2xl border border-white/5 overflow-hidden sticky top-24">
              <div className="p-4 border-b border-white/5">
                <input type="text" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} placeholder="ابحث عن سورة..."
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-quran-gold/50 text-sm font-display" />
              </div>
              <div className="max-h-[60vh] overflow-y-auto">
                {filteredSurahs.map((surah) => (
                  <button key={surah.number} onClick={() => handleSurahSelect(surah.number)}
                    className={`w-full flex items-center gap-3 px-4 py-3 text-right transition-all ${selectedSurah === surah.number ? "bg-quran-gold/10 text-quran-gold border-r-2 border-quran-gold" : "text-gray-300 hover:bg-white/5 hover:text-white"}`}>
                    <span className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold ${selectedSurah === surah.number ? "bg-quran-gold/20 text-quran-gold" : "bg-white/5 text-gray-500"}`}>{surah.number}</span>
                    <div className="flex-1">
                      <div className="text-sm font-bold font-display">{surah.name}</div>
                      <div className="text-xs text-gray-500">{surah.name_en} • {surah.ayah_count} آية • {surah.revelation_type}</div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="lg:col-span-3">
            {currentSurah && (
              <motion.div key={selectedSurah} initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                <div className="surah-header text-center">
                  <h2 className="text-2xl font-bold quran-text gradient-text">سورة {currentSurah.name}</h2>
                  <p className="text-sm text-gray-400 mt-2 font-display">{currentSurah.name_en} • {currentSurah.ayah_count} آية • {currentSurah.revelation_type}</p>
                </div>
                {selectedSurah !== 9 && <div className="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>}
                {loading ? (
                  <div className="flex justify-center py-20"><LoadingSpinner size="lg" /></div>
                ) : (
                  <div className="glass rounded-2xl p-8 border border-white/5">
                    <div className="quran-text text-2xl leading-[3] text-center">
                      {verses.map((verse) => (
                        <span key={verse.id} className="inline">
                          <span className="text-white hover:text-quran-gold transition-colors cursor-pointer">{verse.text_uthmani || verse.text_simple}</span>
                          <span className="verse-number">{verse.ayah_number}</span>{" "}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
