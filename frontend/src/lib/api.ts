import axios from "axios";
import {
  AskQuranRequest,
  AskQuranResponse,
  Category,
  ScientificMiracle,
  SearchResult,
  Surah,
  QuranVerse,
  TafsirEntry,
} from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
  timeout: 30000,
});

export const askQuran = async (data: AskQuranRequest): Promise<AskQuranResponse> => {
  const response = await api.post("/api/ask-quran", data);
  return response.data;
};

export const getCategories = async (): Promise<Category[]> => {
  const response = await api.get("/api/categories");
  return response.data;
};

export const searchVerses = async (query: string): Promise<SearchResult> => {
  const response = await api.get(`/api/quran/search?q=${encodeURIComponent(query)}`);
  return response.data;
};

export const getMiracles = async (): Promise<ScientificMiracle[]> => {
  const response = await api.get("/api/miracles");
  return response.data;
};

export const getSurahs = async (): Promise<Surah[]> => {
  const response = await api.get("/api/quran/surahs");
  return response.data;
};

export const getSurahVerses = async (surahNumber: number): Promise<QuranVerse[]> => {
  const response = await api.get(`/api/quran/surah/${surahNumber}`);
  return response.data;
};

export const getTafsir = async (surahNumber: number, ayahNumber: number): Promise<TafsirEntry[]> => {
  const response = await api.get(`/api/tafsir/${surahNumber}/${ayahNumber}`);
  return response.data;
};

export default api;
