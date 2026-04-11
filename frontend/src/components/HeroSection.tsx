"use client";

import { motion } from "framer-motion";
import Link from "next/link";

export default function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0 animated-bg" />
      <div className="absolute top-20 right-20 w-72 h-72 bg-quran-gold/5 rounded-full blur-3xl animate-float" />
      <div className="absolute bottom-20 left-20 w-96 h-96 bg-green-500/5 rounded-full blur-3xl animate-float" style={{ animationDelay: "3s" }} />

      <div className="relative z-10 max-w-5xl mx-auto px-4 text-center">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-quran-gold/20 mb-8">
          <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          <span className="text-sm text-gray-300 font-display">مدعوم بالذكاء الاصطناعي</span>
        </motion.div>

        <motion.h1 initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="text-4xl sm:text-5xl md:text-7xl font-bold font-display mb-6 leading-tight">
          <span className="gradient-text">حلول الحياة</span><br />
          <span className="text-white">من القرآن الكريم</span>
        </motion.h1>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }} className="mb-8">
          <p className="text-xl sm:text-2xl quran-text text-quran-gold/80 mb-3">﴿ وَنُنَزِّلُ مِنَ الْقُرْآنِ مَا هُوَ شِفَاءٌ وَرَحْمَةٌ لِّلْمُؤْمِنِينَ ﴾</p>
          <p className="text-sm text-gray-400 font-display">سورة الإسراء - الآية 82</p>
        </motion.div>

        <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.8 }} className="text-lg sm:text-xl text-gray-300 max-w-3xl mx-auto mb-12 leading-relaxed font-display">
          منصة ذكية تساعدك في العثور على إرشادات قرآنية لأي موضوع في حياتك، باستخدام تقنيات الذكاء الاصطناعي ومعالجة اللغة الطبيعية
        </motion.p>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 1 }} className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link href="/ask" className="px-8 py-4 bg-gradient-to-l from-quran-gold to-yellow-600 text-quran-dark font-bold rounded-xl text-lg font-display shadow-lg shadow-quran-gold/20 hover:shadow-quran-gold/40 transition-all hover:scale-105 flex items-center gap-2">
            🤖 اسأل القرآن الآن
          </Link>
          <Link href="/quran-reader" className="px-8 py-4 glass border border-quran-gold/20 text-quran-gold font-bold rounded-xl text-lg font-display hover:bg-quran-gold/10 transition-all hover:scale-105">
            📖 تصفح القرآن الكريم
          </Link>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 1.2 }} className="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-6">
          {[{ number: "6,236", label: "آية قرآنية", icon: "📖" }, { number: "114", label: "سورة", icon: "📜" }, { number: "8", label: "فئات حياتية", icon: "🗂️" }, { number: "∞", label: "إرشاد إلهي", icon: "✨" }].map((stat, i) => (
            <div key={i} className="glass rounded-xl p-4 border border-white/5 hover:border-quran-gold/20 transition-all">
              <div className="text-2xl mb-2">{stat.icon}</div>
              <div className="text-2xl font-bold gradient-text font-display">{stat.number}</div>
              <div className="text-sm text-gray-400">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-quran-dark to-transparent" />
    </section>
  );
}
