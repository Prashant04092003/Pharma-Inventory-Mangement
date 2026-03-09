import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_indian_pharma():
    file_path = RAW_DIR / "indian_pharma" / "indian_pharmaceutical_products_clean.csv"
    df = pd.read_csv(file_path)
    return df


def clean_manufacturers(df):
    manufacturers = (
        df["manufacturer"]
        .dropna()
        .str.strip()
        .drop_duplicates()
        .reset_index(drop=True)
    )

    manufacturers_df = pd.DataFrame({
        "manufacturer_id": range(1, len(manufacturers) + 1),
        "manufacturer_name": manufacturers
    })

    return manufacturers_df


def clean_generics(df):
    generics = (
        df[["primary_ingredient", "therapeutic_class"]]
        .dropna(subset=["primary_ingredient"])
        .drop_duplicates()
        .reset_index(drop=True)
    )

    generics["generic_id"] = range(1, len(generics) + 1)

    generics_df = generics.rename(columns={
        "primary_ingredient": "generic_name"
    })

    generics_df = generics_df[[
        "generic_id",
        "generic_name",
        "therapeutic_class"
    ]]

    return generics_df


def clean_brands(df, manufacturers_df, generics_df):
    df = df.copy()

    df = df.merge(
        manufacturers_df,
        left_on="manufacturer",
        right_on="manufacturer_name",
        how="left"
    )

    df = df.merge(
        generics_df,
        left_on="primary_ingredient",
        right_on="generic_name",
        how="left"
    )

    brands_df = df[[
        "brand_name",
        "generic_id",
        "manufacturer_id",
        "dosage_form",
        "primary_strength",
        "pack_size",
        "pack_unit",
        "price_inr",
        "is_discontinued"
    ]].copy()

    brands_df = brands_df.drop_duplicates().reset_index(drop=True)

    brands_df.insert(0, "brand_id", range(1, len(brands_df) + 1))

    return brands_df


def main():
    print("Loading data...")
    df = load_indian_pharma()

    print("Cleaning manufacturers...")
    manufacturers_df = clean_manufacturers(df)

    print("Cleaning generics...")
    generics_df = clean_generics(df)

    print("Cleaning brands...")
    brands_df = clean_brands(df, manufacturers_df, generics_df)

    print("Saving processed files...")

    manufacturers_df.to_csv(PROCESSED_DIR / "manufacturers_master.csv", index=False)
    generics_df.to_csv(PROCESSED_DIR / "generics_master.csv", index=False)
    brands_df.to_csv(PROCESSED_DIR / "brands_master.csv", index=False)

    print("Done.")
    print(f"Manufacturers: {len(manufacturers_df)}")
    print(f"Generics: {len(generics_df)}")
    print(f"Brands: {len(brands_df)}")


if __name__ == "__main__":
    main()