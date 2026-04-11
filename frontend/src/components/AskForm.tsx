"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { askQuran } from "@/lib/api";
import { AskQuranResponse } from "@/types";
import ResponseCard from "./ResponseCard";
import LoadingSpinner from "./LoadingSpinner";
import toast from "react-hot-toast";

const categories = [
  { id: "general", name: "عام", icon: "🌐" },
  { id: "medicine", name: "الطب والصحة", icon: "🏥" },
  { id: "business", name: "العمل والتجارة", icon: "💼" },
  { id: "science", name: "العلوم", icon: "🔬" },
  { id: "family", name: "الأسرة", icon: "👨‍👩‍👧‍👦" },
  { id: "self-development", name: "تطوير الذات", icon: "🌱" },
  { id: "law", name: "القانون والعدل", icon: "⚖️" },
  { id: "environment", name: "البيئة", icon: "🌍" },
];

const sampleQuestions = [
  "كيف يرشدنا القرآن في موضوع الصحة النفسية؟",
  "ما هي الإرشادات القرآنية للنجاح في العمل؟",
  "كيف يوجهنا القرآن في التعامل مع الأسرة؟",
  "ما الآيات المتعلقة بالصبر والمحن؟",
  "ماذا يقول القرآن عن العدل والمساواة؟",
  "كيف نتعامل مع القلق والتوتر قرآنياً؟",
];

export default function AskForm() {
  const [question, setQuestion] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("general");
  const [response, setResponse] = useState<AskQuranResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<{ question: string; response: AskQuranResponse }[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) { toast.error("الرجاء كتابة سؤالك"); return; }
    setLoading(true);
    try {
      const result = await askQuran({ question: question.trim(), category: selectedCategory });
      setResponse(result);
      setHistory((prev) => [{ question: question.trim(), response: result }, ...prev]);
    } catch (error) {
      toast.error("حدث خطأ أثناء معالجة سؤالك. يرجى المحاولة مرة أخرى.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-3 font-display">اختر الفئة</label>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {categories.map((cat) => (
              <button key={cat.id} type="button" onClick={() => setSelectedCategory(cat.id)}
                className={`p-3 rounded-xl text-sm font-display font-medium transition-all flex items-center gap-2 justify-center ${selectedCategory === cat.id ? "bg-quran-gold/20 text-quran-gold border border-quran-gold/30 glow-gold" : "glass border border-white/5 text-gray-400 hover:text-white hover:border-white/10"}`}>
                <span>{cat.icon}</span><span>{cat.name}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="relative">
          <label className="block text-sm font-medium text-gray-300 mb-3 font-display">اكتب سؤالك</label>
          <div className="relative">
            <textarea value={question} onChange={(e) => setQuestion(e.target.value)}
              placeholder="مثال: كيف يرشدنا القرآن في موضوع الصحة النفسية والسعادة؟"
              rows={4}
              className="w-full px-6 py-4 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-quran-gold/50 focus:ring-2 focus:ring-quran-gold/20 resize-none font-display text-lg transition-all" />
            <div className="absolute bottom-3 left-3 text-xs text-gray-500">{question.length}/500</div>
          </div>
        </div>

        <div>
          <p className="text-xs text-gray-500 mb-2 font-display">أسئلة مقترحة:</p>
          <div className="flex flex-wrap gap-2">
            {sampleQuestions.map((sq, i) => (
              <button key={i} type="button" onClick={() => setQuestion(sq)}
                className="px-3 py-1.5 text-xs glass rounded-full text-gray-400 hover:text-quran-gold hover:border-quran-gold/20 border border-white/5 transition-all font-display">
                {sq}
              </button>
            ))}
          </div>
        </div>

        <button type="submit" disabled={loading || !question.trim()}
          className="w-full py-4 bg-gradient-to-l from-quran-gold to-yellow-600 text-quran-dark font-bold rounded-xl text-lg font-display shadow-lg shadow-quran-gold/20 hover:shadow-quran-gold/40 transition-all hover:scale-[1.02] disabled:opacity-50 disabled:hover:scale-100 disabled:cursor-not-allowed flex items-center justify-center gap-3">
          {loading ? (<><LoadingSpinner size="sm" /><span>جاري البحث في القرآن الكريم...</span></>) : (<><span>🔍</span><span>ابحث عن الإرشاد القرآني</span></>)}
        </button>
      </form>

      <AnimatePresence mode="wait">
        {loading && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex flex-col items-center justify-center py-16 space-y-4">
            <LoadingSpinner size="lg" />
            <p className="text-gray-400 font-display animate-pulse">جاري البحث في آيات القرآن الكريم<span className="loading-dots"></span></p>
          </motion.div>
        )}
        {!loading && response && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
            <ResponseCard response={response} question={question} />
          </motion.div>
        )}
      </AnimatePresence>

      {history.length > 1 && (
        <div className="space-y-4">
          <h3 className="text-lg font-bold font-display text-gray-300">سجل الأسئلة السابقة</h3>
          <div className="space-y-3">
            {history.slice(1).map((item, i) => (
              <button key={i} onClick={() => { setQuestion(item.question); setResponse(item.response); }}
                className="w-full text-right p-4 glass rounded-xl border border-white/5 hover:border-quran-gold/20 transition-all">
                <p className="text-sm text-gray-300 font-display">{item.question}</p>
                <p className="text-xs text-gray-500 mt-1">{item.response.verses.length} آيات ذات صلة</p>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
