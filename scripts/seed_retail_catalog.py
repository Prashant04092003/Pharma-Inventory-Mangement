import pandas as pd
from pathlib import Path
from app.models.batch import Batch

from app.db.session import SessionLocal
from app.models.manufacturer import Manufacturer
from app.models.generic_medicine import GenericMedicine
from app.models.brand_medicine import BrandMedicine

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def seed():
    db = SessionLocal()

    print("Loading CSV files...")

    manufacturers_df = pd.read_csv(PROCESSED_DIR / "retail_manufacturers.csv")
    generics_df = pd.read_csv(PROCESSED_DIR / "retail_generics_enriched.csv")
    brands_df = pd.read_csv(PROCESSED_DIR / "retail_brands.csv")

    print("Clearing existing data...")
    db.query(BrandMedicine).delete()
    db.query(GenericMedicine).delete()
    db.query(Manufacturer).delete()
    db.commit()

    print("Seeding manufacturers...")
    manufacturer_objects = [
        Manufacturer(
            id=row["manufacturer_id"],
            name=row["manufacturer_name"]
        )
        for _, row in manufacturers_df.iterrows()
    ]
    db.bulk_save_objects(manufacturer_objects)
    db.commit()

    print("Seeding generics...")
    generic_objects = [
        GenericMedicine(
            id=row["generic_id"],
            name=row["generic_name"],
            therapeutic_class=row.get("therapeutic_class"),
            is_prescription_required=row.get("is_prescription_required", False),
            requires_cold_storage=row.get("requires_cold_storage", False),
            gst_percent=row.get("gst_percent", 5),
        )
        for _, row in generics_df.iterrows()
    ]
    db.bulk_save_objects(generic_objects)
    db.commit()

    print("Seeding brands...")
    brand_objects = [
        BrandMedicine(
            id=row["brand_id"],
            brand_name=row["brand_name"],
            generic_id=row["generic_id"],
            manufacturer_id=row["manufacturer_id"],
            dosage_form=row.get("dosage_form"),
            strength=row.get("primary_strength"),
            pack_size=row.get("pack_size"),
            price=row.get("price_inr"),
            is_discontinued=row.get("is_discontinued", False),
        )
        for _, row in brands_df.iterrows()
    ]
    db.bulk_save_objects(brand_objects)
    db.commit()

    print("Done.")
    print(f"Manufacturers: {len(manufacturer_objects)}")
    print(f"Generics: {len(generic_objects)}")
    print(f"Brands: {len(brand_objects)}")

    db.close()


if __name__ == "__main__":
    seed()