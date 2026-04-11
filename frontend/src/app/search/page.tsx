"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import SearchBar from "@/components/SearchBar";
import QuranVerse from "@/components/QuranVerse";
import LoadingSpinner from "@/components/LoadingSpinner";
import { searchVerses } from "@/lib/api";
import { QuranVerse as QuranVerseType } from "@/types";
import toast from "react-hot-toast";

const demoResults: QuranVerseType[] = [
  { id: 153, surah_number: 2, surah_name: "البقرة", surah_name_en: "Al-Baqarah", ayah_number: 153, text_uthmani: "يَا أَيُّهَا الَّذِينَ آمَنُوا اسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ ۚ إِنَّ اللَّهَ مَعَ الصَّابِرِينَ", text_simple: "يا أيها الذين آمنوا استعينوا بالصبر والصلاة إن الله مع الصابرين", translation: "يا أيها الذين آمنوا، استعينوا على أموركم بالصبر والصلاة، فإن الله مع الصابرين بتأييده ونصره", juz_number: 2, hizb_number: 3, page_number: 23 },
  { id: 286, surah_number: 2, surah_name: "البقرة", surah_name_en: "Al-Baqarah", ayah_number: 286, text_uthmani: "لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا ۚ لَهَا مَا كَسَبَتْ وَعَلَيْهَا مَا اكْتَسَبَتْ", text_simple: "لا يكلف الله نفسا إلا وسعها لها ما كسبت وعليها ما اكتسبت", translation: "لا يكلف الله نفساً فوق طاقتها، لها ثواب ما عملت من خير، وعليها عقاب ما ارتكبت من ذنب", juz_number: 3, hizb_number: 5, page_number: 49 },
  { id: 200, surah_number: 3, surah_name: "آل عمران", surah_name_en: "Aal-E-Imran", ayah_number: 200, text_uthmani: "يَا أَيُّهَا الَّذِينَ آمَنُوا اصْبِرُوا وَصَابِرُوا وَرَابِطُوا وَاتَّقُوا اللَّهَ لَعَلَّكُمْ تُفْلِحُونَ", text_simple: "يا أيها الذين آمنوا اصبروا وصابروا ورابطوا واتقوا الله لعلكم تفلحون", translation: "يا أيها الذين آمنوا اصبروا على طاعة الله وصابروا أعداءكم وكونوا على استعداد دائم واتقوا الله لعلكم تفلحون", juz_number: 4, hizb_number: 8, page_number: 76 },
];

export default function SearchPage() {
  const [results, setResults] = useState<QuranVerseType[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [totalCount, setTotalCount] = useState(0);
  const [currentQuery, setCurrentQuery] = useState("");

  const handleSearch = async (query: string) => {
    setLoading(true); setSearched(true); setCurrentQuery(query);
    try {
      const data = await searchVerses(query);
      setResults(data.verses); setTotalCount(data.total_count);
    } catch {
      const filtered = demoResults.filter((v) => v.text_simple.includes(query) || v.text_uthmani.includes(query) || (v.translation && v.translation.includes(query)));
      setResults(filtered.length > 0 ? filtered : demoResults);
      setTotalCount(filtered.length > 0 ? filtered.length : demoResults.length);
      toast("يتم عرض نتائج تجريبية - الخادم غير متصل", { icon: "ℹ️" });
    } finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-10">
          <h1 className="text-3xl sm:text-4xl font-bold font-display gradient-text mb-4">🔍 البحث في القرآن الكريم</h1>
          <p className="text-gray-400 font-display">ابحث في آيات القرآن الكريم باستخدام الكلمات المفتاحية</p>
          <div className="mt-4 h-1 w-24 mx-auto bg-gradient-to-l from-quran-gold to-yellow-600 rounded-full" />
        </motion.div>
        <div className="mb-8"><SearchBar onSearch={handleSearch} loading={loading} /></div>
        <AnimatePresence mode="wait">
          {loading && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex flex-col items-center py-20 space-y-4">
              <LoadingSpinner size="lg" />
              <p className="text-gray-400 font-display">جاري البحث<span className="loading-dots"></span></p>
            </motion.div>
          )}
          {!loading && searched && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
              <p className="text-sm text-gray-400 font-display">تم العثور على <span className="text-quran-gold font-bold">{totalCount}</span> نتيجة لـ &quot;{currentQuery}&quot;</p>
              {results.length > 0 ? (
                <div className="space-y-4">{results.map((verse, i) => (<QuranVerse key={verse.id} verse={verse} index={i} />))}</div>
              ) : (
                <div className="text-center py-20"><p className="text-4xl mb-4">🔍</p><p className="text-gray-400 font-display">لم يتم العثور على نتائج. حاول استخدام كلمات مختلفة.</p></div>
              )}
            </motion.div>
          )}
          {!loading && !searched && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center py-20">
              <p className="text-6xl mb-6">📖</p>
              <p className="text-xl text-gray-400 font-display mb-2">ابدأ البحث في القرآن الكريم</p>
              <p className="text-sm text-gray-500 font-display">اكتب كلمة أو عبارة للبحث عنها في الآيات القرآنية</p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
