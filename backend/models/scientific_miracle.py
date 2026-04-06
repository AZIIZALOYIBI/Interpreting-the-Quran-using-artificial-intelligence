from sqlalchemy import Column, Integer, String, Text
from database import Base


class ScientificMiracle(Base):
    __tablename__ = "scientific_miracles"

    id = Column(Integer, primary_key=True, index=True)
    title_ar = Column(String(200), nullable=False)
    title_en = Column(String(200))
    ayah = Column(Text, nullable=False)
    surah_name = Column(String(100))
    ayah_ref = Column(String(50))
    scientific_fact = Column(Text)
    category = Column(String(100))
