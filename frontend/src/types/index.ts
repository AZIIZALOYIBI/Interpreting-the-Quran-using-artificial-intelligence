export interface Ayah {
  id: number;
  surah_id: number;
  ayah_number: number;
  text_uthmani: string;
  text_simple: string;
  surah_name?: string;
  surah_name_ar?: string;
  tafsir?: string;
  relevance_score?: number;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  ayahs?: Ayah[];
  category?: string;
  practical_steps?: string[];
  timestamp: Date;
}

export interface QuranVerse {
  id: number;
  surah_number: number;
  surah_name: string;
  surah_name_en: string;
  ayah_number: number;
  text_uthmani: string;
  text_simple: string;
  translation?: string;
  juz_number: number;
  hizb_number: number;
  page_number: number;
}

export interface Category {
  id: string;
  name: string;
  name_en: string;
  icon: string;
  description: string;
  color: string;
  verse_count: number;
}

export interface AskQuranRequest {
  question: string;
  category?: string;
}

export interface AskQuranResponse {
  answer: string;
  ayahs: Ayah[];
  category: string;
  practical_steps: string[];
  disclaimer: string;
}

export interface ScientificMiracle {
  id: number;
  title: string;
  description: string;
  scientific_fact: string;
  quran_reference: string;
  verse_text: string;
  surah_name: string;
  ayah_number: number;
  category: string;
  discovery_year?: string;
  image_url?: string;
}

export interface TafsirEntry {
  id: number;
  verse_id: number;
  scholar_name: string;
  scholar_name_en: string;
  tafsir_text: string;
  source: string;
  era: string;
}

export interface SearchResult {
  verses: QuranVerse[];
  total_count: number;
  query: string;
  suggestions: string[];
}

export interface Tafsir {
  id: number;
  ayahId: number;
  scholarName: string;
  scholarNameAr: string;
  text: string;
  source: string;
}

export interface SurahInfo {
  id: number;
  nameAr: string;
  nameEn: string;
  ayahCount: number;
  revelationType: "meccan" | "medinan";
}

export interface Surah {
  number: number;
  name: string;
  name_en: string;
  name_translation: string;
  revelation_type: string;
  ayah_count: number;
}
