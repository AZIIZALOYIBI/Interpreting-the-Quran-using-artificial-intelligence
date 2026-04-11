import Link from "next/link";

export default function Footer() {
  return (
    <footer className="relative mt-20">
      <div className="h-px bg-gradient-to-l from-transparent via-quran-gold/30 to-transparent" />
      <div className="bg-quran-dark/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-quran-gold to-yellow-600 flex items-center justify-center text-xl">📖</div>
                <h3 className="text-lg font-bold font-display gradient-text">حلول الحياة القرآنية</h3>
              </div>
              <p className="text-gray-400 text-sm leading-relaxed">منصة ذكية تساعدك في العثور على إرشادات قرآنية لأي موضوع في حياتك، باستخدام الذكاء الاصطناعي ومعالجة اللغة الطبيعية.</p>
            </div>
            <div className="space-y-4">
              <h4 className="text-quran-gold font-display font-bold">روابط سريعة</h4>
              <div className="space-y-2">
                {[{ href: "/ask", label: "اسأل القرآن" }, { href: "/quran-reader", label: "قارئ القرآن" }, { href: "/miracles", label: "معجزات علمية" }, { href: "/search", label: "البحث في القرآن" }].map((link) => (
                  <Link key={link.href} href={link.href} className="block text-gray-400 hover:text-quran-gold text-sm transition-colors">{link.label}</Link>
                ))}
              </div>
            </div>
            <div className="space-y-4">
              <h4 className="text-quran-gold font-display font-bold">تنبيه مهم</h4>
              <p className="text-gray-400 text-sm leading-relaxed">هذه المنصة مخصصة للإرشاد العام فقط، ولا تُغني عن الأحكام الشرعية المعتمدة من العلماء المؤهلين.</p>
            </div>
          </div>
          <div className="mt-10 pt-6 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-gray-500 text-sm">© {new Date().getFullYear()} حلول الحياة القرآنية. جميع الحقوق محفوظة.</p>
            <p className="text-gray-500 text-xs">﴿ إِنَّ هَٰذَا الْقُرْآنَ يَهْدِي لِلَّتِي هِيَ أَقْوَمُ ﴾</p>
          </div>
        </div>
      </div>
    </footer>
  );
}
