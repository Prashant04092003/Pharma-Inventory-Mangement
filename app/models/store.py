from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="store")
    batches = relationship("Batch", back_populates="store")
    transactions = relationship("Transaction", back_populates="store")