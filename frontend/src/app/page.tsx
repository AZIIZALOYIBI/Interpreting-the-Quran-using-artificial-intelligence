"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import HeroSection from "@/components/HeroSection";
import CategoryCard from "@/components/CategoryCard";
import { Category } from "@/types";

const defaultCategories: Category[] = [
  { id: "medicine", name: "الطب والصحة", name_en: "Medicine & Health", icon: "🏥", description: "اكتشف الإرشادات القرآنية المتعلقة بالصحة الجسدية والنفسية والغذاء والعلاج", color: "#22c55e", verse_count: 120 },
  { id: "business", name: "العمل والتجارة", name_en: "Business & Commerce", icon: "💼", description: "تعرف على مبادئ التجارة والعمل والمعاملات المالية في القرآن الكريم", color: "#3b82f6", verse_count: 95 },
  { id: "science", name: "العلوم والمعرفة", name_en: "Science & Knowledge", icon: "🔬", description: "اكتشف الآيات المتعلقة بالعلوم الطبيعية والكونية والمعجزات العلمية", color: "#8b5cf6", verse_count: 150 },
  { id: "family", name: "الأسرة والمجتمع", name_en: "Family & Society", icon: "👨‍👩‍👧‍👦", description: "إرشادات قرآنية حول بناء الأسرة والعلاقات الزوجية وتربية الأبناء", color: "#f59e0b", verse_count: 200 },
  { id: "self-development", name: "تطوير الذات", name_en: "Self Development", icon: "🌱", description: "آيات تساعدك في تطوير شخصيتك وتحقيق التوازن النفسي والروحي", color: "#10b981", verse_count: 180 },
  { id: "law", name: "القانون والعدل", name_en: "Law & Justice", icon: "⚖️", description: "مبادئ العدل والمساواة والحقوق والواجبات كما وردت في القرآن الكريم", color: "#ef4444", verse_count: 130 },
  { id: "environment", name: "البيئة والطبيعة", name_en: "Environment & Nature", icon: "🌍", description: "آيات تتحدث عن البيئة والطبيعة والحفاظ على الأرض والموارد الطبيعية", color: "#06b6d4", verse_count: 85 },
  { id: "general", name: "مواضيع عامة", name_en: "General Topics", icon: "🌐", description: "استكشف أي موضوع آخر في حياتك واحصل على إرشاد قرآني شامل", color: "#d4a843", verse_count: 500 },
];

export default function HomePage() {
  const [categories] = useState<Category[]>(defaultCategories);

  return (
    <div className="relative">
      <HeroSection />
      <section className="relative py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold font-display gradient-text mb-4">🗂️ فئات الحياة القرآنية</h2>
            <p className="text-gray-400 max-w-2xl mx-auto font-display">اختر الموضوع الذي يهمك واحصل على إرشاد قرآني مخصص بتقنية الذكاء الاصطناعي</p>
            <div className="mt-4 h-1 w-24 mx-auto bg-gradient-to-l from-quran-gold to-yellow-600 rounded-full" />
          </motion.div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {categories.map((category, index) => (<CategoryCard key={category.id} category={category} index={index} />))}
          </div>
        </div>
      </section>

      <section className="relative py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold font-display gradient-text mb-4">✨ مميزات المنصة</h2>
            <div className="mt-4 h-1 w-24 mx-auto bg-gradient-to-l from-quran-gold to-yellow-600 rounded-full" />
          </motion.div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[{ icon: "��", title: "ذكاء اصطناعي متقدم", description: "نستخدم أحدث تقنيات الذكاء الاصطناعي ومعالجة اللغة الطبيعية لفهم أسئلتك وتقديم إرشادات قرآنية دقيقة" }, { icon: "📖", title: "قاعدة بيانات شاملة", description: "تشمل جميع آيات القرآن الكريم مع التفاسير المتعددة من كبار العلماء والمفسرين" }, { icon: "🔬", title: "معجزات علمية موثقة", description: "اكتشف الحقائق العلمية المذكورة في القرآن قبل أن يكتشفها العلم الحديث بقرون" }, { icon: "🌐", title: "واجهة عربية متكاملة", description: "تصميم حديث وأنيق يدعم اللغة العربية بالكامل مع الخط العثماني الجميل" }, { icon: "🔍", title: "بحث ذكي ومتقدم", description: "ابحث بالكلمات المفتاحية أو المواضيع أو أرقام السور والآيات بسهولة ودقة" }, { icon: "📝", title: "تفاسير متعددة", description: "اطلع على تفاسير العلماء الموثقين لكل آية مع شرح مفصل وسياق تاريخي" }].map((feature, i) => (
              <motion.div key={i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }} viewport={{ once: true }} className="glass rounded-2xl p-8 border border-white/5 card-hover text-center">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold font-display text-white mb-3">{feature.title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed font-display">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="relative py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div initial={{ opacity: 0, scale: 0.95 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }} className="relative glass rounded-3xl p-12 border border-quran-gold/20 text-center overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-quran-gold/5 to-transparent" />
            <div className="relative z-10">
              <p className="quran-text text-2xl text-quran-gold mb-6 leading-loose">﴿ كِتَابٌ أَنزَلْنَاهُ إِلَيْكَ مُبَارَكٌ لِّيَدَّبَّرُوا آيَاتِهِ وَلِيَتَذَكَّرَ أُولُو الْأَلْبَابِ ﴾</p>
              <p className="text-sm text-gray-400 mb-8 font-display">سورة ص - الآية 29</p>
              <h3 className="text-2xl font-bold font-display text-white mb-4">ابدأ رحلتك مع القرآن الكريم الآن</h3>
              <a href="/ask" className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-l from-quran-gold to-yellow-600 text-quran-dark font-bold rounded-xl text-lg font-display shadow-lg shadow-quran-gold/20 hover:shadow-quran-gold/40 transition-all hover:scale-105">🤖 اسأل القرآن الآن</a>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
