import Header from "@/components/Header";
import ScientificMiracleCard from "@/components/ScientificMiracleCard";
import type { ScientificMiracle } from "@/types";

export const metadata = {
  title: "الإعجاز العلمي في القرآن الكريم",
};

const MIRACLES: ScientificMiracle[] = [
  {
    id: 1,
    titleAr: "توسع الكون",
    titleEn: "Expansion of the Universe",
    ayah: "وَالسَّمَاءَ بَنَيْنَاهَا بِأَيْدٍ وَإِنَّا لَمُوسِعُونَ",
    surahName: "سورة الذاريات",
    ayahRef: "الذاريات: 47",
    scientificFact: "اكتشف العلماء في القرن العشرين أن الكون يتوسع باستمرار، وهو ما أشارت إليه هذه الآية قبل 1400 عام.",
    category: "علم الفلك",
  },
  {
    id: 2,
    titleAr: "مراحل تكوين الجنين",
    titleEn: "Stages of Human Embryo Development",
    ayah: "ثُمَّ خَلَقْنَا النُّطْفَةَ عَلَقَةً فَخَلَقْنَا الْعَلَقَةَ مُضْغَةً فَخَلَقْنَا الْمُضْغَةَ عِظَامًا",
    surahName: "سورة المؤمنون",
    ayahRef: "المؤمنون: 14",
    scientificFact: "وصف القرآن مراحل تطور الجنين بدقة متناهية تتطابق مع ما توصل إليه علم الأجنة الحديث.",
    category: "علم الأجنة",
  },
  {
    id: 3,
    titleAr: "الحاجز بين البحرين",
    titleEn: "Barrier Between Two Seas",
    ayah: "مَرَجَ الْبَحْرَيْنِ يَلْتَقِيَانِ ۝ بَيْنَهُمَا بَرْزَخٌ لَّا يَبْغِيَانِ",
    surahName: "سورة الرحمن",
    ayahRef: "الرحمن: 19-20",
    scientificFact: "اكتشف العلماء وجود حواجز مائية تفصل بين البحار المختلطة مما يمنع اختلاط مياهها وملوحتها.",
    category: "علوم البحار",
  },
  {
    id: 4,
    titleAr: "تكون الجبال كالأوتاد",
    titleEn: "Mountains as Pegs",
    ayah: "أَلَمْ نَجْعَلِ الْأَرْضَ مِهَادًا ۝ وَالْجِبَالَ أَوْتَادًا",
    surahName: "سورة النبأ",
    ayahRef: "النبأ: 6-7",
    scientificFact: "أثبتت الدراسات الجيولوجية الحديثة أن الجبال لها جذور عميقة في الأرض كالأوتاد تثبت القشرة الأرضية.",
    category: "علم الجيولوجيا",
  },
  {
    id: 5,
    titleAr: "الماء أساس كل حياة",
    titleEn: "Water as Origin of Life",
    ayah: "وَجَعَلْنَا مِنَ الْمَاءِ كُلَّ شَيْءٍ حَيٍّ ۖ أَفَلَا يُؤْمِنُونَ",
    surahName: "سورة الأنبياء",
    ayahRef: "الأنبياء: 30",
    scientificFact: "أثبت علم الأحياء أن الماء هو الركيزة الأساسية لجميع أشكال الحياة على كوكب الأرض.",
    category: "علم الأحياء",
  },
  {
    id: 6,
    titleAr: "دوران الأجرام السماوية",
    titleEn: "Orbits of Celestial Bodies",
    ayah: "وَكُلٌّ فِي فَلَكٍ يَسْبَحُونَ",
    surahName: "سورة يس",
    ayahRef: "يس: 40",
    scientificFact: "أثبت علم الفلك الحديث أن الشمس والقمر وسائر الأجرام السماوية تسبح في مدارات محددة.",
    category: "علم الفلك",
  },
];

const CATEGORIES = ["الكل", "علم الفلك", "علم الأجنة", "علوم البحار", "علم الجيولوجيا", "علم الأحياء"];

export default function MiraclesPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Hero */}
        <div className="text-center mb-12">
          <div className="text-6xl mb-4">🔬</div>
          <h1 className="text-4xl font-bold text-gray-800 mb-4">الإعجاز العلمي في القرآن الكريم</h1>
          <p className="text-gray-500 max-w-2xl mx-auto text-lg">
            اكتشف كيف أشارت آيات القرآن الكريم إلى حقائق علمية أثبتها العلم الحديث بعد قرون
          </p>
        </div>

        {/* Category filter (static display) */}
        <div className="flex flex-wrap gap-3 justify-center mb-8">
          {CATEGORIES.map((cat) => (
            <span
              key={cat}
              className={`px-4 py-2 rounded-full text-sm font-medium cursor-pointer transition-colors ${
                cat === "الكل"
                  ? "bg-emerald-600 text-white"
                  : "bg-white text-gray-600 border border-gray-200 hover:border-emerald-300"
              }`}
            >
              {cat}
            </span>
          ))}
        </div>

        {/* Miracles grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {MIRACLES.map((miracle) => (
            <ScientificMiracleCard key={miracle.id} miracle={miracle} />
          ))}
        </div>

        {/* Disclaimer */}
        <div className="mt-12 bg-amber-50 border border-amber-200 rounded-xl p-6 text-center">
          <p className="text-amber-800 text-sm">
            ⚠️ المعلومات المعروضة مستقاة من مصادر علمية وتفسيرية موثوقة. يُنصح بالرجوع إلى المصادر الأصلية للتعمق في الموضوع.
          </p>
        </div>
      </main>
    </div>
  );
}
