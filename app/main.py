from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.inventory_service import (
    get_store_inventory,
    get_brand_stock_in_store,
    get_global_brand_stock,
    get_low_stock,
)

app = FastAPI(title="Pharma Inventory API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/store/{store_id}/inventory")
def store_inventory(store_id: int, db: Session = Depends(get_db)):
    data = get_store_inventory(db, store_id)
    return [
        {
            "brand_id": row[0],
            "brand_name": row[1],
            "current_stock": row[2],
        }
        for row in data
    ]


@app.get("/store/{store_id}/brand/{brand_name}")
def brand_in_store(store_id: int, brand_name: str, db: Session = Depends(get_db)):
    result = get_brand_stock_in_store(db, store_id, brand_name)

    if not result:
        raise HTTPException(status_code=404, detail="Brand not found in store")

    return {
        "brand_name": result[0],
        "current_stock": result[1],
    }


@app.get("/brand/{brand_name}/global-stock")
def global_brand_stock(brand_name: str, db: Session = Depends(get_db)):
    data = get_global_brand_stock(db, brand_name)

    return [
        {
            "store_name": row[0],
            "current_stock": row[1],
        }
        for row in data
    ]


@app.get("/store/{store_id}/low-stock")
def low_stock(store_id: int, threshold: int = 50, db: Session = Depends(get_db)):
    data = get_low_stock(db, store_id, threshold)

    return [
        {
            "brand_name": row[0],
            "current_stock": row[1],
        }
        for row in data
    ]