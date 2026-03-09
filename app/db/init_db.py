from app.db.base import Base
from app.db.session import engine

# Import all models so they register with Base
from app.models import (
    manufacturer,
    generic_medicine,
    brand_medicine,
    warehouse,
    store,
    user,
    batch,
    transaction,
)


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()