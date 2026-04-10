import Header from "@/components/Header";
import Footer from "@/components/Footer";
import MiraclesFilter from "@/components/MiraclesFilter";
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
  {
    id: 7,
    titleAr: "تكوين الغيوم والمطر",
    titleEn: "Formation of Clouds and Rain",
    ayah: "وَأَنزَلْنَا مِنَ السَّمَاءِ مَاءً بِقَدَرٍ",
    surahName: "سورة المؤمنون",
    ayahRef: "المؤمنون: 18",
    scientificFact: "وصف القرآن دورة الماء في الطبيعة بدقة علمية قبل اكتشاف علم الأرصاد الجوي الحديث.",
    category: "علم الأرصاد",
  },
  {
    id: 8,
    titleAr: "الحديد من الفضاء",
    titleEn: "Iron Sent from Space",
    ayah: "وَأَنزَلْنَا الْحَدِيدَ فِيهِ بَأْسٌ شَدِيدٌ وَمَنَافِعُ لِلنَّاسِ",
    surahName: "سورة الحديد",
    ayahRef: "الحديد: 25",
    scientificFact: "أثبت العلماء أن عنصر الحديد لم ينشأ على الأرض بل جاء من الفضاء الخارجي عبر النيازك.",
    category: "علم الفيزياء الفلكية",
  },
  {
    id: 9,
    titleAr: "الحاجز بين الليل والنهار",
    titleEn: "Day and Night Cycle",
    ayah: "وَجَعَلَ اللَّيْلَ سَكَنًا وَالشَّمْسَ وَالْقَمَرَ حُسْبَانًا",
    surahName: "سورة الأنعام",
    ayahRef: "الأنعام: 96",
    scientificFact: "دورة الليل والنهار الدقيقة التي تجعل الحياة ممكنة على الأرض.",
    category: "علم الفلك",
  },
  {
    id: 10,
    titleAr: "خلق الإنسان من تراب",
    titleEn: "Human Creation from Clay",
    ayah: "وَلَقَدْ خَلَقْنَا الْإِنسَانَ مِن سُلَالَةٍ مِّن طِينٍ",
    surahName: "سورة المؤمنون",
    ayahRef: "المؤمنون: 12",
    scientificFact: "أثبت العلم أن جسم الإنسان يحتوي على نفس العناصر الكيميائية الموجودة في التراب.",
    category: "علم الكيمياء الحيوية",
  },
  {
    id: 11,
    titleAr: "الجاذبية والسماء المحفوظة",
    titleEn: "The Protected Sky",
    ayah: "وَجَعَلْنَا السَّمَاءَ سَقْفًا مَّحْفُوظًا",
    surahName: "سورة الأنبياء",
    ayahRef: "الأنبياء: 32",
    scientificFact: "الغلاف الجوي والمجال المغناطيسي يحميان الأرض من الأشعة الكونية والنيازك.",
    category: "علم الفيزياء",
  },
  {
    id: 12,
    titleAr: "الضوء والظلام",
    titleEn: "Light and Darkness",
    ayah: "وَجَعَلَ الظُّلُمَاتِ وَالنُّورَ",
    surahName: "سورة الأنعام",
    ayahRef: "الأنعام: 1",
    scientificFact: "اكتشف العلم أن الظلام هو غياب الضوء وليس شيئاً مستقلاً كما أشارت إليه الآية.",
    category: "علم البصريات",
  },
  {
    id: 13,
    titleAr: "تكوين الجبال",
    titleEn: "Mountain Formation",
    ayah: "وَأَلْقَىٰ فِي الْأَرْضِ رَوَاسِيَ أَن تَمِيدَ بِكُمْ",
    surahName: "سورة النحل",
    ayahRef: "النحل: 15",
    scientificFact: "أثبت العلم أن الجبال تعمل كأوتاد تثبت القشرة الأرضية وتمنع اهتزاز الأرض.",
    category: "علم الجيولوجيا",
  },
  {
    id: 14,
    titleAr: "التخصيب بالرياح",
    titleEn: "Wind Pollination",
    ayah: "وَأَرْسَلْنَا الرِّيَاحَ لَوَاقِحَ",
    surahName: "سورة الحجر",
    ayahRef: "الحجر: 22",
    scientificFact: "اكتشف العلماء أن الرياح تلعب دوراً محورياً في تلقيح النباتات.",
    category: "علم النبات",
  },
  {
    id: 15,
    titleAr: "النوم كموت صغير",
    titleEn: "Sleep as Minor Death",
    ayah: "اللَّهُ يَتَوَفَّى الْأَنفُسَ حِينَ مَوْتِهَا وَالَّتِي لَمْ تَمُتْ فِي مَنَامِهَا",
    surahName: "سورة الزمر",
    ayahRef: "الزمر: 42",
    scientificFact: "أثبت علم الأعصاب أن أثناء النوم العميق تنخفض وظائف الجسم الحيوية بشكل مشابه للموت.",
    category: "علم الأعصاب",
  },
];

export default function MiraclesPage() {
  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--claude-bg)" }}>
      <Header />

      {/* Page hero */}
      <div
        className="py-14 px-4 text-center relative overflow-hidden"
        style={{ backgroundColor: "var(--claude-dark)" }}
      >
        <div
          className="absolute inset-0 opacity-5"
          style={{
            backgroundImage:
              "radial-gradient(circle at 30% 50%, var(--claude-accent) 0%, transparent 60%), radial-gradient(circle at 70% 20%, #8B5CF6 0%, transparent 50%)",
          }}
        />
        <div className="relative">
          <div
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-medium mb-5"
            style={{
              backgroundColor: "rgba(217, 119, 87, 0.15)",
              border: "1px solid rgba(217, 119, 87, 0.3)",
              color: "var(--claude-accent-muted)",
            }}
          >
            <span>🔬</span> إعجاز قرآني علمي
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            الإعجاز العلمي
            <br />
            <span style={{ color: "var(--claude-accent)" }}>في القرآن الكريم</span>
          </h1>
          <p className="text-base max-w-2xl mx-auto" style={{ color: "var(--claude-text-muted)" }}>
            اكتشف كيف أشارت آيات القرآن الكريم إلى حقائق علمية أثبتها العلم الحديث بعد قرون
          </p>
        </div>
      </div>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-10">
        {/* Interactive filter + grid (client component) */}
        <MiraclesFilter miracles={MIRACLES} />

        {/* Disclaimer */}
        <div
          className="mt-12 rounded-xl p-6 text-center"
          style={{
            backgroundColor: "var(--claude-gold-light)",
            border: "1px solid var(--claude-gold-border)",
          }}
        >
          <p className="text-sm" style={{ color: "var(--claude-gold)" }}>
            ⚠️ المعلومات المعروضة مستقاة من مصادر علمية وتفسيرية موثوقة. يُنصح بالرجوع إلى المصادر الأصلية للتعمق في الموضوع.
          </p>
        </div>
      </main>

      <Footer />
    </div>
  );
}

