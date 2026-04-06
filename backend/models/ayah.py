from sqlalchemy import Column, Integer, String, Text
from database import Base


class Ayah(Base):
    __tablename__ = "ayahs"

    id = Column(Integer, primary_key=True, index=True)
    surah_id = Column(Integer, nullable=False, index=True)
    ayah_number = Column(Integer, nullable=False)
    text_uthmani = Column(Text, nullable=False)
    text_simple = Column(Text, nullable=False)
    surah_name = Column(String(100))
    surah_name_ar = Column(String(100))
