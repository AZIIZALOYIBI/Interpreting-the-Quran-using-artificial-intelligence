import Header from "@/components/Header";
import Link from "next/link";

const CATEGORY_DATA: Record<string, {
  nameAr: string;
  icon: string;
  description: string;
  color: string;
  ayahs: Array<{ text: string; ref: string; tafsir: string }>;
}> = {
  medicine: {
    nameAr: "الطب والصحة",
    icon: "🏥",
    description: "الإرشاد القرآني في مجال الصحة والطب والعلاج",
    color: "green",
    ayahs: [
      {
        text: "وَإِذَا مَرِضْتُ فَهُوَ يَشْفِينِ",
        ref: "الشعراء: 80",
        tafsir: "في هذه الآية إشارة إلى أن الشفاء من الله وحده، وأن على المريض الأخذ بالأسباب والتوكل على الله.",
      },
      {
        text: "يَخْرُجُ مِن بُطُونِهَا شَرَابٌ مُّخْتَلِفٌ أَلْوَانُهُ فِيهِ شِفَاءٌ لِّلنَّاسِ",
        ref: "النحل: 69",
        tafsir: "ذكر القرآن الكريم العسل ووصفه بأنه شفاء للناس، وقد أثبت العلم الحديث خواصه الطبية المذهلة.",
      },
    ],
  },
  work: {
    nameAr: "العمل والمال",
    icon: "💼",
    description: "التوجيه القرآني في الكسب الحلال وإدارة المال",
    color: "blue",
    ayahs: [
      {
        text: "وَأَحَلَّ اللَّهُ الْبَيْعَ وَحَرَّمَ الرِّبَا",
        ref: "البقرة: 275",
        tafsir: "أحل الله البيع والتجارة المشروعة وحرم الربا لما فيه من ظلم وإضرار بالمجتمع.",
      },
      {
        text: "فَإِذَا قُضِيَتِ الصَّلَاةُ فَانتَشِرُوا فِي الْأَرْضِ وَابْتَغُوا مِن فَضْلِ اللَّهِ",
        ref: "الجمعة: 10",
        tafsir: "حث الإسلام على العمل والسعي في طلب الرزق بعد أداء الشعائر الدينية.",
      },
    ],
  },
  science: {
    nameAr: "العلوم والتكنولوجيا",
    icon: "🔬",
    description: "الإعجاز العلمي والحث على العلم والبحث",
    color: "purple",
    ayahs: [
      {
        text: "اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ",
        ref: "العلق: 1",
        tafsir: "كانت أولى الآيات نزولاً تحث على القراءة والعلم، مما يدل على مكانة العلم في الإسلام.",
      },
      {
        text: "قُلْ هَلْ يَسْتَوِي الَّذِينَ يَعْلَمُونَ وَالَّذِينَ لَا يَعْلَمُونَ",
        ref: "الزمر: 9",
        tafsir: "فرّق القرآن بين العالم والجاهل تفريقاً كبيراً، مما يدل على عظيم قيمة العلم.",
      },
    ],
  },
  family: {
    nameAr: "الأسرة والمجتمع",
    icon: "👨‍👩‍👧‍👦",
    description: "منظومة الأسرة والعلاقات الاجتماعية في الإسلام",
    color: "orange",
    ayahs: [
      {
        text: "وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا لِّتَسْكُنُوا إِلَيْهَا",
        ref: "الروم: 21",
        tafsir: "جعل الله الزواج آية من آياته ووصفه بالمودة والرحمة، وهو أساس الاستقرار الأسري.",
      },
      {
        text: "وَبِالْوَالِدَيْنِ إِحْسَانًا",
        ref: "البقرة: 83",
        tafsir: "قرن الله الإحسان إلى الوالدين بعبادته، مما يدل على عظيم حقهما.",
      },
    ],
  },
  self_development: {
    nameAr: "التطوير الذاتي",
    icon: "🧠",
    description: "بناء الشخصية وتحقيق النمو الروحي والعقلي",
    color: "yellow",
    ayahs: [
      {
        text: "إِنَّ اللَّهَ لَا يُغَيِّرُ مَا بِقَوْمٍ حَتَّىٰ يُغَيِّرُوا مَا بِأَنفُسِهِمْ",
        ref: "الرعد: 11",
        tafsir: "أرشدنا القرآن إلى أن التغيير يبدأ من النفس، وأن سنة الله تقتضي السعي والعمل.",
      },
      {
        text: "وَعَلَّمَ آدَمَ الْأَسْمَاءَ كُلَّهَا",
        ref: "البقرة: 31",
        tafsir: "أشارت الآية إلى أن الإنسان خُلق بقدرة على التعلم والمعرفة.",
      },
    ],
  },
  law: {
    nameAr: "القانون والعدالة",
    icon: "⚖️",
    description: "منظومة العدل والحقوق في الشريعة الإسلامية",
    color: "red",
    ayahs: [
      {
        text: "إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ وَالْإِحْسَانِ",
        ref: "النحل: 90",
        tafsir: "أمر الله بالعدل والإحسان في جميع شؤون الحياة، وهذا يشمل العدل في الحكم والقضاء والمعاملات.",
      },
      {
        text: "يَا أَيُّهَا الَّذِينَ آمَنُوا كُونُوا قَوَّامِينَ بِالْقِسْطِ",
        ref: "النساء: 135",
        tafsir: "أمر القرآن المؤمنين بإقامة القسط ولو على أنفسهم أو ذويهم.",
      },
    ],
  },
  environment: {
    nameAr: "البيئة والطبيعة",
    icon: "🌍",
    description: "الحفاظ على البيئة وعمارة الأرض",
    color: "teal",
    ayahs: [
      {
        text: "وَلَا تُفْسِدُوا فِي الْأَرْضِ بَعْدَ إِصْلَاحِهَا",
        ref: "الأعراف: 56",
        tafsir: "نهى القرآن عن الإفساد في الأرض بعد إصلاحها، وهو توجيه قرآني لحماية البيئة.",
      },
      {
        text: "وَهُوَ الَّذِي جَعَلَكُمْ خَلَائِفَ الْأَرْضِ",
        ref: "الأنعام: 165",
        tafsir: "جعل الله الإنسان خليفة في الأرض، مما يعني مسؤوليته عن الحفاظ عليها.",
      },
    ],
  },
};

const COLOR_CLASSES: Record<string, { bg: string; text: string; badge: string; border: string }> = {
  green: { bg: "bg-green-50", text: "text-green-800", badge: "bg-green-600", border: "border-green-200" },
  blue: { bg: "bg-blue-50", text: "text-blue-800", badge: "bg-blue-600", border: "border-blue-200" },
  purple: { bg: "bg-purple-50", text: "text-purple-800", badge: "bg-purple-600", border: "border-purple-200" },
  orange: { bg: "bg-orange-50", text: "text-orange-800", badge: "bg-orange-600", border: "border-orange-200" },
  yellow: { bg: "bg-yellow-50", text: "text-yellow-800", badge: "bg-yellow-600", border: "border-yellow-200" },
  red: { bg: "bg-red-50", text: "text-red-800", badge: "bg-red-600", border: "border-red-200" },
  teal: { bg: "bg-teal-50", text: "text-teal-800", badge: "bg-teal-600", border: "border-teal-200" },
  emerald: { bg: "bg-emerald-50", text: "text-emerald-800", badge: "bg-emerald-600", border: "border-emerald-200" },
};

export function generateStaticParams() {
  return Object.keys(CATEGORY_DATA).map((category) => ({ category }));
}

export default async function CategoryPage({
  params,
}: {
  params: Promise<{ category: string }>;
}) {
  const { category } = await params;
  const data = CATEGORY_DATA[category];

  if (!data) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="max-w-4xl mx-auto px-4 py-16 text-center">
          <div className="text-6xl mb-4">❓</div>
          <h1 className="text-3xl font-bold text-gray-800 mb-4">الصفحة غير موجودة</h1>
          <Link href="/" className="btn-primary">العودة للرئيسية</Link>
        </main>
      </div>
    );
  }

  const colors = COLOR_CLASSES[data.color] || COLOR_CLASSES.emerald;

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Breadcrumb */}
        <nav className="flex items-center gap-2 text-sm text-gray-500 mb-6">
          <Link href="/" className="hover:text-emerald-600">الرئيسية</Link>
          <span>←</span>
          <span className="text-gray-800">{data.nameAr}</span>
        </nav>

        {/* Header */}
        <div className={`${colors.bg} border ${colors.border} rounded-2xl p-8 text-center mb-8`}>
          <div className="text-6xl mb-4">{data.icon}</div>
          <h1 className={`text-3xl font-bold ${colors.text} mb-3`}>{data.nameAr}</h1>
          <p className="text-gray-600">{data.description}</p>
        </div>

        {/* Ayahs */}
        <div className="space-y-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-800">آيات ذات صلة</h2>
          {data.ayahs.map((ayah, i) => (
            <div key={i} className="card">
              <div className="ayah-card mb-4">
                <p className="quran-font text-gray-800 mb-3">{ayah.text}</p>
                <p className="text-amber-700 text-sm font-semibold text-left">{ayah.ref}</p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <p className="text-sm font-semibold text-emerald-700 mb-2">📝 التفسير:</p>
                <p className="text-gray-700 leading-relaxed">{ayah.tafsir}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Ask button */}
        <div className="text-center">
          <Link
            href={`/ask?category=${category}`}
            className="inline-flex items-center gap-2 btn-primary py-4 px-8 text-lg"
          >
            <span>💬</span>
            اسأل عن {data.nameAr}
          </Link>
        </div>
      </main>
    </div>
  );
}
