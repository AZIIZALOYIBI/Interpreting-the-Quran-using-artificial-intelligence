import Link from "next/link";
import Header from "@/components/Header";

const CATEGORIES = [
  {
    id: "medicine",
    nameAr: "الطب والصحة",
    icon: "🏥",
    description: "الإرشاد القرآني في الصحة والعلاج والوقاية من الأمراض",
    bgColor: "bg-green-50",
    borderColor: "border-green-300",
    textColor: "text-green-700",
    badgeColor: "bg-green-600",
  },
  {
    id: "work",
    nameAr: "العمل والمال",
    icon: "💼",
    description: "التوجيه الإلهي في الرزق والكسب الحلال وإدارة المال",
    bgColor: "bg-blue-50",
    borderColor: "border-blue-300",
    textColor: "text-blue-700",
    badgeColor: "bg-blue-600",
  },
  {
    id: "science",
    nameAr: "العلوم والتكنولوجيا",
    icon: "🔬",
    description: "الإعجاز العلمي في القرآن والحث على البحث والاكتشاف",
    bgColor: "bg-purple-50",
    borderColor: "border-purple-300",
    textColor: "text-purple-700",
    badgeColor: "bg-purple-600",
  },
  {
    id: "family",
    nameAr: "الأسرة والمجتمع",
    icon: "👨‍👩‍👧‍👦",
    description: "منظومة الأسرة في الإسلام والعلاقات الاجتماعية السليمة",
    bgColor: "bg-orange-50",
    borderColor: "border-orange-300",
    textColor: "text-orange-700",
    badgeColor: "bg-orange-600",
  },
  {
    id: "self_development",
    nameAr: "التطوير الذاتي",
    icon: "🧠",
    description: "بناء الشخصية المتكاملة وتحقيق النمو الروحي والعقلي",
    bgColor: "bg-yellow-50",
    borderColor: "border-yellow-300",
    textColor: "text-yellow-700",
    badgeColor: "bg-yellow-600",
  },
  {
    id: "law",
    nameAr: "القانون والعدالة",
    icon: "⚖️",
    description: "منظومة العدل والحقوق والواجبات في الشريعة الإسلامية",
    bgColor: "bg-red-50",
    borderColor: "border-red-300",
    textColor: "text-red-700",
    badgeColor: "bg-red-600",
  },
  {
    id: "environment",
    nameAr: "البيئة والطبيعة",
    icon: "🌍",
    description: "الحفاظ على البيئة وعمارة الأرض في ضوء القرآن الكريم",
    bgColor: "bg-teal-50",
    borderColor: "border-teal-300",
    textColor: "text-teal-700",
    badgeColor: "bg-teal-600",
  },
  {
    id: "chat",
    nameAr: "اسأل القرآن",
    icon: "💬",
    description: "تحدث مباشرة مع مساعدنا الذكي للحصول على إرشاد قرآني فوري",
    bgColor: "bg-emerald-50",
    borderColor: "border-emerald-300",
    textColor: "text-emerald-700",
    badgeColor: "bg-emerald-600",
  },
];

export default function HomePage() {
  return (
    <div className="min-h-screen">
      <Header />

      {/* Hero section */}
      <section className="bg-gradient-to-br from-emerald-900 via-emerald-800 to-teal-800 text-white py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="text-6xl mb-6">📖</div>
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
            حلول الحياة من القرآن الكريم
            <br />
            <span className="text-amber-400">بالذكاء الاصطناعي</span>
          </h1>
          <p className="text-xl text-emerald-100 mb-8 leading-relaxed max-w-2xl mx-auto">
            منصة ذكية تساعدك في إيجاد الإرشاد والتوجيه القرآني لأي موضوع في حياتك،
            من الطب إلى الأعمال إلى العلاقات الأسرية وما بينها
          </p>

          {/* Quran verse */}
          <div className="bg-white/10 backdrop-blur rounded-2xl p-6 mb-10 max-w-2xl mx-auto border border-white/20">
            <p className="quran-font text-white text-2xl mb-2">
              وَنَزَّلْنَا عَلَيْكَ الْكِتَابَ تِبْيَانًا لِّكُلِّ شَيْءٍ
            </p>
            <p className="text-emerald-200 text-sm">سورة النحل - الآية 89</p>
          </div>

          <div className="flex flex-wrap gap-4 justify-center">
            <Link
              href="/ask"
              className="bg-amber-500 hover:bg-amber-600 text-white font-bold py-4 px-8 rounded-xl text-lg transition-colors flex items-center gap-2"
            >
              <span>💬</span> اسأل الآن
            </Link>
            <Link
              href="/reader"
              className="bg-white/20 hover:bg-white/30 text-white font-bold py-4 px-8 rounded-xl text-lg transition-colors backdrop-blur flex items-center gap-2"
            >
              <span>📖</span> تصفح القرآن
            </Link>
          </div>
        </div>
      </section>

      {/* Stats section */}
      <section className="bg-white py-10 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            {[
              { number: "6,236", label: "آية قرآنية", icon: "📜" },
              { number: "114", label: "سورة كريمة", icon: "📚" },
              { number: "8", label: "مجالات حياتية", icon: "🎯" },
              { number: "∞", label: "إجابات قرآنية", icon: "✨" },
            ].map((stat, i) => (
              <div key={i} className="p-4">
                <div className="text-3xl mb-2">{stat.icon}</div>
                <div className="text-3xl font-bold text-emerald-700">{stat.number}</div>
                <div className="text-gray-500 text-sm mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories grid */}
      <section className="py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">مجالات الحياة</h2>
            <p className="text-gray-500 max-w-xl mx-auto">
              اختر المجال الذي يهمك وسنقدم لك الإرشاد القرآني المناسب
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {CATEGORIES.map((cat) => (
              <Link
                key={cat.id}
                href={cat.id === "chat" ? "/ask" : `/categories/${cat.id}`}
                className={`category-card ${cat.bgColor} border ${cat.borderColor} flex flex-col items-center text-center gap-4`}
              >
                <span className="text-5xl">{cat.icon}</span>
                <h3 className={`text-xl font-bold ${cat.textColor}`}>{cat.nameAr}</h3>
                <p className="text-gray-600 text-sm leading-relaxed flex-1">{cat.description}</p>
                <span className={`text-xs font-semibold px-4 py-1.5 rounded-full ${cat.badgeColor} text-white`}>
                  استكشف →
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16 px-4 bg-emerald-50">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">كيف يعمل؟</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { step: "1", icon: "✍️", title: "اكتب سؤالك", desc: "اطرح أي سؤال يتعلق بحياتك بأي أسلوب" },
              { step: "2", icon: "🤖", title: "يحلل الذكاء الاصطناعي", desc: "يبحث النظام في القرآن الكريم وكتب التفسير" },
              { step: "3", icon: "📖", title: "تحصل على الإجابة", desc: "تستقبل إرشاداً قرآنياً دقيقاً مع آيات التلاوة" },
            ].map((item) => (
              <div key={item.step} className="text-center card">
                <div className="w-14 h-14 bg-emerald-600 text-white rounded-full flex items-center justify-center text-2xl mx-auto mb-4">
                  {item.icon}
                </div>
                <div className="text-5xl font-bold text-emerald-100 mb-2">{item.step}</div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">{item.title}</h3>
                <p className="text-gray-500">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 px-4 bg-emerald-800 text-white text-center">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold mb-4">ابدأ رحلتك القرآنية الآن</h2>
          <p className="text-emerald-200 mb-8">
            أكثر من 6000 آية قرآنية تنتظر لمساعدتك في إيجاد الحلول
          </p>
          <Link
            href="/ask"
            className="inline-flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-white font-bold py-4 px-10 rounded-xl text-lg transition-colors"
          >
            <span>💬</span> اسأل القرآن الآن
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8 px-4 text-center text-sm">
        <p className="mb-2">
          ⚠️ <strong>تنبيه:</strong> هذه المنصة للتوجيه العام فقط وليست بديلاً عن الفتاوى الشرعية المعتمدة
        </p>
        <p>© 2024 حلول الحياة من القرآن الكريم | جميع الحقوق محفوظة</p>
      </footer>
    </div>
  );
}
