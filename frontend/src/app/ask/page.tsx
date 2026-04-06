import AskQuranChat from "@/components/AskQuranChat";
import Header from "@/components/Header";

export const metadata = {
  title: "اسأل القرآن | حلول الحياة من القرآن الكريم",
};

export default function AskPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">اسأل القرآن الكريم</h1>
          <p className="text-gray-500">اطرح سؤالك وسنجد لك الإرشاد القرآني المناسب</p>
        </div>
        <AskQuranChat />
      </main>
    </div>
  );
}
