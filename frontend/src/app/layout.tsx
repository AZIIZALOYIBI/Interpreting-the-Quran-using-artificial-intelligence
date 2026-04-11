import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Toaster } from "react-hot-toast";

export const metadata: Metadata = {
  title: "حلول الحياة من القرآن الكريم | منصة الذكاء الاصطناعي",
  description: "منصة ذكية تساعدك في العثور على إرشادات قرآنية لأي موضوع في حياتك باستخدام الذكاء الاصطناعي",
  keywords: ["القرآن الكريم", "ذكاء اصطناعي", "إرشاد قرآني", "تفسير", "معجزات علمية"],
  authors: [{ name: "Quran Life Solutions" }],
  openGraph: { title: "حلول الحياة من القرآن الكريم", description: "منصة ذكية تساعدك في العثور على إرشادات قرآنية لأي موضوع في حياتك", type: "website", locale: "ar_SA" },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ar" dir="rtl">
      <head>
        <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@300;400;500;700;800&family=Noto+Sans+Arabic:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-screen bg-quran-dark text-white font-body">
        <Toaster position="top-center" toastOptions={{ style: { background: "#16213e", color: "#e0e0e0", border: "1px solid rgba(212, 168, 67, 0.3)", direction: "rtl", fontFamily: "Tajawal, sans-serif" } }} />
        <Navbar />
        <main className="min-h-screen">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
