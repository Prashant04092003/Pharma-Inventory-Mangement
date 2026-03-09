from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    brands = relationship("BrandMedicine", back_populates="manufacturer")