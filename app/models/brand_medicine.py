from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class BrandMedicine(Base):
    __tablename__ = "brand_medicines"

    id = Column(Integer, primary_key=True, index=True)

    brand_name = Column(String, nullable=False)

    generic_id = Column(Integer, ForeignKey("generic_medicines.id"))
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))

    dosage_form = Column(String)
    strength = Column(String)
    pack_size = Column(String)

    price = Column(Float)
    is_discontinued = Column(Boolean, default=False)

    generic = relationship("GenericMedicine", back_populates="brands")
    manufacturer = relationship("Manufacturer", back_populates="brands")

    batches = relationship("Batch", back_populates="brand")