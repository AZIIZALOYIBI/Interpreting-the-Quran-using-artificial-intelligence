import QuranReader from "@/components/QuranReader";
import Footer from "@/components/Footer";
import Header from "@/components/Header";

export const metadata = {
  title: "القرآن الكريم | قراءة وتصفح",
};

export default function ReaderPage() {
  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--claude-bg)" }}>
      <Header />

      {/* Page hero */}
      <div
        className="py-10 px-4 text-center"
        style={{ backgroundColor: "var(--claude-dark)", borderBottom: "1px solid var(--claude-dark-3)" }}
      >
        <div
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-medium mb-4"
          style={{
            backgroundColor: "rgba(217, 119, 87, 0.15)",
            border: "1px solid rgba(217, 119, 87, 0.3)",
            color: "var(--claude-accent-muted)",
          }}
        >
          <span>📖</span> تصفح بالخط العثماني
        </div>
        <h1 className="text-3xl md:text-4xl font-bold text-white mb-3">
          القرآن <span style={{ color: "var(--claude-accent)" }}>الكريم</span>
        </h1>
        <p className="text-base max-w-xl mx-auto" style={{ color: "var(--claude-text-muted)" }}>
          تصفح آيات القرآن الكريم بخط عثماني جميل واستمتع بتجربة قراءة روحانية
        </p>
      </div>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-8">
        <QuranReader />
      </main>

      <Footer />
    </div>
  );
}
