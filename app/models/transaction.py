from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Enum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base


class TransactionType(enum.Enum):
    IN = "IN"
    OUT = "OUT"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    batch_id = Column(Integer, ForeignKey("batches.id"))

    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)

    quantity = Column(Integer, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)

    unit_price = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)

    batch = relationship("Batch", back_populates="transactions")
    warehouse = relationship("Warehouse", back_populates="transactions")
    store = relationship("Store", back_populates="transactions")


# Indexes for performance (important for 2M rows)
Index("idx_transaction_store", Transaction.store_id)
Index("idx_transaction_timestamp", Transaction.timestamp)
Index("idx_transaction_batch", Transaction.batch_id)