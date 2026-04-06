import type { ChatRequest, ChatResponse, Ayah, Tafsir, Category, SurahInfo } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API Error ${response.status}: ${error}`);
  }

  return response.json();
}

export async function askQuran(question: string, category?: string): Promise<ChatResponse> {
  const body: ChatRequest = { question, category, language: "ar" };
  return fetchAPI<ChatResponse>("/api/ask-quran", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function searchAyahs(query: string): Promise<Ayah[]> {
  return fetchAPI<Ayah[]>(`/api/quran/search?q=${encodeURIComponent(query)}`);
}

export async function getAyah(surahId: number, ayahNum: number): Promise<Ayah> {
  return fetchAPI<Ayah>(`/api/quran/ayah/${surahId}/${ayahNum}`);
}

export async function getTafsir(ayahId: number): Promise<Tafsir[]> {
  return fetchAPI<Tafsir[]>(`/api/tafsir/${ayahId}`);
}

export async function getCategories(): Promise<Category[]> {
  return fetchAPI<Category[]>("/api/categories");
}

export async function getCategoryContent(category: string): Promise<{ category: Category; ayahs: Ayah[] }> {
  return fetchAPI<{ category: Category; ayahs: Ayah[] }>(`/api/categories/${category}`);
}

export async function getSurahs(): Promise<SurahInfo[]> {
  return fetchAPI<SurahInfo[]>("/api/quran/surahs");
}

export async function getSurah(surahId: number): Promise<{ info: SurahInfo; ayahs: Ayah[] }> {
  return fetchAPI<{ info: SurahInfo; ayahs: Ayah[] }>(`/api/quran/surah/${surahId}`);
}

export async function getMiracles(category?: string): Promise<unknown[]> {
  const path = category ? `/api/miracles/${category}` : "/api/miracles";
  return fetchAPI<unknown[]>(path);
}
