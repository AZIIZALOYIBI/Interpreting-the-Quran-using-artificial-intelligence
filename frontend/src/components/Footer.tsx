import Link from "next/link";

export default function Footer() {
  return (
    <footer
      className="py-10 px-4 text-center text-sm"
      style={{
        backgroundColor: "#1A1614",
        borderTop: "1px solid var(--claude-dark-3)",
        color: "var(--claude-text-subtle)",
      }}
    >
      <div className="max-w-4xl mx-auto space-y-4">
        {/* Nav links */}
        <div className="flex flex-wrap justify-center gap-x-6 gap-y-2" style={{ color: "var(--claude-text-muted)" }}>
          <Link href="/" className="hover:underline transition-colors" style={{ color: "var(--claude-text-muted)" }}>
            الرئيسية
          </Link>
          <Link href="/ask" className="hover:underline transition-colors" style={{ color: "var(--claude-text-muted)" }}>
            اسأل القرآن
          </Link>
          <Link href="/reader" className="hover:underline transition-colors" style={{ color: "var(--claude-text-muted)" }}>
            القرآن الكريم
          </Link>
          <Link href="/miracles" className="hover:underline transition-colors" style={{ color: "var(--claude-text-muted)" }}>
            الإعجاز العلمي
          </Link>
        </div>

        <div className="w-16 mx-auto border-t" style={{ borderColor: "var(--claude-dark-3)" }} />

        <p>
          ⚠️{" "}
          <strong style={{ color: "var(--claude-text-muted)" }}>تنبيه:</strong>{" "}
          هذه المنصة للتوجيه العام فقط وليست بديلاً عن الفتاوى الشرعية المعتمدة
        </p>

        <p>
          تصميم وتطوير:{" "}
          <span className="font-semibold" style={{ color: "var(--claude-accent)" }}>
            عبدالعزيز بن سلطان العتيبي
          </span>
        </p>
        <p>© 2026 حلول الحياة من القرآن الكريم | جميع الحقوق محفوظة</p>
      </div>
    </footer>
  );
}
