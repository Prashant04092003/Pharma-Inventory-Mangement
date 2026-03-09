from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class GenericMedicine(Base):
    __tablename__ = "generic_medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    therapeutic_class = Column(String)

    is_prescription_required = Column(Boolean, default=False)
    requires_cold_storage = Column(Boolean, default=False)
    gst_percent = Column(Integer, default=5)

    brands = relationship("BrandMedicine", back_populates="generic")