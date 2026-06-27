"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import CategoryCard from "@/components/CategoryCard";
import { Category } from "@/types";

const defaultCategories: Category[] = [
  { id: "medicine", name: "الطب والصحة", name_en: "Medicine & Health", icon: "🏥", description: "اكتشف الإرشادات القرآنية المتعلقة بالصحة الجسدية والنفسية والغذاء والعلاج", color: "#22c55e", verse_count: 120 },
  { id: "work", name: "العمل والمال", name_en: "Work & Finance", icon: "💼", description: "تعرف على مبادئ الكسب الحلال والإدارة المالية وأخلاقيات العمل في ضوء القرآن الكريم", color: "#3b82f6", verse_count: 95 },
  { id: "science", name: "العلوم والمعرفة", name_en: "Science & Knowledge", icon: "🔬", description: "اكتشف الآيات المتعلقة بالعلوم الطبيعية والكونية والمعجزات العلمية", color: "#8b5cf6", verse_count: 150 },
  { id: "family", name: "الأسرة والمجتمع", name_en: "Family & Society", icon: "👨‍👩‍👧‍👦", description: "إرشادات قرآنية حول بناء الأسرة والعلاقات الزوجية وتربية الأبناء", color: "#f59e0b", verse_count: 200 },
  { id: "self_development", name: "التطوير الذاتي", name_en: "Self Development", icon: "🌱", description: "آيات تساعدك في تطوير شخصيتك وتحقيق التوازن النفسي والروحي", color: "#10b981", verse_count: 180 },
  { id: "law", name: "القانون والعدل", name_en: "Law & Justice", icon: "⚖️", description: "مبادئ العدل والمساواة والحقوق والواجبات كما وردت في القرآن الكريم", color: "#ef4444", verse_count: 130 },
  { id: "environment", name: "البيئة والطبيعة", name_en: "Environment & Nature", icon: "🌍", description: "آيات تتحدث عن البيئة والطبيعة والحفاظ على الأرض والموارد الطبيعية", color: "#06b6d4", verse_count: 85 },
  { id: "ethics", name: "الأخلاق والقيم", name_en: "Ethics & Values", icon: "🤝", description: "توجيهات قرآنية لبناء السلوك القويم، الصدق، الأمانة، والرحمة في التعامل اليومي", color: "#14b8a6", verse_count: 140 },
  { id: "general", name: "عام", name_en: "General", icon: "🌐", description: "استكشف أي موضوع آخر في حياتك واحصل على إرشاد قرآني شامل", color: "#d4a843", verse_count: 500 },
];

export default function HomePage() {
  const features = [
    { icon: "🤖", title: "إجابات قرآنية ذكية", description: "حلل سؤالك بالعربية واحصل على إجابة مرتبطة بآيات موثوقة وتوجيه واضح." },
    { icon: "📚", title: "تفسير متعدد المصادر", description: "الوصول السريع إلى معاني الآيات وتفاسيرها لتوسيع الفهم قبل اتخاذ القرار." },
    { icon: "🔎", title: "بحث موضوعي سريع", description: "ابحث في الموضوعات والسور والآيات للوصول للمحتوى المناسب خلال ثوان." },
    { icon: "⚡", title: "تجربة عملية يومية", description: "واجهة سريعة ومناسبة للجوال تساعدك على تطبيق التوجيه القرآني في الحياة اليومية." },
  ];

  const journey = [
    { step: "1", title: "اكتب سؤالك", description: "صف موقفك أو تحديك الواقعي بلغة بسيطة." },
    { step: "2", title: "اختر الفئة", description: "حدد المجال المناسب لتحسين دقة التوجيه." },
    { step: "3", title: "استلم الإجابة", description: "احصل على إرشاد مع آيات مرتبطة يمكنك الرجوع إليها مباشرة." },
  ];

  const useCases = [
    { title: "قرارات العمل والمال", description: "إرشاد أخلاقي وعملي للتعاملات المالية، العقود، والإنصاف في بيئة العمل." },
    { title: "العلاقات الأسرية", description: "توجيهات واضحة لبناء المودة والرحمة وحل الخلافات بميزان قرآني متزن." },
    { title: "تنمية النفس", description: "مسار يومي للثبات، الصبر، وإعادة ترتيب الأولويات وفق القيم القرآنية." },
  ];

  const faqs = [
    {
      question: "هل المنصة تقدم فتوى شرعية؟",
      answer: "لا. المنصة تقدم إرشادًا عامًا وتدبرًا قرآنيًا، ولا تغني عن الرجوع للعلماء المؤهلين في مسائل الفتوى.",
    },
    {
      question: "كيف أستفيد بأفضل شكل من الإجابات؟",
      answer: "اكتب سؤالك بصيغة واضحة وحدد الفئة المناسبة، ثم راجع الآيات المرتبطة وتفسيرها قبل اتخاذ القرار.",
    },
    {
      question: "هل يمكنني استخدام المنصة يوميًا؟",
      answer: "نعم. المنصة مصممة للاستخدام السريع اليومي على الجوال وسطح المكتب مع تجربة عربية كاملة.",
    },
  ];

  return (
    <main className="relative overflow-hidden">
      <div className="absolute inset-0 animated-bg" />
      <div className="absolute top-10 right-10 h-80 w-80 rounded-full bg-quran-gold/10 blur-3xl" />
      <div className="absolute bottom-10 left-10 h-80 w-80 rounded-full bg-emerald-500/10 blur-3xl" />

      <section className="relative px-4 pb-20 pt-16 sm:pt-24">
        <div className="mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-8 inline-flex items-center gap-2 rounded-full border border-quran-gold/30 bg-black/25 px-4 py-2"
          >
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            <span className="text-sm text-gray-200">منصة إرشاد قرآني مدعومة بالذكاء الاصطناعي</span>
          </motion.div>

          <div className="grid items-center gap-10 lg:grid-cols-2">
            <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
              <h1 className="mb-6 text-4xl font-bold leading-tight text-white sm:text-5xl lg:text-6xl">
                <span className="gradient-text">حلول الحياة</span>
                <br />
                من القرآن الكريم
              </h1>
              <p className="mb-6 text-lg leading-8 text-gray-300">
                حوّل أسئلتك اليومية إلى رحلة فهم قرآنية واضحة. المنصة تقدم توجيهًا عمليًا، آيات ذات صلة، ومسارًا أبسط لاتخاذ قرارات متوازنة.
              </p>
              <p className="quran-text mb-8 text-xl text-quran-gold/90">﴿ كِتَابٌ أَنزَلْنَاهُ إِلَيْكَ مُبَارَكٌ لِّيَدَّبَّرُوا آيَاتِهِ ﴾</p>
              <div className="flex flex-wrap items-center gap-3">
                <Link href="/ask" className="rounded-xl bg-gradient-to-l from-quran-gold to-yellow-600 px-6 py-3 text-base font-bold text-quran-dark transition hover:scale-[1.02]">
                  ابدأ بسؤالك الآن
                </Link>
                <Link href="/quran-reader" className="rounded-xl border border-quran-gold/30 bg-white/5 px-6 py-3 text-base font-bold text-quran-gold transition hover:bg-quran-gold/10">
                  تصفح المصحف
                </Link>
              </div>
            </motion.div>

            <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass rounded-3xl border border-white/10 p-6 sm:p-8">
              <h2 className="mb-6 text-2xl font-bold text-white">لماذا هذه المنصة؟</h2>
              <div className="mb-6 grid grid-cols-2 gap-4">
                {[
                  { value: "6,236", label: "آية" },
                  { value: "114", label: "سورة" },
                  { value: "9", label: "فئات رئيسية" },
                  { value: "24/7", label: "إتاحة رقمية" },
                ].map((item) => (
                  <div key={item.label} className="rounded-2xl border border-white/10 bg-black/20 p-4 text-center">
                    <p className="mb-1 text-2xl font-bold gradient-text">{item.value}</p>
                    <p className="text-sm text-gray-300">{item.label}</p>
                  </div>
                ))}
              </div>
              <div className="rounded-2xl border border-quran-gold/20 bg-black/30 p-4">
                <p className="mb-2 text-sm text-quran-gold">مثال سريع للإجابة</p>
                <p className="text-sm leading-7 text-gray-300">
                  &quot;عند ضغط العمل، وجّه القرآن إلى التوازن بين السعي والسكينة، والصدق في النية، مع الصبر واتخاذ الأسباب.&quot;
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      <section className="relative px-4 py-16">
        <div className="max-w-7xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="mb-12 text-center">
            <h2 className="mb-4 text-3xl font-bold gradient-text sm:text-4xl">حلول عملية لكل جانب من حياتك</h2>
            <p className="mx-auto max-w-2xl text-gray-300">تم تصميم المنصة لتغطي الاحتياجات اليومية الأكثر شيوعًا حتى تجد التوجيه المناسب بسرعة.</p>
            <div className="mt-4 h-1 w-24 mx-auto bg-gradient-to-l from-quran-gold to-yellow-600 rounded-full" />
          </motion.div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {defaultCategories.map((category, index) => (
              <CategoryCard key={category.id} category={category} index={index} />
            ))}
          </div>
        </div>
      </section>

      <section className="relative px-4 py-16">
        <div className="max-w-7xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="mb-12 text-center">
            <h2 className="mb-4 text-3xl font-bold gradient-text sm:text-4xl">مزايا احترافية لتجربة موثوقة</h2>
            <div className="mt-4 h-1 w-24 mx-auto bg-gradient-to-l from-quran-gold to-yellow-600 rounded-full" />
          </motion.div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
            {features.map((feature, i) => (
              <motion.div key={feature.title} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }} viewport={{ once: true }} className="glass card-hover rounded-2xl border border-white/5 p-6 text-center">
                <div className="mb-4 text-4xl">{feature.icon}</div>
                <h3 className="mb-2 text-xl font-bold text-white">{feature.title}</h3>
                <p className="text-sm leading-7 text-gray-300">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="relative px-4 py-16">
        <div className="mx-auto max-w-7xl">
          <motion.div initial={{ opacity: 0, y: 18 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="mb-10 text-center">
            <h2 className="mb-4 text-3xl font-bold gradient-text sm:text-4xl">حالات استخدام واقعية</h2>
            <p className="mx-auto max-w-2xl text-gray-300">المنصة موجهة لمشكلات الحياة اليومية، لا مجرد عرض معلومات.</p>
          </motion.div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            {useCases.map((item, index) => (
              <motion.div key={item.title} initial={{ opacity: 0, y: 16 }} whileInView={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.1 }} viewport={{ once: true }} className="glass rounded-2xl border border-white/10 p-6">
                <h3 className="mb-3 text-xl font-bold text-white">{item.title}</h3>
                <p className="text-sm leading-7 text-gray-300">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="relative px-4 py-16">
        <div className="mx-auto max-w-6xl">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="mb-8 text-center">
            <h2 className="mb-4 text-3xl font-bold gradient-text sm:text-4xl">كيف تبدأ خلال دقيقة؟</h2>
          </motion.div>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            {journey.map((item, index) => (
              <motion.div key={item.step} initial={{ opacity: 0, y: 16 }} whileInView={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.1 }} viewport={{ once: true }} className="glass rounded-2xl border border-white/10 p-6">
                <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-full bg-quran-gold/20 text-lg font-bold text-quran-gold">{item.step}</div>
                <h3 className="mb-2 text-xl font-bold text-white">{item.title}</h3>
                <p className="text-sm leading-7 text-gray-300">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="relative px-4 py-10">
        <div className="mx-auto max-w-5xl">
          <motion.div initial={{ opacity: 0, y: 18 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="mb-8 text-center">
            <h2 className="mb-4 text-3xl font-bold gradient-text sm:text-4xl">أسئلة شائعة</h2>
          </motion.div>

          <div className="space-y-4">
            {faqs.map((faq) => (
              <motion.details key={faq.question} initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="glass rounded-2xl border border-white/10 p-5">
                <summary className="cursor-pointer list-none text-base font-bold text-white">{faq.question}</summary>
                <p className="mt-3 text-sm leading-7 text-gray-300">{faq.answer}</p>
              </motion.details>
            ))}
          </div>
        </div>
      </section>

      <section className="relative px-4 pb-24 pt-10">
        <div className="max-w-4xl mx-auto">
          <motion.div initial={{ opacity: 0, scale: 0.95 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }} className="relative overflow-hidden rounded-3xl border border-quran-gold/20 glass p-12 text-center">
            <div className="absolute inset-0 bg-gradient-to-br from-quran-gold/5 to-transparent" />
            <div className="relative z-10">
              <p className="quran-text mb-6 text-2xl leading-loose text-quran-gold">﴿ وَقُل رَّبِّ زِدْنِي عِلْمًا ﴾</p>
              <p className="mb-8 text-sm text-gray-300">سورة طه - الآية 114</p>
              <h3 className="mb-4 text-2xl font-bold text-white">ابدأ الآن بخطوة بسيطة نحو فهم أعمق</h3>
              <p className="mx-auto mb-8 max-w-2xl text-gray-300">اكتب سؤالك، استكشف الإجابة، وارجع للآيات بسهولة. رحلة التدبر تبدأ من هنا.</p>
              <Link href="/ask" className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-l from-quran-gold to-yellow-600 px-8 py-4 text-lg font-bold text-quran-dark shadow-lg shadow-quran-gold/20 transition hover:scale-[1.02] hover:shadow-quran-gold/40">
                🤖 اسأل القرآن الآن
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </main>
  );
}
