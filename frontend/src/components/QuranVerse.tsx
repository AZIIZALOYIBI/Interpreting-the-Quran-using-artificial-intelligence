"use client";

import { motion } from "framer-motion";
import { QuranVerse as QuranVerseType } from "@/types";
import Link from "next/link";

interface QuranVerseProps {
  verse: QuranVerseType;
  index: number;
  showTafsirLink?: boolean;
}

export default function QuranVerse({ verse, index, showTafsirLink = true }: QuranVerseProps) {
  return (
    <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: index * 0.1 }}
      className="glass rounded-xl p-6 border border-white/5 hover:border-quran-gold/20 transition-all group">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="verse-number">{verse.ayah_number}</span>
          <div>
            <span className="text-sm font-bold font-display text-quran-gold">{verse.surah_name}</span>
            <span className="text-xs text-gray-500 mr-2">({verse.surah_name_en})</span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500">الجزء {verse.juz_number}</span>
          {showTafsirLink && (
            <Link href={`/tafsir?surah=${verse.surah_number}&ayah=${verse.ayah_number}`} className="text-xs text-quran-gold/60 hover:text-quran-gold transition-colors opacity-0 group-hover:opacity-100">التفسير ←</Link>
          )}
        </div>
      </div>
      <p className="quran-text text-xl sm:text-2xl text-white leading-loose mb-4 text-center py-4">{verse.text_uthmani || verse.text_simple}</p>
      {verse.translation && (
        <div className="pt-4 border-t border-white/5">
          <p className="text-sm text-gray-400 leading-relaxed font-display">{verse.translation}</p>
        </div>
      )}
    </motion.div>
  );
}
