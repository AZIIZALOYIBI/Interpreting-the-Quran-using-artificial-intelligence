"use client";

import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface SearchBarProps {
  onSearch: (query: string) => void;
  loading?: boolean;
  placeholder?: string;
}

export default function SearchBar({ onSearch, loading = false, placeholder = "ابحث في آيات القرآن الكريم..." }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [focused, setFocused] = useState(false);

  const suggestions = ["الصبر", "الرحمة", "التوبة", "العدل", "العلم", "الصلاة", "الزكاة", "الجنة", "التقوى", "الشكر"];

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) onSearch(query.trim());
  }, [query, onSearch]);

  return (
    <div className="relative">
      <form onSubmit={handleSubmit}>
        <div className={`relative flex items-center transition-all duration-300 ${focused ? "scale-[1.02]" : ""}`}>
          <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} onFocus={() => setFocused(true)} onBlur={() => setTimeout(() => setFocused(false), 200)} placeholder={placeholder}
            className={`w-full px-6 py-4 bg-white/5 border rounded-xl text-white placeholder-gray-500 focus:outline-none text-lg font-display transition-all pr-14 ${focused ? "border-quran-gold/50 ring-2 ring-quran-gold/20" : "border-white/10"}`} />
          <button type="submit" disabled={loading || !query.trim()} className="absolute left-2 p-2 rounded-lg bg-quran-gold/20 text-quran-gold hover:bg-quran-gold/30 transition-colors disabled:opacity-50">
            {loading ? (
              <svg className="w-6 h-6 animate-spin" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            )}
          </button>
          <span className="absolute right-4 text-xl">🔍</span>
        </div>
      </form>
      <AnimatePresence>
        {focused && !query && (
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="absolute top-full right-0 left-0 mt-2 p-4 glass-dark rounded-xl border border-white/10 z-50">
            <p className="text-xs text-gray-500 mb-3 font-display">كلمات مقترحة للبحث:</p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((s) => (
                <button key={s} onClick={() => { setQuery(s); onSearch(s); }} className="px-3 py-1.5 rounded-full text-sm glass text-gray-300 hover:text-quran-gold hover:border-quran-gold/20 border border-white/5 transition-all font-display">{s}</button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
