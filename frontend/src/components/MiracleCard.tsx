"use client";

import { motion } from "framer-motion";
import { ScientificMiracle } from "@/types";

interface MiracleCardProps {
  miracle: ScientificMiracle;
  index: number;
}

export default function MiracleCard({ miracle, index }: MiracleCardProps) {
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.1 }} viewport={{ once: true }} className="glass rounded-2xl overflow-hidden border border-white/5 card-hover group">
      <div className="p-6 bg-gradient-to-l from-quran-gold/10 to-transparent border-b border-white/5">
        <div className="flex items-start justify-between">
          <div>
            <span className="text-xs text-quran-gold/60 font-display">{miracle.category}</span>
            <h3 className="text-lg font-bold font-display text-white mt-1">{miracle.title}</h3>
          </div>
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center text-2xl">🔬</div>
        </div>
      </div>
      <div className="p-6 space-y-4">
        <div className="p-4 rounded-xl bg-quran-gold/5 border border-quran-gold/10">
          <p className="quran-text text-lg text-quran-gold text-center leading-loose mb-2">{miracle.verse_text}</p>
          <p className="text-xs text-gray-400 text-center font-display">{miracle.quran_reference}</p>
        </div>
        <div>
          <h4 className="text-sm font-bold font-display text-green-400 mb-2 flex items-center gap-2"><span>🧪</span> الحقيقة العلمية</h4>
          <p className="text-sm text-gray-300 leading-relaxed font-display">{miracle.scientific_fact}</p>
        </div>
        <p className="text-sm text-gray-400 leading-relaxed font-display">{miracle.description}</p>
        {miracle.discovery_year && (
          <div className="flex items-center gap-2 text-xs text-gray-500"><span>📅</span><span>تاريخ الاكتشاف العلمي: {miracle.discovery_year}</span></div>
        )}
      </div>
    </motion.div>
  );
}
