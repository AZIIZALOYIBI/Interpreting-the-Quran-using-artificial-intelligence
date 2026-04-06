import QuranReader from "@/components/QuranReader";
import Header from "@/components/Header";

export const metadata = {
  title: "القرآن الكريم | قراءة وتصفح",
};

export default function ReaderPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">📖 القرآن الكريم</h1>
          <p className="text-gray-500">تصفح القرآن الكريم بخط عثماني جميل</p>
        </div>
        <QuranReader />
      </main>
    </div>
  );
}
