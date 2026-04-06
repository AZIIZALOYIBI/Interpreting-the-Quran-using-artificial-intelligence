from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), nullable=False, index=True)
    category = Column(String(50))
    ayah_id = Column(Integer, ForeignKey("ayahs.id"), nullable=True)
