import type { ScientificMiracle } from "@/types";

interface ScientificMiracleCardProps {
  miracle: ScientificMiracle;
}

export default function ScientificMiracleCard({ miracle }: ScientificMiracleCardProps) {
  return (
    <div
      className="card flex flex-col"
      style={{ borderRight: "3px solid var(--claude-accent)" }}
    >
      <div className="flex items-start justify-between gap-4 mb-4">
        <h3 className="text-lg font-bold" style={{ color: "var(--claude-text)" }}>
          {miracle.titleAr}
        </h3>
        <span
          className="text-xs px-2 py-1 rounded-full whitespace-nowrap flex-shrink-0"
          style={{
            backgroundColor: "var(--claude-accent-light)",
            color: "var(--claude-accent-hover)",
          }}
        >
          {miracle.category}
        </span>
      </div>

      {/* Ayah */}
      <div className="ayah-card mb-4">
        <p className="quran-font mb-3" style={{ color: "var(--claude-text)" }}>
          {miracle.ayah}
        </p>
        <div className="flex items-center justify-between text-sm border-t pt-2" style={{ borderColor: "var(--claude-gold-border)" }}>
          <span className="font-semibold" style={{ color: "var(--claude-gold)" }}>
            {miracle.surahName}
          </span>
          <span style={{ color: "var(--claude-text-muted)" }}>{miracle.ayahRef}</span>
        </div>
      </div>

      {/* Scientific fact */}
      <div
        className="rounded-xl p-4 mt-auto"
        style={{
          backgroundColor: "var(--claude-surface)",
          border: "1px solid var(--claude-border)",
        }}
      >
        <div className="flex items-center gap-2 mb-2">
          <span>🔬</span>
          <span className="font-semibold text-sm" style={{ color: "var(--claude-text)" }}>
            الحقيقة العلمية
          </span>
        </div>
        <p className="text-sm leading-relaxed" style={{ color: "var(--claude-text-secondary)" }}>
          {miracle.scientificFact}
        </p>
      </div>
    </div>
  );
}
