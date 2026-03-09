import random
from datetime import datetime

import app.models

from app.db.session import SessionLocal
from app.models.store import Store
from app.models.warehouse import Warehouse
from app.models.batch import Batch
from app.models.transaction import Transaction, TransactionType

CHUNK_SIZE = 300


def get_tier(city):
    tier1 = ["Lucknow", "Kanpur", "Noida"]
    tier2 = ["Ayodhya", "Bareilly", "Meerut"]
    tier3 = ["Bahraich", "Gonda", "Kasganj"]

    if city in tier1:
        return 1
    elif city in tier2:
        return 2
    else:
        return 3


def seed_store_distribution():
    db = SessionLocal()

    warehouse = db.query(Warehouse).first()
    stores = db.query(Store).all()

    warehouse_batches = (
        db.query(Batch)
        .filter(Batch.warehouse_id == warehouse.id)
        .all()
    )

    brand_to_batches = {}
    for batch in warehouse_batches:
        brand_to_batches.setdefault(batch.brand_id, []).append(batch)

    all_brand_ids = list(brand_to_batches.keys())

    print(f"Warehouse brands available: {len(all_brand_ids)}")

    for store in stores:
        city = store.location
        tier = get_tier(city)

        if tier == 1:
            target_skus = random.randint(1500, 2000)
        elif tier == 2:
            target_skus = random.randint(800, 1200)
        else:
            target_skus = random.randint(400, 700)

        selected_brands = random.sample(
            all_brand_ids,
            min(target_skus, len(all_brand_ids))
        )

        print(f"{store.name} -> {len(selected_brands)} SKUs")

        batch_buffer = []
        txn_buffer = []

        for brand_id in selected_brands:
            batches = brand_to_batches.get(brand_id)
            if not batches:
                continue

            source_batch = random.choice(batches)

            if source_batch.total_units <= 20:
                continue

            transfer_units = random.randint(
                10,
                min(200, int(source_batch.total_units * 0.25))
            )

            transfer_units = min(transfer_units, source_batch.total_units)

            # Deduct from warehouse
            source_batch.total_units -= transfer_units

            # Create store batch
            store_batch = Batch(
                brand_id=brand_id,
                warehouse_id=None,
                store_id=store.id,
                total_units=transfer_units,
                expiry_date=source_batch.expiry_date,
                cost_price=source_batch.cost_price,
            )

            db.add(store_batch)
            db.flush()  # ensures store_batch.id is generated

            # Warehouse OUT transaction
            warehouse_txn = Transaction(
                batch_id=source_batch.id,
                warehouse_id=warehouse.id,
                store_id=None,
                quantity=transfer_units,
                transaction_type=TransactionType.OUT,
                unit_price=source_batch.cost_price,
                timestamp=datetime.utcnow(),
            )

            # Store IN transaction
            store_txn = Transaction(
                batch_id=store_batch.id,
                warehouse_id=None,
                store_id=store.id,
                quantity=transfer_units,
                transaction_type=TransactionType.IN,
                unit_price=source_batch.cost_price,
                timestamp=datetime.utcnow(),
            )

            txn_buffer.extend([warehouse_txn, store_txn])

            if len(txn_buffer) >= CHUNK_SIZE:
                db.add_all(txn_buffer)
                db.commit()
                txn_buffer.clear()

        if txn_buffer:
            db.add_all(txn_buffer)
            db.commit()

    print("Store distribution complete with symmetrical ledger.")
    db.close()


if __name__ == "__main__":
    seed_store_distribution()