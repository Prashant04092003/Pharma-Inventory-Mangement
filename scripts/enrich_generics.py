import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

GENERICS_FILE = PROCESSED_DIR / "retail_generics.csv"


def prescription_logic(row):
    text = str(row["therapeutic_class"]).lower()

    keywords = [
        "antibiotic", "diabetic", "cardio", "hypertension",
        "steroid", "hormone", "thyroid", "psychiatric"
    ]

    return any(k in text for k in keywords)


def cold_storage_logic(row):
    name = str(row["generic_name"]).lower()

    keywords = ["insulin", "vaccine", "epoetin", "filgrastim"]

    return any(k in name for k in keywords)


def gst_logic(row):
    if row["cold_storage_required"]:
        return 18
    elif row["prescription_required"]:
        return 12
    else:
        return 5


def main():
    df = pd.read_csv(GENERICS_FILE)

    print("Applying prescription logic...")
    df["prescription_required"] = df.apply(prescription_logic, axis=1)

    print("Applying cold storage logic...")
    df["cold_storage_required"] = df.apply(cold_storage_logic, axis=1)

    print("Applying GST logic...")
    df["gst_percentage"] = df.apply(gst_logic, axis=1)

    df.to_csv(PROCESSED_DIR / "retail_generics_enriched.csv", index=False)

    print("Done.")
    print(f"Total generics enriched: {len(df)}")


if __name__ == "__main__":
    main()