"use client";

import { motion } from "framer-motion";
import { AskQuranResponse } from "@/types";

interface ResponseCardProps {
  response: AskQuranResponse;
  question: string;
}

export default function ResponseCard({ response, question }: ResponseCardProps) {
  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="glass rounded-2xl p-8 border border-quran-gold/20">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center text-lg">🤖</div>
          <div>
            <h3 className="text-lg font-bold font-display text-white">الإرشاد القرآني</h3>
            <p className="text-xs text-gray-400">بناءً على سؤالك: {question}</p>
          </div>
        </div>
        <p className="text-gray-200 leading-relaxed font-display text-base whitespace-pre-wrap">{response.answer}</p>
        <div className="mt-6 flex items-center gap-2">
          <span className="text-xs text-gray-500">الفئة:</span>
          <span className="px-3 py-1 rounded-full text-xs font-medium bg-quran-gold/10 text-quran-gold border border-quran-gold/20">{response.category}</span>
        </div>
      </motion.div>

      {response.ayahs.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="space-y-4">
          <h3 className="text-lg font-bold font-display text-quran-gold flex items-center gap-2">
            <span>📖</span><span>الآيات القرآنية ذات الصلة</span>
            <span className="text-sm text-gray-500 font-normal">({response.ayahs.length} آيات)</span>
          </h3>
          <div className="space-y-4">
            {response.ayahs.map((ayah, i) => (
              <motion.div key={i} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }}
                className="glass rounded-xl p-6 border border-white/5 hover:border-quran-gold/20 transition-all">
                <div className="flex items-center gap-3 mb-4">
                  <span className="verse-number">{ayah.ayah_number}</span>
                  <span className="text-sm font-bold font-display text-quran-gold">{ayah.surah_name_ar ?? ayah.surah_name}</span>
                </div>
                <p className="quran-text text-xl sm:text-2xl text-white leading-loose text-center py-4">{ayah.text_uthmani || ayah.text_simple}</p>
                {ayah.tafsir && (
                  <div className="pt-4 border-t border-white/5">
                    <p className="text-sm text-gray-400 leading-relaxed font-display">{ayah.tafsir}</p>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {response.practical_steps && response.practical_steps.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="glass rounded-2xl p-6 border border-white/5">
          <h3 className="text-lg font-bold font-display text-white mb-4 flex items-center gap-2"><span>✅</span><span>خطوات عملية</span></h3>
          <div className="space-y-3">
            {response.practical_steps.map((step, i) => (
              <div key={i} className="flex gap-3 p-3 rounded-lg bg-white/5">
                <span className="text-quran-gold mt-1">◆</span>
                <p className="text-gray-300 text-sm leading-relaxed font-display">{step}</p>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.6 }} className="p-4 rounded-xl bg-yellow-500/5 border border-yellow-500/10">
        <p className="text-xs text-yellow-400/70 text-center font-display">⚠️ {response.disclaimer || "هذا الإرشاد للتوجيه العام فقط. يُرجى استشارة العلماء المؤهلين في المسائل الشرعية الدقيقة."}</p>
      </motion.div>
    </div>
  );
}

