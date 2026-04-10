"use client";
import { useState } from "react";
import ScientificMiracleCard from "@/components/ScientificMiracleCard";
import type { ScientificMiracle } from "@/types";

const ALL_CATEGORIES = [
  "الكل",
  "علم الفلك",
  "علم الأجنة",
  "علوم البحار",
  "علم الجيولوجيا",
  "علم الأحياء",
  "علم الأرصاد",
  "علم الفيزياء الفلكية",
  "علم الفيزياء",
  "علم الكيمياء الحيوية",
  "علم البصريات",
  "علم النبات",
  "علم الأعصاب",
];

interface MiraclesFilterProps {
  miracles: ScientificMiracle[];
}

export default function MiraclesFilter({ miracles }: MiraclesFilterProps) {
  const [activeCategory, setActiveCategory] = useState("الكل");

  const filtered = activeCategory === "الكل"
    ? miracles
    : miracles.filter((m) => m.category === activeCategory);

  const getCount = (cat: string) =>
    cat === "الكل" ? miracles.length : miracles.filter((m) => m.category === cat).length;

  return (
    <>
      {/* Category filter */}
      <div className="flex flex-wrap gap-3 justify-center mb-10">
        {ALL_CATEGORIES.map((cat) => {
          const isActive = cat === activeCategory;
          const count = getCount(cat);
          if (count === 0) return null;
          return (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className="px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center gap-2"
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
              {cat}
              <span
                className="text-xs px-1.5 py-0.5 rounded-full font-semibold"
                style={{
                  backgroundColor: isActive ? "rgba(255,255,255,0.25)" : "var(--claude-surface-2)",
                  color: isActive ? "white" : "var(--claude-text-muted)",
                }}
              >
                {count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Miracles grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {filtered.map((miracle) => (
          <ScientificMiracleCard key={miracle.id} miracle={miracle} />
        ))}
      </div>
    </>
  );
}
