"use client";
import { useState } from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

type TabKey = "morning" | "evening" | "general";

interface ZikrItem {
  id: number;
  text: string;
  surah: string;
  ref: string;
  count: string;
}

const MORNING_AZKAR: ZikrItem[] = [
  {
    id: 1,
    text: "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ",
    surah: "البقرة",
    ref: "البقرة: 201",
    count: "3× صباحاً",
  },
  {
    id: 2,
    text: "رَبِّ زِدْنِي عِلْمًا",
    surah: "طه",
    ref: "طه: 114",
    count: "7× صباحاً",
  },
  {
    id: 3,
    text: "حَسْبِيَ اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ",
    surah: "التوبة",
    ref: "التوبة: 129",
    count: "7× صباحاً",
  },
];

const EVENING_AZKAR: ZikrItem[] = [
  {
    id: 4,
    text: "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ",
    surah: "البقرة",
    ref: "البقرة: 255 — آية الكرسي",
    count: "1× مساءً",
  },
  {
    id: 5,
    text: "آمَنَ الرَّسُولُ بِمَا أُنزِلَ إِلَيْهِ مِن رَّبِّهِ وَالْمُؤْمِنُونَ ۚ كُلٌّ آمَنَ بِاللَّهِ وَمَلَائِكَتِهِ وَكُتُبِهِ وَرُسُلِهِ",
    surah: "البقرة",
    ref: "البقرة: 285-286",
    count: "1× مساءً",
  },
  {
    id: 6,
    text: "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ ۝ مِن شَرِّ مَا خَلَقَ",
    surah: "الفلق",
    ref: "الفلق: 1-2",
    count: "3× مساءً",
  },
];

const GENERAL_DUAS: ZikrItem[] = [
  {
    id: 7,
    text: "رَبِّ اشْرَحْ لِي صَدْرِي ۝ وَيَسِّرْ لِي أَمْرِي",
    surah: "طه",
    ref: "طه: 25-26",
    count: "دعاء عام",
  },
  {
    id: 8,
    text: "رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا وَهَبْ لَنَا مِن لَّدُنكَ رَحْمَةً",
    surah: "آل عمران",
    ref: "آل عمران: 8",
    count: "دعاء عام",
  },
  {
    id: 9,
    text: "رَبِّ إِنِّي لِمَا أَنزَلْتَ إِلَيَّ مِنْ خَيْرٍ فَقِيرٌ",
    surah: "القصص",
    ref: "القصص: 24",
    count: "دعاء عام",
  },
];

const TABS: { key: TabKey; label: string; icon: string }[] = [
  { key: "morning", label: "أذكار الصباح", icon: "🌅" },
  { key: "evening", label: "أذكار المساء", icon: "🌙" },
  { key: "general", label: "أدعية قرآنية", icon: "🤲" },
];

const TAB_DATA: Record<TabKey, ZikrItem[]> = {
  morning: MORNING_AZKAR,
  evening: EVENING_AZKAR,
  general: GENERAL_DUAS,
};

function ZikrCard({ item }: { item: ZikrItem }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(`${item.text}\n— ${item.ref}`).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div
      className="card relative"
      style={{ borderRight: "4px solid var(--claude-accent)" }}
    >
      {/* Count badge */}
      <span
        className="absolute top-4 left-4 text-xs font-semibold px-2 py-1 rounded-full"
        style={{
          backgroundColor: "var(--claude-accent-light)",
          color: "var(--claude-accent-hover)",
        }}
      >
        {item.count}
      </span>

      {/* Arabic text */}
      <p
        className="quran-font leading-loose mb-5 text-right mt-8"
        style={{ fontSize: "1.4rem", color: "var(--claude-text)" }}
      >
        {item.text}
      </p>

      {/* Footer */}
      <div
        className="flex items-center justify-between pt-3 border-t"
        style={{ borderColor: "var(--claude-border)" }}
      >
        <span className="text-sm font-semibold" style={{ color: "var(--claude-gold)" }}>
          {item.ref}
        </span>
        <button
          onClick={handleCopy}
          className="text-xs px-3 py-1.5 rounded-lg transition-all flex items-center gap-1"
          style={{
            backgroundColor: copied ? "var(--claude-accent-light)" : "var(--claude-surface)",
            color: copied ? "var(--claude-accent-hover)" : "var(--claude-text-muted)",
            border: "1px solid var(--claude-border)",
          }}
        >
          {copied ? "✓ تم النسخ" : "📋 نسخ"}
        </button>
      </div>
    </div>
  );
}

export default function AzkarPage() {
  const [activeTab, setActiveTab] = useState<TabKey>("morning");
  const items = TAB_DATA[activeTab];

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--claude-bg)" }}>
      <Header />

      {/* Hero */}
      <div
        className="py-14 px-4 text-center relative overflow-hidden"
        style={{ backgroundColor: "var(--claude-dark)" }}
      >
        <div
          className="absolute inset-0 opacity-5"
          style={{
            backgroundImage:
              "radial-gradient(circle at 30% 50%, var(--claude-accent) 0%, transparent 60%)",
          }}
        />
        <div className="relative">
          <div
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-medium mb-5"
            style={{
              backgroundColor: "rgba(217, 119, 87, 0.15)",
              border: "1px solid rgba(217, 119, 87, 0.3)",
              color: "var(--claude-accent-muted)",
            }}
          >
            <span>🤲</span> من القرآن الكريم
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            الأذكار والأدعية
            <br />
            <span style={{ color: "var(--claude-accent)" }}>القرآنية المأثورة</span>
          </h1>
          <p className="text-base max-w-xl mx-auto" style={{ color: "var(--claude-text-muted)" }}>
            أذكار الصباح والمساء والأدعية القرآنية لتحصين يومك وتقوية صلتك بالله
          </p>
        </div>
      </div>

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-10">
        {/* Tabs */}
        <div className="flex flex-wrap gap-3 justify-center mb-10">
          {TABS.map((tab) => {
            const isActive = tab.key === activeTab;
            return (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className="px-6 py-2.5 rounded-full text-sm font-semibold transition-all flex items-center gap-2"
                style={
                  isActive
                    ? {
                        backgroundColor: "var(--claude-accent)",
                        color: "white",
                        boxShadow: "0 2px 8px rgba(217, 119, 87, 0.35)",
                      }
                    : {
                        backgroundColor: "white",
                        color: "var(--claude-text-secondary)",
                        border: "1px solid var(--claude-border)",
                      }
                }
              >
                <span>{tab.icon}</span>
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Cards */}
        <div className="space-y-6">
          {items.map((item) => (
            <ZikrCard key={item.id} item={item} />
          ))}
        </div>

        {/* Disclaimer */}
        <div
          className="mt-12 rounded-xl p-6 text-center"
          style={{
            backgroundColor: "var(--claude-gold-light)",
            border: "1px solid var(--claude-gold-border)",
          }}
        >
          <p className="text-sm" style={{ color: "var(--claude-gold)" }}>
            ⚠️ الأذكار والأدعية المعروضة مستقاة من القرآن الكريم. يُنصح بالرجوع لأهل العلم للتثبت من الأدعية السنية.
          </p>
        </div>
      </main>

      <Footer />
    </div>
  );
}
