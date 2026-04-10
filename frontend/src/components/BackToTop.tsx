"use client";
import { useState, useEffect } from "react";

export default function BackToTop() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const handleScroll = () => setVisible(window.scrollY > 300);
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  if (!visible) return null;

  return (
    <button
      onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
      aria-label="العودة للأعلى"
      className="fixed bottom-6 left-6 z-50 w-12 h-12 rounded-full flex items-center justify-center text-white shadow-lg transition-all"
      style={{
        backgroundColor: "var(--claude-accent)",
        boxShadow: "0 4px 16px rgba(217, 119, 87, 0.45)",
      }}
      onMouseEnter={(e) => {
        (e.currentTarget as HTMLElement).style.backgroundColor = "var(--claude-accent-hover)";
        (e.currentTarget as HTMLElement).style.transform = "translateY(-2px)";
      }}
      onMouseLeave={(e) => {
        (e.currentTarget as HTMLElement).style.backgroundColor = "var(--claude-accent)";
        (e.currentTarget as HTMLElement).style.transform = "translateY(0)";
      }}
    >
      ↑
    </button>
  );
}
