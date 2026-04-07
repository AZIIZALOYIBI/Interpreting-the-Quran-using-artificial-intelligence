/**
 * Offline fallback page — displayed by the service worker (or Next.js)
 * when the user has no network connection.
 */
export default function OfflinePage() {
  return (
    <div
      dir="rtl"
      className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-8 text-center"
    >
      <div className="max-w-md w-full bg-white rounded-2xl shadow-lg p-8">
        {/* Icon */}
        <div className="text-6xl mb-6">📶</div>

        {/* Title */}
        <h1 className="text-2xl font-bold text-gray-900 mb-3">
          لا يوجد اتصال بالإنترنت
        </h1>

        {/* Description */}
        <p className="text-gray-600 mb-2 leading-relaxed">
          يبدو أنك غير متصل بالإنترنت حالياً. يرجى التحقق من اتصالك والمحاولة
          مجدداً.
        </p>

        {/* Quran verse for comfort */}
        <div className="my-6 p-4 bg-emerald-50 border border-emerald-200 rounded-xl">
          <p className="text-emerald-800 font-semibold text-lg leading-loose mb-1">
            ﴿وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ﴾
          </p>
          <p className="text-emerald-600 text-sm">سورة الطلاق: 3</p>
        </div>

        {/* Retry button */}
        <button
          onClick={() => window.location.reload()}
          className="w-full py-3 px-6 bg-emerald-700 hover:bg-emerald-800 text-white font-medium rounded-xl transition-colors"
        >
          إعادة المحاولة
        </button>

        {/* Tip */}
        <p className="text-gray-400 text-xs mt-4">
          تأكد من تفعيل الواي فاي أو بيانات الجوال ثم اضغط إعادة المحاولة
        </p>
      </div>
    </div>
  );
}
