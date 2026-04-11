"use client";

import { Suspense } from "react";
import { motion } from "framer-motion";
import AskForm from "@/components/AskForm";
import LoadingSpinner from "@/components/LoadingSpinner";

export default function AskPage() {
  return (
    <div className="min-h-screen pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-quran-gold/20 mb-6">
            <span className="text-lg">🤖</span>
            <span className="text-sm text-gray-300 font-display">مدعوم بالذكاء الاصطناعي</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold font-display gradient-text mb-4">اسأل القرآن الكريم</h1>
          <p className="text-gray-400 max-w-2xl mx-auto font-display">اطرح أي سؤال عن الحياة واحصل على إرشاد قرآني مخصص مع الآيات ذات الصلة والتفاسير</p>
          <div className="mt-4 h-1 w-24 mx-auto bg-gradient-to-l from-quran-gold to-yellow-600 rounded-full" />
        </motion.div>
        <Suspense fallback={<div className="flex justify-center py-20"><LoadingSpinner size="lg" /></div>}>
          <AskForm />
        </Suspense>
      </div>
    </div>
  );
}
