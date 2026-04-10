"use client";
import Link from "next/link";
import { useState } from "react";
import { usePathname } from "next/navigation";

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const pathname = usePathname();

  const navLinks = [
    { href: "/", label: "الرئيسية" },
    { href: "/ask", label: "اسأل القرآن" },
    { href: "/reader", label: "القرآن الكريم" },
    { href: "/miracles", label: "الإعجاز العلمي" },
    { href: "/azkar", label: "الأذكار" },
    { href: "/categories/medicine", label: "التصنيفات" },
  ];

  const isActive = (href: string) => {
    if (href === "/") return pathname === "/";
    return pathname.startsWith(href);
  };

  return (
    <header
      className="sticky top-0 z-50 shadow-md"
      style={{ backgroundColor: "var(--claude-dark)", borderBottom: "1px solid var(--claude-dark-2)" }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 group">
            <div
              className="w-10 h-10 rounded-xl flex items-center justify-center text-xl font-bold shadow-sm"
              style={{ backgroundColor: "var(--claude-accent)", color: "white" }}
            >
              ق
            </div>
            <div>
              <div className="font-bold text-base leading-tight text-white">حلول الحياة</div>
              <div className="text-xs" style={{ color: "var(--claude-text-subtle)" }}>
                من القرآن الكريم بالذكاء الاصطناعي
              </div>
            </div>
          </Link>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => {
              const active = isActive(link.href);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className="px-3 py-2 rounded-lg text-sm font-medium transition-colors"
                  style={{
                    color: active ? "var(--claude-accent)" : "var(--claude-text-subtle)",
                    backgroundColor: active ? "var(--claude-dark-3)" : "transparent",
                  }}
                  onMouseEnter={(e) => {
                    if (!active) {
                      (e.target as HTMLElement).style.color = "white";
                      (e.target as HTMLElement).style.backgroundColor = "var(--claude-dark-3)";
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (!active) {
                      (e.target as HTMLElement).style.color = "var(--claude-text-subtle)";
                      (e.target as HTMLElement).style.backgroundColor = "transparent";
                    }
                  }}
                >
                  {link.label}
                </Link>
              );
            })}
          </nav>

          {/* Ask button */}
          <Link
            href="/ask"
            className="hidden md:inline-flex items-center gap-2 font-bold py-2 px-5 rounded-lg transition-all text-sm shadow-sm"
            style={{
              backgroundColor: "var(--claude-accent)",
              color: "white",
            }}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLElement).style.backgroundColor = "var(--claude-accent-hover)";
              (e.currentTarget as HTMLElement).style.boxShadow = "0 4px 12px rgba(217, 119, 87, 0.4)";
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLElement).style.backgroundColor = "var(--claude-accent)";
              (e.currentTarget as HTMLElement).style.boxShadow = "";
            }}
          >
            <span>💬</span>
            <span>اسأل الآن</span>
          </Link>

          {/* Mobile menu toggle */}
          <button
            className="md:hidden p-2 rounded-lg transition-colors"
            style={{ color: "var(--claude-text-subtle)" }}
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="القائمة"
          >
            <span className="text-xl">{menuOpen ? "✕" : "☰"}</span>
          </button>
        </div>

        {/* Mobile nav */}
        {menuOpen && (
          <nav
            className="md:hidden py-3 border-t"
            style={{ borderColor: "var(--claude-dark-3)" }}
          >
            {navLinks.map((link) => {
              const active = isActive(link.href);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className="block px-3 py-2.5 text-sm rounded-lg transition-colors"
                  style={{
                    color: active ? "var(--claude-accent)" : "var(--claude-text-subtle)",
                    backgroundColor: active ? "var(--claude-dark-3)" : "transparent",
                  }}
                  onClick={() => setMenuOpen(false)}
                >
                  {link.label}
                </Link>
              );
            })}
            <div className="mt-3 pt-3" style={{ borderTop: "1px solid var(--claude-dark-3)" }}>
              <Link
                href="/ask"
                className="block text-center font-bold py-2.5 px-4 rounded-lg text-sm"
                style={{ backgroundColor: "var(--claude-accent)", color: "white" }}
                onClick={() => setMenuOpen(false)}
              >
                💬 اسأل الآن
              </Link>
            </div>
          </nav>
        )}
      </div>
    </header>
  );
}

