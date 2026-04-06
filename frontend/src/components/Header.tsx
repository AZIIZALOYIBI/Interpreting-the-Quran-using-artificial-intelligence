"use client";
import Link from "next/link";
import { useState } from "react";

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  const navLinks = [
    { href: "/", label: "الرئيسية" },
    { href: "/ask", label: "اسأل القرآن" },
    { href: "/reader", label: "القرآن الكريم" },
    { href: "/miracles", label: "الإعجاز العلمي" },
    { href: "/categories/medicine", label: "التصنيفات" },
  ];

  return (
    <header className="bg-emerald-800 text-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3">
            <span className="text-3xl">📖</span>
            <div>
              <div className="font-bold text-lg leading-tight">حلول الحياة</div>
              <div className="text-emerald-200 text-xs">من القرآن الكريم بالذكاء الاصطناعي</div>
            </div>
          </Link>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-6">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-emerald-100 hover:text-white hover:underline transition-colors text-sm font-medium"
              >
                {link.label}
              </Link>
            ))}
          </nav>

          {/* Ask button */}
          <Link
            href="/ask"
            className="hidden md:inline-flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-white font-bold py-2 px-4 rounded-lg transition-colors text-sm"
          >
            <span>💬</span>
            <span>اسأل الآن</span>
          </Link>

          {/* Mobile menu toggle */}
          <button
            className="md:hidden p-2 rounded-lg hover:bg-emerald-700"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="القائمة"
          >
            <span className="text-xl">{menuOpen ? "✕" : "☰"}</span>
          </button>
        </div>

        {/* Mobile nav */}
        {menuOpen && (
          <nav className="md:hidden py-4 border-t border-emerald-700">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="block py-2 text-emerald-100 hover:text-white"
                onClick={() => setMenuOpen(false)}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        )}
      </div>
    </header>
  );
}
