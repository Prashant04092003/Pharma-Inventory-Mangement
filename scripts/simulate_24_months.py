import random
from datetime import datetime
from dateutil.relativedelta import relativedelta

import app.models

from app.db.session import SessionLocal
from app.models.store import Store
from app.models.warehouse import Warehouse
from app.models.batch import Batch
from app.models.transaction import Transaction, TransactionType
from app.models.brand_medicine import BrandMedicine
from app.models.generic_medicine import GenericMedicine

CHUNK_SIZE = 500
MONTHS = 24


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


def seasonal_multiplier(month):
    if month in [7, 8, 9]:
        return 1.5
    elif month in [12, 1]:
        return 1.4
    else:
        return 1.0


def demand_weight(therapeutic_class):
    if not therapeutic_class:
        return 1

    t = therapeutic_class.lower()

    if any(k in t for k in ["antibiotic", "fever", "pain"]):
        return 5
    elif any(k in t for k in ["diabet", "cardio", "bp"]):
        return 4
    elif any(k in t for k in ["vitamin", "gastro"]):
        return 3
    else:
        return 1


def simulate():
    db = SessionLocal()

    warehouse = db.query(Warehouse).first()
    stores = db.query(Store).all()

    brands = {b.id: b for b in db.query(BrandMedicine).all()}
    generics = {g.id: g for g in db.query(GenericMedicine).all()}

    current_date = datetime.utcnow()

    txn_buffer = []

    for month_index in range(MONTHS):
        sim_date = current_date + relativedelta(months=month_index)
        print(f"Simulating Month {month_index + 1} ({sim_date.month}/{sim_date.year})")

        for store in stores:
            tier = get_tier(store.location)
            tier_multiplier = {1: 1.5, 2: 1.0, 3: 0.6}[tier]

            store_batches = (
                db.query(Batch)
                .filter(Batch.store_id == store.id, Batch.total_units > 0)
                .all()
            )

            brand_to_batches = {}
            for batch in store_batches:
                brand_to_batches.setdefault(batch.brand_id, []).append(batch)

            for brand_id, batches in brand_to_batches.items():
                brand = brands.get(brand_id)
                generic = generics.get(brand.generic_id)

                weight = demand_weight(generic.therapeutic_class)
                season = seasonal_multiplier(sim_date.month)

                if weight >= 4:
                    season_factor = season
                else:
                    season_factor = 1.0

                base_rate = random.randint(5, 20)

                monthly_units = int(
                    base_rate * weight * tier_multiplier * season_factor
                )

                total_available = sum(b.total_units for b in batches)

                if total_available <= 0:
                    continue

                units_to_sell = min(monthly_units, total_available)

                remaining = units_to_sell

                # FIFO: sort by earliest expiry
                batches.sort(key=lambda x: x.expiry_date or datetime.max)

                for batch in batches:
                    if remaining <= 0:
                        break

                    sell_from_batch = min(batch.total_units, remaining)
                    batch.total_units -= sell_from_batch
                    remaining -= sell_from_batch

                    sale_txn = Transaction(
                        batch_id=batch.id,
                        store_id=store.id,
                        warehouse_id=None,
                        quantity=sell_from_batch,
                        transaction_type=TransactionType.OUT,
                        unit_price=batch.cost_price * 1.3,
                        timestamp=sim_date,
                    )

                    txn_buffer.append(sale_txn)

                # Replenishment check
                new_total = sum(b.total_units for b in batches)

                if new_total < 100:
                    warehouse_batches = (
                        db.query(Batch)
                        .filter(
                            Batch.warehouse_id == warehouse.id,
                            Batch.brand_id == brand_id,
                            Batch.total_units > 0,
                        )
                        .all()
                    )

                    if warehouse_batches:
                        source_batch = random.choice(warehouse_batches)
                        replenish_qty = min(500, source_batch.total_units)

                        source_batch.total_units -= replenish_qty

                        new_batch = Batch(
                            brand_id=brand_id,
                            store_id=store.id,
                            warehouse_id=None,
                            total_units=replenish_qty,
                            expiry_date=source_batch.expiry_date,
                            cost_price=source_batch.cost_price,
                        )

                        db.add(new_batch)
                        db.flush()

                        warehouse_txn = Transaction(
                            batch_id=source_batch.id,
                            warehouse_id=warehouse.id,
                            store_id=None,
                            quantity=replenish_qty,
                            transaction_type=TransactionType.OUT,
                            unit_price=source_batch.cost_price,
                            timestamp=sim_date,
                        )

                        store_in_txn = Transaction(
                            batch_id=new_batch.id,
                            warehouse_id=None,
                            store_id=store.id,
                            quantity=replenish_qty,
                            transaction_type=TransactionType.IN,
                            unit_price=source_batch.cost_price,
                            timestamp=sim_date,
                        )

                        txn_buffer.extend([warehouse_txn, store_in_txn])

                if len(txn_buffer) >= CHUNK_SIZE:
                    db.add_all(txn_buffer)
                    db.commit()
                    txn_buffer.clear()

    if txn_buffer:
        db.add_all(txn_buffer)
        db.commit()

    print("24-month simulation complete.")
    db.close()


if __name__ == "__main__":
    simulate()