from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(String(50), primary_key=True)
    name_ar = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    icon = Column(String(10))
    description = Column(Text)
    color = Column(String(50))
    bg_color = Column(String(50))
    text_color = Column(String(50))
    parent_id = Column(String(50), ForeignKey("categories.id"), nullable=True)
