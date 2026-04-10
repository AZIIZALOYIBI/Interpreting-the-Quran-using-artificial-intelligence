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
  { text: "ما أذكار الصباح والمساء في القرآن؟", category: "general" },
  { text: "كيف يعالج الإسلام الحزن والاكتئاب؟", category: "self_development" },
];

const CATEGORY_LABELS: Record<string, string> = {
  medicine: "الطب والصحة",
  work: "العمل والمال",
  science: "العلوم",
  family: "الأسرة",
  self_development: "التطوير الذاتي",
  law: "القانون",
  environment: "البيئة",
  ethics: "الأخلاق والقيم",
  azkar: "الأذكار",
  chat: "عام",
  general: "عام",
};

function CopyButton({ message }: { message: { content: string; ayahs?: { surahNameAr: string; ayahNumber: number; textUthmani: string }[] } }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    let text = message.content;
    if (message.ayahs && message.ayahs.length > 0) {
      text += "\n\n" + message.ayahs.map((a) => `${a.textUthmani}\n— ${a.surahNameAr}: ${a.ayahNumber}`).join("\n\n");
    }
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <button
      onClick={handleCopy}
      title="نسخ الرسالة"
      className="absolute top-3 left-3 text-xs px-2 py-1 rounded-lg transition-all"
      style={{
        backgroundColor: copied ? "var(--claude-accent-light)" : "var(--claude-surface)",
        color: copied ? "var(--claude-accent-hover)" : "var(--claude-text-muted)",
        border: "1px solid var(--claude-border)",
      }}
    >
      {copied ? "✓ تم النسخ" : "📋"}
    </button>
  );
}

function AyahCard({ ayah }: { ayah: Ayah }) {
  return (
    <div className="ayah-card">
      <p className="quran-font mb-3" style={{ color: "var(--claude-text)" }}>
        {ayah.textUthmani}
      </p>
      <div
        className="flex items-center justify-between text-sm border-t pt-2"
        style={{ borderColor: "var(--claude-gold-border)" }}
      >
        <span className="font-semibold" style={{ color: "var(--claude-gold)" }}>
          {ayah.surahNameAr}
        </span>
        <span style={{ color: "var(--claude-text-muted)" }}>الآية {ayah.ayahNumber}</span>
      </div>
      {ayah.tafsir && (
        <div
          className="mt-3 p-3 rounded-lg border"
          style={{
            backgroundColor: "white",
            borderColor: "var(--claude-gold-border)",
          }}
        >
          <p className="text-sm leading-relaxed" style={{ color: "var(--claude-text-secondary)" }}>
            {ayah.tafsir}
          </p>
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
    <div
      className="flex flex-col h-full max-h-[85vh] rounded-2xl overflow-hidden"
      style={{
        backgroundColor: "white",
        border: "1px solid var(--claude-border)",
        boxShadow: "0 4px 24px rgba(28, 25, 23, 0.08)",
      }}
    >
      {/* Chat header */}
      <div
        className="p-4 flex items-center gap-3"
        style={{ backgroundColor: "var(--claude-dark)", borderBottom: "1px solid var(--claude-dark-3)" }}
      >
        <div
          className="w-10 h-10 rounded-xl flex items-center justify-center text-lg font-bold"
          style={{ backgroundColor: "var(--claude-accent)", color: "white" }}
        >
          ق
        </div>
        <div>
          <h2 className="font-bold text-base text-white">اسأل القرآن</h2>
          <p className="text-xs" style={{ color: "var(--claude-text-subtle)" }}>
            مساعدك القرآني الذكي
          </p>
        </div>
        <div className="mr-auto flex items-center gap-2">
          <span
            className="w-2 h-2 rounded-full animate-pulse"
            style={{ backgroundColor: "#4ADE80" }}
          ></span>
          <span className="text-xs" style={{ color: "var(--claude-text-subtle)" }}>
            متصل
          </span>
        </div>
      </div>

      {/* Quick questions */}
      <div
        className="border-b p-3"
        style={{
          backgroundColor: "var(--claude-surface)",
          borderColor: "var(--claude-border)",
        }}
      >
        <p className="text-xs font-medium mb-2" style={{ color: "var(--claude-text-muted)" }}>
          أسئلة سريعة:
        </p>
        <div className="flex flex-wrap gap-2">
          {QUICK_QUESTIONS.map((q, i) => (
            <button
              key={i}
              onClick={() => sendMessage(q.text, q.category)}
              disabled={loading}
              className="text-xs px-3 py-1.5 rounded-full transition-all disabled:opacity-50"
              style={{
                backgroundColor: "white",
                border: "1px solid var(--claude-border)",
                color: "var(--claude-text-secondary)",
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLElement).style.borderColor = "var(--claude-accent)";
                (e.currentTarget as HTMLElement).style.color = "var(--claude-accent-hover)";
                (e.currentTarget as HTMLElement).style.backgroundColor = "var(--claude-accent-light)";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLElement).style.borderColor = "var(--claude-border)";
                (e.currentTarget as HTMLElement).style.color = "var(--claude-text-secondary)";
                (e.currentTarget as HTMLElement).style.backgroundColor = "white";
              }}
            >
              {q.text}
            </button>
          ))}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4" style={{ backgroundColor: "var(--claude-bg)" }}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === "user" ? "justify-start" : "justify-end"}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl ${
                message.role === "user"
                  ? "rounded-tl-sm px-4 py-3"
                  : "rounded-tr-sm p-4 w-full relative"
              }`}
              style={
                message.role === "user"
                  ? { backgroundColor: "var(--claude-accent)", color: "white" }
                  : {
                      backgroundColor: "white",
                      border: "1px solid var(--claude-border)",
                      color: "var(--claude-text)",
                    }
              }
            >
              {/* Copy button for assistant messages */}
              {message.role === "assistant" && message.id !== "welcome" && (
                <CopyButton message={message} />
              )}
              {/* Category badge */}
              {message.category && (
                <span
                  className="inline-block text-xs px-2 py-0.5 rounded-full mb-2"
                  style={{
                    backgroundColor: "var(--claude-accent-light)",
                    color: "var(--claude-accent-hover)",
                  }}
                >
                  {CATEGORY_LABELS[message.category] || message.category}
                </span>
              )}

              {/* Content */}
              <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>

              {/* Ayahs */}
              {message.ayahs && message.ayahs.length > 0 && (
                <div className="mt-4 space-y-3">
                  <p
                    className="text-sm font-semibold flex items-center gap-2"
                    style={{ color: "var(--claude-text-secondary)" }}
                  >
                    <span>📖</span> الآيات ذات الصلة
                  </p>
                  {message.ayahs.map((ayah, i) => (
                    <AyahCard key={i} ayah={ayah} />
                  ))}
                </div>
              )}

              {/* Practical steps */}
              {message.practicalSteps && message.practicalSteps.length > 0 && (
                <div
                  className="mt-4 rounded-xl p-4 border"
                  style={{
                    backgroundColor: "var(--claude-surface)",
                    borderColor: "var(--claude-border)",
                  }}
                >
                  <p
                    className="text-sm font-semibold mb-2 flex items-center gap-2"
                    style={{ color: "var(--claude-text)" }}
                  >
                    <span>✅</span> خطوات عملية
                  </p>
                  <ul className="space-y-2">
                    {message.practicalSteps.map((step, i) => (
                      <li
                        key={i}
                        className="text-sm flex items-start gap-2"
                        style={{ color: "var(--claude-text-secondary)" }}
                      >
                        <span style={{ color: "var(--claude-accent)", marginTop: "2px", flexShrink: 0 }}>•</span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <p
                className="text-xs mt-2"
                style={{
                  color:
                    message.role === "user"
                      ? "rgba(255,255,255,0.6)"
                      : "var(--claude-text-subtle)",
                }}
              >
                {message.timestamp.toLocaleTimeString("ar-EG")}
              </p>
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-end">
            <div
              className="rounded-2xl rounded-tr-sm p-4"
              style={{
                backgroundColor: "white",
                border: "1px solid var(--claude-border)",
              }}
            >
              <div className="flex items-center gap-2" style={{ color: "var(--claude-text-muted)" }}>
                <div className="flex gap-1">
                  {[0, 150, 300].map((delay) => (
                    <span
                      key={delay}
                      className="w-2 h-2 rounded-full animate-bounce"
                      style={{
                        backgroundColor: "var(--claude-accent)",
                        animationDelay: `${delay}ms`,
                      }}
                    ></span>
                  ))}
                </div>
                <span className="text-sm">جاري البحث في القرآن الكريم...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Disclaimer */}
      <div
        className="px-4 py-2 border-t"
        style={{
          backgroundColor: "var(--claude-accent-light)",
          borderColor: "var(--claude-accent-muted)",
        }}
      >
        <p className="text-xs text-center" style={{ color: "var(--claude-accent-hover)" }}>
          ⚠️ هذه المنصة للاستئناس والتوجيه العام فقط. يُرجى الرجوع إلى العلماء المتخصصين في المسائل الدينية الدقيقة.
        </p>
      </div>

      {/* Input */}
      <form
        onSubmit={handleSubmit}
        className="p-4 border-t"
        style={{ backgroundColor: "white", borderColor: "var(--claude-border)" }}
      >
        <div className="flex gap-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="اكتب سؤالك هنا..."
            disabled={loading}
            maxLength={500}
            className="flex-1 rounded-xl px-4 py-3 text-right focus:outline-none transition-all"
            style={{
              border: "1.5px solid var(--claude-border)",
              backgroundColor: "var(--claude-bg)",
              color: "var(--claude-text)",
            }}
            onFocus={(e) => {
              (e.target as HTMLInputElement).style.borderColor = "var(--claude-accent)";
              (e.target as HTMLInputElement).style.boxShadow = "0 0 0 3px rgba(217, 119, 87, 0.12)";
            }}
            onBlur={(e) => {
              (e.target as HTMLInputElement).style.borderColor = "var(--claude-border)";
              (e.target as HTMLInputElement).style.boxShadow = "none";
            }}
            dir="rtl"
          />
          <button
            type="submit"
            disabled={loading || !inputText.trim()}
            className="btn-primary px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div
                className="w-5 h-5 border-2 border-t-transparent rounded-full animate-spin"
                style={{ borderColor: "rgba(255,255,255,0.4)", borderTopColor: "transparent" }}
              ></div>
            ) : (
              "إرسال"
            )}
          </button>
        </div>
        {inputText.length > 0 && (
          <p
            className="text-xs mt-1 text-left"
            style={{ color: inputText.length > 450 ? "var(--claude-accent-hover)" : "var(--claude-text-subtle)" }}
          >
            {inputText.length}/500
          </p>
        )}
      </form>
    </div>
  );
}
