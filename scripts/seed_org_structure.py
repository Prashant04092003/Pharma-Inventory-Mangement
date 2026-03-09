import app.models  # registers all models

from app.db.session import SessionLocal
from app.models.warehouse import Warehouse
from app.models.store import Store
from app.models.user import User


def seed_org():
    db = SessionLocal()

    print("Clearing existing org data...")
    db.query(User).delete()
    db.query(Store).delete()
    db.query(Warehouse).delete()
    db.commit()

    print("Creating warehouse...")
    warehouse = Warehouse(name="UP Central Pharma Distribution - Lucknow")
    db.add(warehouse)
    db.commit()

    print("Creating stores...")

    tier1 = ["Lucknow", "Kanpur", "Noida"]
    tier2 = ["Ayodhya", "Bareilly", "Meerut"]
    tier3 = ["Bahraich", "Gonda", "Kasganj"]

    stores = []

    # Tier 1 → 3 stores per city
    for city in tier1:
        for i in range(1, 4):
            store = Store(
                name=f"{city} Store {i}",
                location=city
            )
            stores.append(store)

    # Tier 2 → 1 store each
    for city in tier2:
        store = Store(
            name=f"{city} Store 1",
            location=city
        )
        stores.append(store)

    # Tier 3 → 1 store each
    for city in tier3:
        store = Store(
            name=f"{city} Store 1",
            location=city
        )
        stores.append(store)

    db.add_all(stores)
    db.commit()

    print("Creating users...")

    # Admin
    admin = User(
        name="System Admin",
        role="ADMIN",
        store_id=None
    )
    db.add(admin)

    # Store Operators
    for store in stores:
        operator = User(
            name=f"{store.name} Operator",
            role="SHOP_OPERATOR",
            store_id=store.id
        )
        db.add(operator)

    db.commit()

    print("Done.")
    print(f"Warehouse: 1")
    print(f"Stores: {len(stores)}")
    print(f"Users: {1 + len(stores)}")

    db.close()


if __name__ == "__main__":
    seed_org()