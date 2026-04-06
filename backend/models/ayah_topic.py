from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class AyahTopic(Base):
    __tablename__ = "ayah_topics"

    id = Column(Integer, primary_key=True, index=True)
    ayah_id = Column(Integer, ForeignKey("ayahs.id"), nullable=False)
    topic = Column(String(100), nullable=False)
    relevance_score = Column(Integer, default=1)
