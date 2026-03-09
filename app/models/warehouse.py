from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    batches = relationship("Batch", back_populates="warehouse")
    transactions = relationship("Transaction", back_populates="warehouse")