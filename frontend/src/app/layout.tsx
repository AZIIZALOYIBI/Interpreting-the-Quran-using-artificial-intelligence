import type { Metadata } from "next";
import "./globals.css";
import BackToTop from "@/components/BackToTop";

export const metadata: Metadata = {
  title: "حلول الحياة من القرآن الكريم | بالذكاء الاصطناعي",
  description: "منصة ذكية تساعدك في إيجاد الإرشاد والتوجيه القرآني لأي موضوع في حياتك",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ar" dir="rtl">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Amiri+Quran&family=Amiri:ital,wght@0,400;0,700;1,400&family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen" style={{ backgroundColor: "var(--claude-bg)", color: "var(--claude-text)" }}>
        {children}
        <BackToTop />
      </body>
    </html>
  );
}
