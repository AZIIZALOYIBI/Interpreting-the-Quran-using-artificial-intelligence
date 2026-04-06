"use client";
import { useState, useCallback } from "react";

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  suggestions?: string[];
}

export default function SearchBar({
  onSearch,
  placeholder = "ابحث في القرآن الكريم...",
  suggestions = [],
}: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      if (query.trim()) {
        onSearch(query.trim());
        setShowSuggestions(false);
      }
    },
    [query, onSearch]
  );

  const defaultSuggestions = [
    "الصبر والشكر",
    "الصحة والشفاء",
    "الرزق والمال",
    "الأسرة والزواج",
    "العلم والتعلم",
    "التوبة والمغفرة",
  ];

  const displaySuggestions = suggestions.length > 0 ? suggestions : defaultSuggestions;

  return (
    <div className="relative w-full">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <div className="relative flex-1">
          <span className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg">🔍</span>
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setShowSuggestions(e.target.value.length > 0);
            }}
            onFocus={() => setShowSuggestions(true)}
            onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
            placeholder={placeholder}
            className="w-full bg-white border-2 border-emerald-200 rounded-xl py-3 px-12 text-right focus:outline-none focus:border-emerald-500 transition-colors text-gray-800"
            dir="rtl"
          />
        </div>
        <button type="submit" className="btn-primary px-6 py-3">
          بحث
        </button>
      </form>

      {showSuggestions && (
        <div className="absolute top-full right-0 left-0 mt-1 bg-white border border-gray-200 rounded-xl shadow-lg z-10 overflow-hidden">
          <div className="p-2 text-xs text-gray-500 border-b px-4">اقتراحات شائعة</div>
          {displaySuggestions.map((suggestion, i) => (
            <button
              key={i}
              className="w-full text-right px-4 py-2 hover:bg-emerald-50 text-gray-700 transition-colors"
              onMouseDown={() => {
                setQuery(suggestion);
                onSearch(suggestion);
                setShowSuggestions(false);
              }}
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
