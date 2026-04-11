"use client";

import { useState, Suspense } from "react";
import { motion } from "framer-motion";
import LoadingSpinner from "@/components/LoadingSpinner";
import { TafsirEntry } from "@/types";

const sampleTafsirs: TafsirEntry[] = [
  { id: 1, verse_id: 1, scholar_name: "ابن كثير", scholar_name_en: "Ibn Kathir", tafsir_text: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ: قال ابن كثير رحمه الله: الاستعاذة أمر بها الشرع عند ابتداء القراءة فيُستعاذ بالله من الشيطان الرجيم. والبسملة قد قيل إنها آية مستقلة من أول كل سورة.", source: "تفسير ابن كثير", era: "القرن الثامن الهجري" },
  { id: 2, verse_id: 1, scholar_name: "الطبري", scholar_name_en: "Al-Tabari", tafsir_text: "قال أبو جعفر الطبري: يعني تعالى ذكره بقوله: بسم الله، أي: بالله. والله أصله الإله، حذفت الهمزة التي هي فاء الاسم، ثم أُدغمت اللام في اللام فصارت: الله.", source: "جامع البيان عن تأويل آي القرآن", era: "القرن الثالث الهجري" },
  { id: 3, verse_id: 1, scholar_name: "القرطبي", scholar_name_en: "Al-Qurtubi", tafsir_text: "قال القرطبي: البسملة آية من كتاب الله بإجماع. واختلف العلماء هل هي آية من كل سورة أم من الفاتحة فقط.", source: "الجامع لأحكام القرآن", era: "القرن السابع الهجري" },
  { id: 4, verse_id: 2, scholar_name: "السعدي", scholar_name_en: "As-Sa'di", tafsir_text: "الحمد لله رب العالمين: الحمد هو الثناء على الله بصفات الكمال وبأفعاله الدائرة بين الفضل والعدل، فله الحمد الكامل بجميع الوجوه.", source: "تيسير الكريم الرحمن", era: "القرن الرابع عشر الهجري" },
];

export default function TafsirPage() {
  const [surahNumber, setSurahNumber] = useState(1);
  const [ayahNumber, setAyahNumber] = useState(1);
  const [tafsirs] = useState<TafsirEntry[]>(sampleTafsirs);
  const [loading] = useState(false);

  const filteredTafsirs = tafsirs.filter((t) => t.verse_id === ayahNumber);
  const displayTafsirs = filteredTafsirs.length > 0 ? filteredTafsirs : tafsirs;

  return (
    <div className="min-h-screen pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-10">
          <h1 className="text-3xl sm:text-4xl font-bold font-display gradient-text mb-4">📝 هيئة التفسير</h1>
          <p className="text-gray-400 font-display">تفسيرات متعددة من كبار العلماء لكل آية من القرآن الكريم</p>
          <div className="mt-4 h-1 w-24 mx-auto bg-gradient-to-l from-quran-gold to-yellow-600 rounded-full" />
        </motion.div>

        <div className="glass rounded-2xl p-6 border border-white/5 mb-8">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2 font-display">رقم السورة</label>
              <input type="number" min="1" max="114" value={surahNumber} onChange={(e) => setSurahNumber(Number(e.target.value))}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:border-quran-gold/50 font-display text-center text-lg" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2 font-display">رقم الآية</label>
              <input type="number" min="1" value={ayahNumber} onChange={(e) => setAyahNumber(Number(e.target.value))}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:border-quran-gold/50 font-display text-center text-lg" />
            </div>
          </div>
        </div>

        <Suspense fallback={<div className="flex justify-center py-20"><LoadingSpinner size="lg" /></div>}>
          {loading ? (
            <div className="flex justify-center py-20"><LoadingSpinner size="lg" /></div>
          ) : (
            <div className="space-y-6">
              {displayTafsirs.map((tafsir, i) => (
                <motion.div key={tafsir.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
                  className="glass rounded-2xl p-6 border border-white/5 card-hover">
                  <div className="flex items-center gap-4 mb-4 pb-4 border-b border-white/5">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-quran-gold/20 to-yellow-600/20 flex items-center justify-center text-xl">📚</div>
                    <div>
                      <h3 className="text-lg font-bold font-display text-quran-gold">{tafsir.scholar_name}</h3>
                      <p className="text-xs text-gray-500">{tafsir.source} • {tafsir.era}</p>
                    </div>
                  </div>
                  <p className="text-gray-300 leading-relaxed font-display text-base">{tafsir.tafsir_text}</p>
                </motion.div>
              ))}
            </div>
          )}
        </Suspense>
      </div>
    </div>
  );
}
