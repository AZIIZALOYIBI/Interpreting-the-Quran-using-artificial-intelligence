import type { ScientificMiracle } from "@/types";

interface ScientificMiracleCardProps {
  miracle: ScientificMiracle;
}

export default function ScientificMiracleCard({ miracle }: ScientificMiracleCardProps) {
  return (
    <div className="card border-r-4 border-emerald-500 hover:shadow-xl transition-shadow">
      <div className="flex items-start justify-between gap-4 mb-4">
        <h3 className="text-lg font-bold text-gray-800">{miracle.titleAr}</h3>
        <span className="text-xs bg-emerald-100 text-emerald-700 px-2 py-1 rounded-full whitespace-nowrap">
          {miracle.category}
        </span>
      </div>

      {/* Ayah */}
      <div className="ayah-card mb-4">
        <p className="quran-font text-gray-800 mb-3">{miracle.ayah}</p>
        <div className="flex items-center justify-between text-sm">
          <span className="text-amber-700 font-semibold">{miracle.surahName}</span>
          <span className="text-gray-500">{miracle.ayahRef}</span>
        </div>
      </div>

      {/* Scientific fact */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-blue-600">🔬</span>
          <span className="text-blue-700 font-semibold text-sm">الحقيقة العلمية</span>
        </div>
        <p className="text-gray-700 text-sm leading-relaxed">{miracle.scientificFact}</p>
      </div>
    </div>
  );
}
