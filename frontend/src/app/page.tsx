import Link from "next/link";
import Header from "@/components/Header";

const CATEGORIES = [
  {
    id: "medicine",
    nameAr: "الطب والصحة",
    icon: "🏥",
    description: "الإرشاد القرآني في الصحة والعلاج والوقاية من الأمراض",
  },
  {
    id: "work",
    nameAr: "العمل والمال",
    icon: "💼",
    description: "التوجيه الإلهي في الرزق والكسب الحلال وإدارة المال",
  },
  {
    id: "science",
    nameAr: "العلوم والتكنولوجيا",
    icon: "🔬",
    description: "الإعجاز العلمي في القرآن والحث على البحث والاكتشاف",
  },
  {
    id: "family",
    nameAr: "الأسرة والمجتمع",
    icon: "👨‍👩‍👧‍👦",
    description: "منظومة الأسرة في الإسلام والعلاقات الاجتماعية السليمة",
  },
  {
    id: "self_development",
    nameAr: "التطوير الذاتي",
    icon: "🧠",
    description: "بناء الشخصية المتكاملة وتحقيق النمو الروحي والعقلي",
  },
  {
    id: "law",
    nameAr: "القانون والعدالة",
    icon: "⚖️",
    description: "منظومة العدل والحقوق والواجبات في الشريعة الإسلامية",
  },
  {
    id: "environment",
    nameAr: "البيئة والطبيعة",
    icon: "🌍",
    description: "الحفاظ على البيئة وعمارة الأرض في ضوء القرآن الكريم",
  },
  {
    id: "chat",
    nameAr: "اسأل القرآن",
    icon: "💬",
    description: "تحدث مباشرة مع مساعدنا الذكي للحصول على إرشاد قرآني فوري",
  },
];

export default function HomePage() {
  return (
    <div className="min-h-screen" style={{ backgroundColor: "var(--claude-bg)" }}>
      <Header />

      {/* Hero section */}
      <section
        className="py-20 px-4 relative overflow-hidden"
        style={{ backgroundColor: "var(--claude-dark)" }}
      >
        {/* Subtle pattern overlay */}
        <div
          className="absolute inset-0 opacity-5"
          style={{
            backgroundImage:
              "radial-gradient(circle at 25% 50%, var(--claude-accent) 0%, transparent 50%), radial-gradient(circle at 75% 20%, #8B5CF6 0%, transparent 50%)",
          }}
        />
        <div className="max-w-4xl mx-auto text-center relative">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-medium mb-8"
            style={{
              backgroundColor: "rgba(217, 119, 87, 0.15)",
              border: "1px solid rgba(217, 119, 87, 0.3)",
              color: "var(--claude-accent-muted)",
            }}
          >
            <span className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ backgroundColor: "var(--claude-accent)" }}></span>
            مدعوم بالذكاء الاصطناعي
          </div>

          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight text-white">
            حلول الحياة
            <br />
            <span style={{ color: "var(--claude-accent)" }}>من القرآن الكريم</span>
          </h1>
          <p className="text-lg md:text-xl mb-10 leading-relaxed max-w-2xl mx-auto"
            style={{ color: "var(--claude-text-muted)" }}
          >
            منصة ذكية تساعدك في إيجاد الإرشاد والتوجيه القرآني لأي موضوع في حياتك،
            من الطب إلى الأعمال إلى العلاقات الأسرية وما بينها
          </p>

          {/* Quran verse card */}
          <div
            className="rounded-2xl p-6 mb-10 max-w-2xl mx-auto"
            style={{
              backgroundColor: "rgba(245, 239, 230, 0.06)",
              border: "1px solid rgba(232, 221, 209, 0.15)",
              backdropFilter: "blur(8px)",
            }}
          >
            <p className="quran-font text-white text-2xl mb-3">
              وَنَزَّلْنَا عَلَيْكَ الْكِتَابَ تِبْيَانًا لِّكُلِّ شَيْءٍ
            </p>
            <p className="text-sm" style={{ color: "var(--claude-text-subtle)" }}>
              سورة النحل — الآية 89
            </p>
          </div>

          <div className="flex flex-wrap gap-4 justify-center">
            <Link
              href="/ask"
              className="inline-flex items-center gap-2 font-bold py-4 px-8 rounded-xl text-lg transition-all shadow-lg"
              style={{ backgroundColor: "var(--claude-accent)", color: "white" }}
            >
              <span>💬</span> اسأل الآن
            </Link>
            <Link
              href="/reader"
              className="inline-flex items-center gap-2 font-bold py-4 px-8 rounded-xl text-lg transition-all"
              style={{
                backgroundColor: "rgba(255,255,255,0.08)",
                color: "white",
                border: "1px solid rgba(255,255,255,0.15)",
              }}
            >
              <span>📖</span> تصفح القرآن
            </Link>
          </div>
        </div>
      </section>

      {/* Stats section */}
      <section
        className="py-10 border-b"
        style={{ backgroundColor: "white", borderColor: "var(--claude-border)" }}
      >
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
                <div className="text-3xl font-bold mb-1" style={{ color: "var(--claude-accent)" }}>
                  {stat.number}
                </div>
                <div className="text-sm" style={{ color: "var(--claude-text-muted)" }}>
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories grid */}
      <section className="py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <div
              className="inline-block px-3 py-1 rounded-full text-xs font-semibold mb-4"
              style={{
                backgroundColor: "var(--claude-accent-light)",
                color: "var(--claude-accent-hover)",
              }}
            >
              مجالات الحياة
            </div>
            <h2 className="text-3xl font-bold mb-4" style={{ color: "var(--claude-text)" }}>
              استكشف بحسب اهتمامك
            </h2>
            <p className="max-w-xl mx-auto" style={{ color: "var(--claude-text-muted)" }}>
              اختر المجال الذي يهمك وسنقدم لك الإرشاد القرآني المناسب
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {CATEGORIES.map((cat) => (
              <Link
                key={cat.id}
                href={cat.id === "chat" ? "/ask" : `/categories/${cat.id}`}
                className="category-card flex flex-col items-center text-center gap-4 group"
              >
                <div
                  className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl shadow-sm group-hover:shadow-md transition-shadow"
                  style={{ backgroundColor: "var(--claude-surface)" }}
                >
                  {cat.icon}
                </div>
                <h3 className="text-lg font-bold" style={{ color: "var(--claude-text)" }}>
                  {cat.nameAr}
                </h3>
                <p className="text-sm leading-relaxed flex-1" style={{ color: "var(--claude-text-muted)" }}>
                  {cat.description}
                </p>
                <span
                  className="text-xs font-semibold px-4 py-1.5 rounded-full transition-colors"
                  style={{
                    backgroundColor: "var(--claude-accent-light)",
                    color: "var(--claude-accent-hover)",
                  }}
                >
                  استكشف ←
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16 px-4" style={{ backgroundColor: "var(--claude-surface)" }}>
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <div
              className="inline-block px-3 py-1 rounded-full text-xs font-semibold mb-4"
              style={{
                backgroundColor: "var(--claude-accent-light)",
                color: "var(--claude-accent-hover)",
              }}
            >
              كيف يعمل؟
            </div>
            <h2 className="text-3xl font-bold" style={{ color: "var(--claude-text)" }}>
              ثلاث خطوات بسيطة
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { step: "01", icon: "✍️", title: "اكتب سؤالك", desc: "اطرح أي سؤال يتعلق بحياتك بأي أسلوب" },
              { step: "02", icon: "🤖", title: "يحلل الذكاء الاصطناعي", desc: "يبحث النظام في القرآن الكريم وكتب التفسير" },
              { step: "03", icon: "📖", title: "تحصل على الإجابة", desc: "تستقبل إرشاداً قرآنياً دقيقاً مع آيات التلاوة" },
            ].map((item) => (
              <div key={item.step} className="card text-center relative">
                <div
                  className="absolute -top-3 right-6 text-xs font-bold px-2 py-0.5 rounded-md"
                  style={{
                    backgroundColor: "var(--claude-accent)",
                    color: "white",
                  }}
                >
                  {item.step}
                </div>
                <div
                  className="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl mx-auto mb-4 mt-2"
                  style={{ backgroundColor: "var(--claude-accent-light)" }}
                >
                  {item.icon}
                </div>
                <h3 className="text-lg font-bold mb-2" style={{ color: "var(--claude-text)" }}>
                  {item.title}
                </h3>
                <p className="text-sm" style={{ color: "var(--claude-text-muted)" }}>
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section
        className="py-16 px-4 text-center"
        style={{ backgroundColor: "var(--claude-dark)" }}
      >
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold mb-4 text-white">ابدأ رحلتك القرآنية الآن</h2>
          <p className="mb-8" style={{ color: "var(--claude-text-muted)" }}>
            أكثر من 6000 آية قرآنية تنتظر لمساعدتك في إيجاد الحلول
          </p>
          <Link
            href="/ask"
            className="inline-flex items-center gap-2 font-bold py-4 px-10 rounded-xl text-lg transition-all shadow-lg"
            style={{ backgroundColor: "var(--claude-accent)", color: "white" }}
          >
            <span>💬</span> اسأل القرآن الآن
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer
        className="py-10 px-4 text-center text-sm"
        style={{
          backgroundColor: "#1A1614",
          borderTop: "1px solid var(--claude-dark-3)",
          color: "var(--claude-text-subtle)",
        }}
      >
        <div className="max-w-2xl mx-auto space-y-3">
          <p>
            ⚠️ <strong style={{ color: "var(--claude-text-muted)" }}>تنبيه:</strong> هذه المنصة للتوجيه العام فقط وليست بديلاً عن الفتاوى الشرعية المعتمدة
          </p>
          <div
            className="w-16 mx-auto border-t"
            style={{ borderColor: "var(--claude-dark-3)" }}
          />
          <p style={{ color: "var(--claude-text-muted)" }}>
            تصميم وتطوير:{" "}
            <span className="font-semibold" style={{ color: "var(--claude-accent)" }}>
              عبدالعزيز بن سلطان العتيبي
            </span>
          </p>
          <p>© 2026 حلول الحياة من القرآن الكريم | جميع الحقوق محفوظة</p>
        </div>
      </footer>
    </div>
  );
}

