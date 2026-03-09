from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)

    brand_id = Column(Integer, ForeignKey("brand_medicines.id"))

    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)

    total_units = Column(Integer, nullable=False)

    expiry_date = Column(DateTime)
    cost_price = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    brand = relationship("BrandMedicine", back_populates="batches")
    warehouse = relationship("Warehouse", back_populates="batches")
    store = relationship("Store", back_populates="batches")
    transactions = relationship("Transaction", back_populates="batch")