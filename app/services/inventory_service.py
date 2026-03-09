from sqlalchemy.orm import Session
from sqlalchemy import case, func

from app.models.batch import Batch
from app.models.transaction import Transaction, TransactionType
from app.models.store import Store
from app.models.brand_medicine import BrandMedicine


def _stock_expression():
    """
    Creates SUM(IN - OUT) expression.
    """
    return func.sum(
        case(
            (Transaction.transaction_type == TransactionType.IN, Transaction.quantity),
            (Transaction.transaction_type == TransactionType.OUT, -Transaction.quantity),
            else_=0,
        )
    )


def get_store_inventory(db: Session, store_id: int):
    return (
        db.query(
            BrandMedicine.id.label("brand_id"),
            BrandMedicine.brand_name,
            func.sum(
                case(
                    (Transaction.transaction_type == TransactionType.IN, Transaction.quantity),
                    (Transaction.transaction_type == TransactionType.OUT, -Transaction.quantity),
                    else_=0,
                )
            ).label("current_stock"),
        )
        .join(Batch, Batch.brand_id == BrandMedicine.id)
        .join(Transaction, Transaction.batch_id == Batch.id)
        .filter(Transaction.store_id == store_id)
        .group_by(BrandMedicine.id, BrandMedicine.brand_name)
        .having(
            func.sum(
                case(
                    (Transaction.transaction_type == TransactionType.IN, Transaction.quantity),
                    (Transaction.transaction_type == TransactionType.OUT, -Transaction.quantity),
                    else_=0,
                )
            ) > 0
        )
        .all()
    )


def get_brand_stock_in_store(db: Session, store_id: int, brand_name: str):
    return (
        db.query(
            BrandMedicine.brand_name,
            _stock_expression().label("current_stock"),
        )
        .join(Batch, Batch.brand_id == BrandMedicine.id)
        .join(Transaction, Transaction.batch_id == Batch.id)
        .filter(
            Transaction.store_id == store_id,
            BrandMedicine.brand_name.ilike(f"%{brand_name}%"),
        )
        .group_by(BrandMedicine.brand_name)
        .first()
    )


def get_global_brand_stock(db: Session, brand_name: str):
    return (
        db.query(
            Store.name,
            _stock_expression().label("current_stock"),
        )
        .join(Batch, Batch.store_id == Store.id)
        .join(Transaction, Transaction.batch_id == Batch.id)
        .join(BrandMedicine, Batch.brand_id == BrandMedicine.id)
        .filter(BrandMedicine.brand_name.ilike(f"%{brand_name}%"))
        .group_by(Store.name)
        .having(_stock_expression() > 0)
        .all()
    )

def get_low_stock(db: Session, store_id: int, threshold: int = 50):
    return (
        db.query(
            BrandMedicine.brand_name,
            _stock_expression().label("current_stock"),
        )
        .join(Batch, Batch.brand_id == BrandMedicine.id)
        .join(Transaction, Transaction.batch_id == Batch.id)
        .filter(Transaction.store_id == store_id)
        .group_by(BrandMedicine.brand_name)
        .having(_stock_expression() < threshold)
        .all()
    )