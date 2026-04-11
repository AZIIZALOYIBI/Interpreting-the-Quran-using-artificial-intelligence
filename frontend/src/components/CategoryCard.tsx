"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Category } from "@/types";

interface CategoryCardProps {
  category: Category;
  index: number;
}

export default function CategoryCard({ category, index }: CategoryCardProps) {
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.1 }} viewport={{ once: true }}>
      <Link href={`/ask?category=${category.id}`} className="block group">
        <div className="relative glass rounded-2xl p-6 border border-white/5 card-hover overflow-hidden">
          <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl" style={{ background: `radial-gradient(circle at center, ${category.color}15, transparent 70%)` }} />
          <div className="relative z-10">
            <div className="w-14 h-14 rounded-xl flex items-center justify-center text-2xl mb-4 transition-transform group-hover:scale-110" style={{ background: `linear-gradient(135deg, ${category.color}20, ${category.color}10)`, border: `1px solid ${category.color}30` }}>
              {category.icon}
            </div>
            <h3 className="text-lg font-bold font-display text-white mb-2 group-hover:text-quran-gold transition-colors">{category.name}</h3>
            <p className="text-sm text-gray-400 leading-relaxed mb-4">{category.description}</p>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">{category.verse_count}+ آية ذات صلة</span>
              <span className="text-xs font-bold opacity-0 group-hover:opacity-100 transition-opacity" style={{ color: category.color }}>استكشف ←</span>
            </div>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
