from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ADMIN / SHOP_OPERATOR

    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    store = relationship("Store", back_populates="users")