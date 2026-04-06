import Link from "next/link";
import type { Category } from "@/types";

interface CategoryCardProps {
  category: Category;
}

export default function CategoryCard({ category }: CategoryCardProps) {
  return (
    <Link href={`/categories/${category.id}`}>
      <div className={`category-card h-full flex flex-col items-center text-center gap-4 ${category.bgColor}`}>
        <span className="text-4xl">{category.icon}</span>
        <h3 className={`text-xl font-bold ${category.textColor}`}>{category.nameAr}</h3>
        <p className="text-gray-600 text-sm leading-relaxed">{category.description}</p>
        <span className={`mt-auto text-xs font-semibold px-3 py-1 rounded-full ${category.color} text-white`}>
          استكشف →
        </span>
      </div>
    </Link>
  );
}
