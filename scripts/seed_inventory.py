import random
from datetime import datetime, timedelta

import app.models  # ensure model registry loads

from app.db.session import SessionLocal
from app.models.brand_medicine import BrandMedicine
from app.models.generic_medicine import GenericMedicine
from app.models.warehouse import Warehouse
from app.models.batch import Batch

CHUNK_SIZE = 500
TARGET_WAREHOUSE_BRANDS = 6000


def months_from_now(months):
    return datetime.utcnow() + timedelta(days=30 * months)


def demand_weight(generic: GenericMedicine, brand: BrandMedicine):
    text = (generic.therapeutic_class or "").lower()

    high_keywords = ["antibiotic", "fever", "pain", "diabetic", "cardio"]
    medium_keywords = ["vitamin", "gastro", "allergy", "bp"]

    weight = 1

    if any(k in text for k in high_keywords):
        weight = 5
    elif any(k in text for k in medium_keywords):
        weight = 3

    # Tablets slightly higher demand
    if brand.dosage_form and brand.dosage_form.lower() == "tablet":
        weight += 1

    return weight


def seed_warehouse_inventory():
    db = SessionLocal()

    print("Loading brands & generics...")

    brands = (
        db.query(BrandMedicine)
        .filter(BrandMedicine.is_discontinued == False)
        .all()
    )

    generics_map = {
        g.id: g for g in db.query(GenericMedicine).all()
    }

    warehouse = db.query(Warehouse).first()

    print(f"Total eligible brands: {len(brands)}")

    # Compute weighted list
    weighted_brands = []

    for brand in brands:
        generic = generics_map.get(brand.generic_id)
        w = demand_weight(generic, brand)
        weighted_brands.extend([brand] * w)

    print("Selecting warehouse brands (weighted)...")

    selected_brands = random.sample(
        weighted_brands,
        min(TARGET_WAREHOUSE_BRANDS, len(weighted_brands))
    )

    # Remove duplicates after sampling
    selected_brands = list({b.id: b for b in selected_brands}.values())

    print(f"Final warehouse brand count: {len(selected_brands)}")

    batches_to_insert = []

    for brand in selected_brands:
        generic = generics_map.get(brand.generic_id)
        weight = demand_weight(generic, brand)

        num_batches = random.randint(1, 3)

        for _ in range(num_batches):
            base_qty = random.randint(200, 800)
            total_units = base_qty * weight * 3  # over-provisioned

            expiry_months = random.randint(6, 24)
            expiry_date = months_from_now(expiry_months)

            mrp = brand.price or 100
            cost_price = mrp * random.uniform(0.7, 0.85)

            batch = Batch(
                brand_id=brand.id,
                warehouse_id=warehouse.id,
                store_id=None,
                total_units=int(total_units),
                expiry_date=expiry_date,
                cost_price=round(cost_price, 2),
            )

            batches_to_insert.append(batch)

            if len(batches_to_insert) >= CHUNK_SIZE:
                db.bulk_save_objects(batches_to_insert)
                db.commit()
                batches_to_insert.clear()

    if batches_to_insert:
        db.bulk_save_objects(batches_to_insert)
        db.commit()

    print("Warehouse inventory seeded.")
    db.close()


if __name__ == "__main__":
    seed_warehouse_inventory()