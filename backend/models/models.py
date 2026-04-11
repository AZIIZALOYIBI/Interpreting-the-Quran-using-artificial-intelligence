"""SQLAlchemy database models."""

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Surah(Base):
    __tablename__ = "surahs"
    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    name_translation = Column(String(200))
    revelation_type = Column(String(20))
    ayah_count = Column(Integer)
    verses = relationship("Verse", back_populates="surah")


class Verse(Base):
    __tablename__ = "verses"
    id = Column(Integer, primary_key=True)
    surah_number = Column(Integer, ForeignKey("surahs.number"), nullable=False, index=True)
    ayah_number = Column(Integer, nullable=False)
    text_uthmani = Column(Text, nullable=False)
    text_simple = Column(Text, nullable=False)
    translation = Column(Text)
    juz_number = Column(Integer)
    hizb_number = Column(Integer)
    page_number = Column(Integer)
    surah = relationship("Surah", back_populates="verses")
    tafsirs = relationship("Tafsir", back_populates="verse")


class Tafsir(Base):
    __tablename__ = "tafsirs"
    id = Column(Integer, primary_key=True)
    verse_id = Column(Integer, ForeignKey("verses.id"), nullable=False, index=True)
    scholar_name = Column(String(200), nullable=False)
    scholar_name_en = Column(String(200))
    tafsir_text = Column(Text, nullable=False)
    source = Column(String(300))
    era = Column(String(100))
    verse = relationship("Verse", back_populates="tafsirs")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    question_text = Column(Text, nullable=False)
    category = Column(String(50))
    answer_text = Column(Text)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
