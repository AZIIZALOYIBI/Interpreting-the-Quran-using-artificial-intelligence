"use client";
import { useState } from "react";
import ScientificMiracleCard from "@/components/ScientificMiracleCard";
import type { ScientificMiracle } from "@/types";

const ALL_CATEGORIES = ["الكل", "علم الفلك", "علم الأجنة", "علوم البحار", "علم الجيولوجيا", "علم الأحياء"];

interface MiraclesFilterProps {
  miracles: ScientificMiracle[];
}

export default function MiraclesFilter({ miracles }: MiraclesFilterProps) {
  const [activeCategory, setActiveCategory] = useState("الكل");

  const filtered = activeCategory === "الكل"
    ? miracles
    : miracles.filter((m) => m.category === activeCategory);

  return (
    <>
      {/* Category filter */}
      <div className="flex flex-wrap gap-3 justify-center mb-10">
        {ALL_CATEGORIES.map((cat) => {
          const isActive = cat === activeCategory;
          return (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className="px-5 py-2 rounded-full text-sm font-medium transition-all"
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
