"use client";

import { motion } from "framer-motion";
import { AskQuranResponse } from "@/types";
import QuranVerse from "./QuranVerse";

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
          <div className="mr-auto">
            <div className="px-3 py-1 rounded-full text-xs font-medium bg-green-500/10 text-green-400 border border-green-500/20">دقة {Math.round(response.confidence * 100)}%</div>
          </div>
        </div>
        <p className="text-gray-200 leading-relaxed font-display text-base whitespace-pre-wrap">{response.answer}</p>
        <div className="mt-6 flex items-center gap-2">
          <span className="text-xs text-gray-500">الفئة:</span>
          <span className="px-3 py-1 rounded-full text-xs font-medium bg-quran-gold/10 text-quran-gold border border-quran-gold/20">{response.category}</span>
        </div>
      </motion.div>

      {response.verses.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="space-y-4">
          <h3 className="text-lg font-bold font-display text-quran-gold flex items-center gap-2">
            <span>📖</span><span>الآيات القرآنية ذات الصلة</span>
            <span className="text-sm text-gray-500 font-normal">({response.verses.length} آيات)</span>
          </h3>
          <div className="space-y-4">{response.verses.map((verse, i) => (<QuranVerse key={i} verse={verse} index={i} />))}</div>
        </motion.div>
      )}

      {response.tafsir_notes && response.tafsir_notes.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="glass rounded-2xl p-6 border border-white/5">
          <h3 className="text-lg font-bold font-display text-white mb-4 flex items-center gap-2"><span>📝</span><span>ملاحظات تفسيرية</span></h3>
          <div className="space-y-3">
            {response.tafsir_notes.map((note, i) => (
              <div key={i} className="flex gap-3 p-3 rounded-lg bg-white/5">
                <span className="text-quran-gold mt-1">◆</span>
                <p className="text-gray-300 text-sm leading-relaxed font-display">{note}</p>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {response.related_topics && response.related_topics.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }}>
          <h4 className="text-sm font-display text-gray-400 mb-3">مواضيع ذات صلة:</h4>
          <div className="flex flex-wrap gap-2">
            {response.related_topics.map((topic, i) => (
              <span key={i} className="px-4 py-2 glass rounded-full text-sm text-gray-300 border border-white/5 hover:border-quran-gold/20 hover:text-quran-gold transition-all cursor-pointer font-display">{topic}</span>
            ))}
          </div>
        </motion.div>
      )}

      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.8 }} className="p-4 rounded-xl bg-yellow-500/5 border border-yellow-500/10">
        <p className="text-xs text-yellow-400/70 text-center font-display">⚠️ هذا الإرشاد مبني على تحليل الذكاء الاصطناعي للنصوص القرآنية وهو للتوجيه العام فقط. يُرجى استشارة العلماء المؤهلين في المسائل الشرعية الدقيقة.</p>
      </motion.div>
    </div>
  );
}
