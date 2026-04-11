"use client";
import { useState, useEffect } from "react";
import type { Tafsir, Ayah } from "@/types";

interface TafsirPanelProps {
  ayah: Ayah | null;
  onClose: () => void;
}

const MOCK_TAFSIR: Tafsir[] = [
  {
    id: 1,
    ayahId: 1,
    scholarName: "Ibn Kathir",
    scholarNameAr: "ابن كثير",
    text: "يُبيِّن الله سبحانه في هذه الآية الكريمة عظيم فضله ورحمته بعباده، وإحاطة علمه بأحوالهم.",
    source: "تفسير القرآن العظيم",
  },
  {
    id: 2,
    ayahId: 1,
    scholarName: "Al-Tabari",
    scholarNameAr: "الطبري",
    text: "قال الطبري رحمه الله: يعني بذلك جلَّ ثناؤه الإخبار عن صفاته الجليلة وأسمائه الحسنى.",
    source: "جامع البيان في تأويل القرآن",
  },
  {
    id: 3,
    ayahId: 1,
    scholarName: "Al-Qurtubi",
    scholarNameAr: "القرطبي",
    text: "استنبط القرطبي من هذه الآية أحكاماً فقهية عديدة تتعلق بمعاملات الناس وعلاقاتهم.",
    source: "الجامع لأحكام القرآن",
  },
];

export default function TafsirPanel({ ayah, onClose }: TafsirPanelProps) {
  const [tafsirList, setTafsirList] = useState<Tafsir[]>(MOCK_TAFSIR);
  const [activeScholar, setActiveScholar] = useState<string>("ابن كثير");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!ayah) return;

    let isMounted = true;

    const startTimer = setTimeout(() => {
      if (isMounted) setLoading(true);
    }, 0);

    const timer = setTimeout(() => {
      if (isMounted) {
        setTafsirList(MOCK_TAFSIR);
        setLoading(false);
      }
    }, 500);

    return () => {
      isMounted = false;
      clearTimeout(startTimer);
      clearTimeout(timer);
    };
  }, [ayah]);

  if (!ayah) return null;

  const activeTafsir = tafsirList.find((t) => t.scholarNameAr === activeScholar) || tafsirList[0];

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="bg-emerald-800 text-white p-4 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold">التفسير</h2>
            <p className="text-emerald-200 text-sm">
              سورة {ayah.surah_name_ar} - الآية {ayah.ayah_number}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-emerald-700 rounded-lg transition-colors"
            aria-label="إغلاق"
          >
            ✕
          </button>
        </div>

        {/* Ayah text */}
        <div className="ayah-card mx-4 mt-4">
          <p className="quran-font text-gray-800">{ayah.text_uthmani}</p>
        </div>

        {/* Scholar tabs */}
        <div className="flex gap-2 px-4 pt-4 overflow-x-auto">
          {tafsirList.map((t) => (
            <button
              key={t.scholarNameAr}
              onClick={() => setActiveScholar(t.scholarNameAr)}
              className={`whitespace-nowrap px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeScholar === t.scholarNameAr
                  ? "bg-emerald-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {t.scholarNameAr}
            </button>
          ))}
        </div>

        {/* Tafsir content */}
        <div className="flex-1 overflow-y-auto p-4">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full"></div>
            </div>
          ) : activeTafsir ? (
            <div>
              <div className="flex items-center gap-2 mb-3">
                <span className="text-emerald-700 font-bold">{activeTafsir.scholarNameAr}</span>
                <span className="text-gray-400">•</span>
                <span className="text-gray-500 text-sm">{activeTafsir.source}</span>
              </div>
              <p className="text-gray-700 leading-relaxed text-lg">{activeTafsir.text}</p>
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">لا يوجد تفسير متاح</p>
          )}
        </div>
      </div>
    </div>
  );
}