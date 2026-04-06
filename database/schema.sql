-- Quran AI Platform Schema

CREATE TABLE IF NOT EXISTS categories (
    id VARCHAR(50) PRIMARY KEY,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    icon VARCHAR(10),
    description TEXT,
    color VARCHAR(50),
    bg_color VARCHAR(50),
    text_color VARCHAR(50),
    parent_id VARCHAR(50) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS ayahs (
    id SERIAL PRIMARY KEY,
    surah_id INTEGER NOT NULL,
    ayah_number INTEGER NOT NULL,
    text_uthmani TEXT NOT NULL,
    text_simple TEXT NOT NULL,
    surah_name VARCHAR(100),
    surah_name_ar VARCHAR(100),
    UNIQUE(surah_id, ayah_number)
);
CREATE INDEX IF NOT EXISTS idx_ayahs_surah ON ayahs(surah_id);

CREATE TABLE IF NOT EXISTS tafsirs (
    id SERIAL PRIMARY KEY,
    ayah_id INTEGER REFERENCES ayahs(id) ON DELETE CASCADE,
    scholar_name VARCHAR(100),
    scholar_name_ar VARCHAR(100),
    text TEXT NOT NULL,
    source VARCHAR(200)
);
CREATE INDEX IF NOT EXISTS idx_tafsirs_ayah ON tafsirs(ayah_id);

CREATE TABLE IF NOT EXISTS scientific_miracles (
    id SERIAL PRIMARY KEY,
    title_ar VARCHAR(200) NOT NULL,
    title_en VARCHAR(200),
    ayah TEXT NOT NULL,
    surah_name VARCHAR(100),
    ayah_ref VARCHAR(50),
    scientific_fact TEXT,
    category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS qa_pairs (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS keywords (
    id SERIAL PRIMARY KEY,
    word VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    ayah_id INTEGER REFERENCES ayahs(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_keywords_word ON keywords(word);

CREATE TABLE IF NOT EXISTS ayah_topics (
    id SERIAL PRIMARY KEY,
    ayah_id INTEGER REFERENCES ayahs(id) ON DELETE CASCADE,
    topic VARCHAR(100) NOT NULL,
    relevance_score INTEGER DEFAULT 1
);
