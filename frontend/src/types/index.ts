export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  ayahs?: Ayah[];
  category?: string;
  practicalSteps?: string[];
  timestamp: Date;
}

export interface Ayah {
  id: number;
  surahId: number;
  surahName: string;
  surahNameAr: string;
  ayahNumber: number;
  textUthmani: string;
  textSimple: string;
  translation?: string;
  tafsir?: string;
  relevanceScore?: number;
}

export interface Tafsir {
  id: number;
  ayahId: number;
  scholarName: string;
  scholarNameAr: string;
  text: string;
  source: string;
}

export interface Category {
  id: string;
  nameAr: string;
  nameEn: string;
  icon: string;
  description: string;
  color: string;
  bgColor: string;
  textColor: string;
}

export interface ScientificMiracle {
  id: number;
  titleAr: string;
  titleEn: string;
  ayah: string;
  surahName: string;
  ayahRef: string;
  scientificFact: string;
  category: string;
}

export interface QuranSolution {
  question: string;
  category: string;
  answer: string;
  ayahs: Ayah[];
  practicalSteps: string[];
  additionalContext?: string;
}

export interface ChatRequest {
  question: string;
  category?: string;
  language?: "ar" | "en";
}

export interface ChatResponse {
  answer: string;
  category: string;
  ayahs: Ayah[];
  practicalSteps: string[];
  disclaimer: string;
}

export interface SurahInfo {
  id: number;
  nameAr: string;
  nameEn: string;
  ayahCount: number;
  revelationType: "meccan" | "medinan";
}
