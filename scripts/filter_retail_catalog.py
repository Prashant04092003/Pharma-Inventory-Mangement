import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

BRANDS_FILE = PROCESSED_DIR / "brands_master.csv"
GENERICS_FILE = PROCESSED_DIR / "generics_master.csv"
MANUFACTURERS_FILE = PROCESSED_DIR / "manufacturers_master.csv"

TARGET_GENERICS = 1500
TARGET_MANUFACTURERS = 1500
TARGET_BRANDS = 8000


def load_data():
    brands = pd.read_csv(BRANDS_FILE)
    generics = pd.read_csv(GENERICS_FILE)
    manufacturers = pd.read_csv(MANUFACTURERS_FILE)
    return brands, generics, manufacturers


def filter_retail(brands):
    # Remove discontinued
    brands = brands[brands["is_discontinued"] == False]

    # Keep common dosage forms
    allowed_forms = ["tablet", "capsule", "syrup", "injection", "ointment", "drops"]
    brands = brands[
        brands["dosage_form"].str.lower().isin(allowed_forms)
    ]

    return brands


def select_top_generics(brands):
    generic_counts = brands["generic_id"].value_counts()

    top_generics = generic_counts.head(TARGET_GENERICS).index.tolist()

    brands = brands[brands["generic_id"].isin(top_generics)]

    return brands


def select_top_manufacturers(brands):
    manufacturer_counts = brands["manufacturer_id"].value_counts()

    top_manufacturers = manufacturer_counts.head(TARGET_MANUFACTURERS).index.tolist()

    brands = brands[brands["manufacturer_id"].isin(top_manufacturers)]

    return brands


def cap_brands(brands):
    if len(brands) > TARGET_BRANDS:
        brands = brands.head(TARGET_BRANDS)
    return brands


def main():
    print("Loading master data...")
    brands, generics, manufacturers = load_data()

    print("Filtering retail products...")
    brands = filter_retail(brands)

    print("Selecting top generics...")
    brands = select_top_generics(brands)

    print("Selecting top manufacturers...")
    brands = select_top_manufacturers(brands)

    print("Capping brand count...")
    brands = cap_brands(brands)

    print("Rebuilding generics & manufacturers...")

    generics = generics[generics["generic_id"].isin(brands["generic_id"])]
    manufacturers = manufacturers[manufacturers["manufacturer_id"].isin(brands["manufacturer_id"])]

    print("Saving retail catalog...")

    brands.to_csv(PROCESSED_DIR / "retail_brands.csv", index=False)
    generics.to_csv(PROCESSED_DIR / "retail_generics.csv", index=False)
    manufacturers.to_csv(PROCESSED_DIR / "retail_manufacturers.csv", index=False)

    print("Done.")
    print(f"Retail Manufacturers: {len(manufacturers)}")
    print(f"Retail Generics: {len(generics)}")
    print(f"Retail Brands: {len(brands)}")


if __name__ == "__main__":
    main()