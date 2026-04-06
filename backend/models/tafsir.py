from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base


class Tafsir(Base):
    __tablename__ = "tafsirs"

    id = Column(Integer, primary_key=True, index=True)
    ayah_id = Column(Integer, ForeignKey("ayahs.id"), nullable=False, index=True)
    scholar_name = Column(String(100))
    scholar_name_ar = Column(String(100))
    text = Column(Text, nullable=False)
    source = Column(String(200))
