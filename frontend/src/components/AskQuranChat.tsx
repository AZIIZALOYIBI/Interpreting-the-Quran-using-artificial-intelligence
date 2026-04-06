"use client";
import { useState, useRef, useEffect, useCallback } from "react";
import type { Message, Ayah } from "@/types";
import { askQuran } from "@/lib/api";

const QUICK_QUESTIONS = [
  { text: "كيف أتعامل مع الضغوط النفسية؟", category: "self_development" },
  { text: "ما حكم الإسلام في التداوي والطب؟", category: "medicine" },
  { text: "كيف أبارك في رزقي ومالي؟", category: "work" },
  { text: "ما هو دور الأسرة في الإسلام؟", category: "family" },
  { text: "كيف يحث الإسلام على طلب العلم؟", category: "science" },
  { text: "ما موقف الإسلام من العدل والحقوق؟", category: "law" },
  { text: "كيف يأمر الإسلام بحماية البيئة؟", category: "environment" },
  { text: "كيف أقوى إيماني وعلاقتي بالله؟", category: "self_development" },
];

const CATEGORY_LABELS: Record<string, string> = {
  medicine: "الطب والصحة",
  work: "العمل والمال",
  science: "العلوم",
  family: "الأسرة",
  self_development: "التطوير الذاتي",
  law: "القانون",
  environment: "البيئة",
  chat: "عام",
};

function AyahCard({ ayah }: { ayah: Ayah }) {
  return (
    <div className="ayah-card">
      <p className="quran-font text-gray-800 mb-3">{ayah.textUthmani}</p>
      <div className="flex items-center justify-between text-sm border-t border-amber-200 pt-2">
        <span className="text-amber-700 font-semibold">{ayah.surahNameAr}</span>
        <span className="text-gray-500">الآية {ayah.ayahNumber}</span>
      </div>
      {ayah.tafsir && (
        <div className="mt-3 p-3 bg-white rounded-lg border border-amber-100">
          <p className="text-sm text-gray-600 leading-relaxed">{ayah.tafsir}</p>
        </div>
      )}
    </div>
  );
}

export default function AskQuranChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content: "مرحباً بك في منصة حلول الحياة من القرآن الكريم 🌿\n\nيمكنك سؤالي عن أي موضوع في حياتك، وسأبحث لك عن الإرشاد والتوجيه القرآني الكريم.\n\nاختر سؤالاً من الأسئلة السريعة أو اكتب سؤالك الخاص.",
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = useCallback(
    async (text: string, category?: string) => {
      if (!text.trim() || loading) return;

      const userMessage: Message = {
        id: Date.now().toString(),
        role: "user",
        content: text.trim(),
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setInputText("");
      setLoading(true);

      try {
        const response = await askQuran(text.trim(), category);

        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: response.answer,
          ayahs: response.ayahs,
          category: response.category,
          practicalSteps: response.practicalSteps,
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch {
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: "عذراً، حدث خطأ في الاتصال. يرجى التأكد من تشغيل الخادم والمحاولة مرة أخرى.",
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setLoading(false);
      }
    },
    [loading]
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputText);
  };

  return (
    <div className="flex flex-col h-full max-h-[85vh] bg-white rounded-2xl shadow-xl overflow-hidden">
      {/* Chat header */}
      <div className="bg-emerald-800 text-white p-4 flex items-center gap-3">
        <div className="w-10 h-10 bg-emerald-600 rounded-full flex items-center justify-center text-xl">
          📖
        </div>
        <div>
          <h2 className="font-bold text-lg">اسأل القرآن</h2>
          <p className="text-emerald-200 text-xs">مساعدك القرآني الذكي</p>
        </div>
        <div className="mr-auto flex items-center gap-2">
          <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
          <span className="text-xs text-emerald-200">متصل</span>
        </div>
      </div>

      {/* Quick questions */}
      <div className="border-b border-gray-100 p-3 bg-gray-50">
        <p className="text-xs text-gray-500 mb-2 font-medium">أسئلة سريعة:</p>
        <div className="flex flex-wrap gap-2">
          {QUICK_QUESTIONS.map((q, i) => (
            <button
              key={i}
              onClick={() => sendMessage(q.text, q.category)}
              disabled={loading}
              className="text-xs bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 px-3 py-1.5 rounded-full transition-colors disabled:opacity-50"
            >
              {q.text}
            </button>
          ))}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === "user" ? "justify-start" : "justify-end"}`}
          >
            <div
              className={`max-w-[85%] ${
                message.role === "user"
                  ? "bg-emerald-600 text-white rounded-2xl rounded-tl-sm px-4 py-3"
                  : "bg-gray-50 border border-gray-200 rounded-2xl rounded-tr-sm p-4 w-full"
              }`}
            >
              {/* Category badge */}
              {message.category && (
                <span className="inline-block bg-emerald-100 text-emerald-700 text-xs px-2 py-0.5 rounded-full mb-2">
                  {CATEGORY_LABELS[message.category] || message.category}
                </span>
              )}

              {/* Content */}
              <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>

              {/* Ayahs */}
              {message.ayahs && message.ayahs.length > 0 && (
                <div className="mt-4 space-y-3">
                  <p className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                    <span>📖</span> الآيات ذات الصلة
                  </p>
                  {message.ayahs.map((ayah, i) => (
                    <AyahCard key={i} ayah={ayah} />
                  ))}
                </div>
              )}

              {/* Practical steps */}
              {message.practicalSteps && message.practicalSteps.length > 0 && (
                <div className="mt-4 bg-emerald-50 border border-emerald-200 rounded-xl p-4">
                  <p className="text-sm font-semibold text-emerald-800 mb-2 flex items-center gap-2">
                    <span>✅</span> خطوات عملية
                  </p>
                  <ul className="space-y-2">
                    {message.practicalSteps.map((step, i) => (
                      <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                        <span className="text-emerald-500 mt-0.5 flex-shrink-0">•</span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <p className="text-xs text-gray-400 mt-2">
                {message.timestamp.toLocaleTimeString("ar-EG")}
              </p>
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-end">
            <div className="bg-gray-50 border border-gray-200 rounded-2xl rounded-tr-sm p-4">
              <div className="flex items-center gap-2 text-gray-500">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></span>
                  <span className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></span>
                  <span className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></span>
                </div>
                <span className="text-sm">جاري البحث في القرآن الكريم...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Disclaimer */}
      <div className="bg-amber-50 border-t border-amber-200 px-4 py-2">
        <p className="text-xs text-amber-700 text-center">
          ⚠️ هذه المنصة للاستئناس والتوجيه العام فقط. يُرجى الرجوع إلى العلماء المتخصصين في المسائل الدينية الدقيقة.
        </p>
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200 bg-white">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="اكتب سؤالك هنا..."
            disabled={loading}
            className="flex-1 border-2 border-gray-200 focus:border-emerald-500 rounded-xl px-4 py-3 text-right focus:outline-none transition-colors disabled:bg-gray-50"
            dir="rtl"
          />
          <button
            type="submit"
            disabled={loading || !inputText.trim()}
            className="btn-primary px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              "إرسال"
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
