# Pharma Inventory Prototype – Technical Documentation

## 1. System Objective

The objective of this project was to design and implement a structured, queryable pharmaceutical inventory backend capable of supporting:

- Real-time inventory queries
- Store-level stock visibility
- Brand-level stock inspection
- Low-stock detection
- Multi-store inventory aggregation

The system is implemented as a prototype to simulate how a production-grade inventory database would interact with a chatbot or dashboard layer.

The scope includes database design, data ingestion, transaction simulation, business logic abstraction, and REST API exposure.

---

## 2. System Architecture Overview

The system follows a layered architecture:

```
Client (Chatbot / Dashboard)
        ↓
FastAPI (API Layer)
        ↓
Service Layer (Business Logic)
        ↓
SQLAlchemy ORM
        ↓
SQLite Database
```

Each layer has a clearly defined responsibility:

- **Database Layer**: Structured storage and relational integrity.
- **ORM Layer**: Object-relational abstraction.
- **Service Layer**: Business logic and aggregation.
- **API Layer**: HTTP interface for external consumers.

---

## 3. Database Design

### 3.1 Core Entities

The database schema includes the following tables:

- `manufacturers`
- `generic_medicines`
- `brand_medicines`
- `warehouses`
- `stores`
- `users`
- `batches`
- `transactions`

The schema is fully normalized to ensure data consistency and extensibility.

---

### 3.2 Master Data Layer

The master catalog was constructed using structured CSV datasets and includes:

- 871 manufacturers
- 571 generic medicines
- 8000 brand medicines

Each brand medicine contains:

- Brand name
- Generic reference
- Manufacturer reference
- Dosage form
- Strength
- Pack size
- Price

This ensures realistic pharmaceutical SKU representation.

---

### 3.3 Organizational Model

The system models a hierarchical distribution structure:

- One central warehouse
- Fifteen stores across multiple locations
- One administrative user
- Multiple store operator users

This enables store-specific inventory visibility and supports multi-location stock management.

---

### 3.4 Batch-Level Inventory Modeling

Inventory is modeled at the batch level to reflect real-world pharmaceutical operations.

The `batches` table contains:

- `brand_id`
- `warehouse_id`
- `store_id`
- `total_units`
- `expiry_date`
- `cost_price`

This design enables:

- Expiry tracking
- Cost tracking
- Traceability
- Controlled stock movement

Approximately 8,700 warehouse batches were initialized.

---

## 4. Ledger-Based Inventory Accounting

### 4.1 Transaction Model

Inventory movements are recorded in the `transactions` table using a ledger-based approach.

Each transaction contains:

- `batch_id`
- `store_id`
- `transaction_type` (IN / OUT)
- `quantity`
- `timestamp`

Stock is not stored directly.

Instead, current inventory is computed dynamically using:

```
Stock = SUM(IN) − SUM(OUT)
```

---

### 4.2 Simulation

A 24-month transaction simulation was executed to generate realistic operational data.

Results:

- Approximately 541,000 transaction records
- Multi-store distribution patterns
- Variable consumption behavior
- Realistic stock depletion scenarios

This enables reliable aggregation testing and API validation.

---

## 5. Business Logic Layer

Business logic is implemented in:

```
app/services/inventory_service.py
```

The service layer encapsulates stock computation and relational joins.

### 5.1 Core Functions

- `get_store_inventory(store_id)`
- `get_brand_stock_in_store(store_id, brand_name)`
- `get_global_brand_stock(brand_name)`
- `get_low_stock(store_id, threshold)`

### 5.2 Aggregation Strategy

Stock is calculated using SQLAlchemy expressions:

```
SUM(
    CASE
        WHEN transaction_type = IN  THEN quantity
        WHEN transaction_type = OUT THEN -quantity
        ELSE 0
    END
)
```

Joins follow this relational path:

```
BrandMedicine → Batch → Transaction
```

All queries are grouped and filtered to return only meaningful stock values.

---

## 6. API Layer

The API is implemented using FastAPI.

### 6.1 Exposed Endpoints

```
GET /store/{store_id}/inventory
GET /store/{store_id}/brand/{brand_name}
GET /brand/{brand_name}/global-stock
GET /store/{store_id}/low-stock
```

### 6.2 API Responsibilities

The API layer:

- Accepts HTTP requests
- Validates parameters
- Invokes service-layer functions
- Returns structured JSON responses

No direct SQL queries are exposed externally.

---

## 7. OpenAPI Documentation

FastAPI auto-generates an OpenAPI specification accessible via:

```
/docs
```

This provides:

- Interactive endpoint testing
- Structured API schema
- Compatibility with AI tool-call integrations

---

## 8. Design Decisions

### 8.1 Why Ledger-Based Instead of Stored Stock?

Advantages:

- Auditability
- Deterministic recomputation
- Prevention of stock corruption
- Historical traceability
- Realistic accounting model

---

### 8.2 Why Layered Architecture?

Separation of concerns ensures:

- Database independence
- Service-layer testability
- API portability
- Chatbot integration flexibility

---

### 8.3 Why No Authentication in Prototype?

This system is a functional prototype intended to simulate chatbot interaction with structured inventory data.

Authentication and production-grade security mechanisms are intentionally excluded from scope.

---

## 9. Final System Metrics

- 8000 brand medicines
- 871 manufacturers
- 571 generics
- 15 stores
- 1 warehouse
- 24 months simulated
- 541,000+ transactions
- Ledger-based inventory computation
- Fully functional REST API

---

## 10. Conclusion

The system successfully implements a multi-store, ledger-based pharmaceutical inventory backend with dynamic stock computation and REST API exposure.

The database layer, business logic layer, and API layer are complete and operational.

The system is ready for integration with:

- Chatbot reasoning engines
- Dashboards
- Reporting layers
- AI-based inventory analysis tools