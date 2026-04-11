"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";

const navLinks = [
  { href: "/", label: "الرئيسية", icon: "🏠" },
  { href: "/ask", label: "اسأل القرآن", icon: "🤖" },
  { href: "/quran-reader", label: "قارئ القرآن", icon: "📖" },
  { href: "/miracles", label: "معجزات علمية", icon: "🔬" },
  { href: "/search", label: "البحث", icon: "🔍" },
  { href: "/tafsir", label: "التفسير", icon: "📝" },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav className={`fixed top-0 right-0 left-0 z-50 transition-all duration-300 ${scrolled ? "glass-dark shadow-lg shadow-black/20" : "bg-transparent"}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-quran-gold to-yellow-600 flex items-center justify-center text-xl shadow-lg group-hover:scale-110 transition-transform">📖</div>
            <div className="hidden sm:block">
              <h1 className="text-lg font-bold font-display gradient-text">حلول الحياة القرآنية</h1>
              <p className="text-[10px] text-gray-400 -mt-1">AI-Powered Quranic Guidance</p>
            </div>
          </Link>
          <div className="hidden lg:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link key={link.href} href={link.href}
                className={`relative px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-2 ${pathname === link.href ? "text-quran-gold bg-quran-gold/10" : "text-gray-300 hover:text-white hover:bg-white/5"}`}>
                <span className="text-base">{link.icon}</span>
                <span className="font-display">{link.label}</span>
                {pathname === link.href && (
                  <motion.div layoutId="activeTab" className="absolute bottom-0 right-2 left-2 h-0.5 bg-gradient-to-l from-quran-gold to-yellow-500 rounded-full" transition={{ type: "spring", stiffness: 300, damping: 30 }} />
                )}
              </Link>
            ))}
          </div>
          <button onClick={() => setIsOpen(!isOpen)} className="lg:hidden p-2 rounded-lg text-gray-300 hover:text-white hover:bg-white/10 transition-colors">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {isOpen ? <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /> : <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />}
            </svg>
          </button>
        </div>
      </div>
      <AnimatePresence>
        {isOpen && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} className="lg:hidden glass-dark border-t border-white/5">
            <div className="px-4 py-3 space-y-1">
              {navLinks.map((link) => (
                <Link key={link.href} href={link.href} onClick={() => setIsOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all ${pathname === link.href ? "text-quran-gold bg-quran-gold/10" : "text-gray-300 hover:text-white hover:bg-white/5"}`}>
                  <span className="text-lg">{link.icon}</span>
                  <span className="font-display">{link.label}</span>
                </Link>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
