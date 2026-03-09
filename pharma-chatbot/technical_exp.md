# Pharmaceutical Inventory AI Chatbot  
## System Architecture Documentation

---

## 1. System Purpose

This system provides a secure, deterministic AI interface over a ledger-based pharmaceutical inventory backend.

The chatbot:

- Interprets natural language queries
- Converts them into structured intent
- Executes validated business logic
- Returns formatted analytical responses
- Maintains structured conversational memory

The AI model does not access the database directly.

All database operations are controlled by backend logic.

---

## 2. Architectural Overview

```
User (UI / Streamlit)
        ↓
FastAPI Chat Endpoint (/chat)
        ↓
ChatService (Orchestration Layer)
        ↓
Intent Extractor (LLM - Structured JSON Output)
        ↓
Validator (Access Control + Schema Enforcement)
        ↓
Intent Router (Deterministic Mapping)
        ↓
Inventory Service (ORM Aggregation Layer)
        ↓
Database (Ledger-Based Model)
        ↓
Response Formatter (LLM - Text Only)
        ↓
Memory Update
        ↓
Final Response
```

---

## 3. Core Architectural Principles

1. LLM never accesses database.
2. LLM never generates SQL.
3. All analytical computation is deterministic.
4. Role-based access is enforced in backend.
5. Conversational memory is structured, not free-form.
6. Database queries use ORM (PostgreSQL-ready).
7. System is database-agnostic.

---

## 4. Data Model (Inventory Layer)

The system uses a ledger-based transaction model.

Stock is not stored directly.

Instead:

```
Current Stock = SUM(IN transactions) − SUM(OUT transactions)
```

This enables:

- Historical reconstruction
- Turnover analysis
- Time-window filtering
- Multi-store comparison
- Data integrity enforcement

Database contains:

- manufacturers
- generic_medicines
- brand_medicines
- stores
- warehouses
- batches
- transactions (~541k records)

---

## 5. Query Flow Examples

---

### Example 1: Direct Store Query

**User Query**

> How much stock of Azithral 500 is available in Lucknow Store 1?

---

### Step 1 – Intent Extraction (LLM)

```json
{
  "intent": "get_brand_stock_in_store",
  "brand_name": "Azithral 500",
  "store_name": "Lucknow Store 1",
  "threshold": null,
  "time_window_days": null
}
```

---

### Step 2 – Validation

- Brand existence verified
- Store existence verified
- Role access validated
- Defaults injected if required

---

### Step 3 – Routing

Intent → `inventory_service.get_brand_stock_in_store()`

---

### Step 4 – Database Aggregation

```
SUM(IN − OUT)
WHERE brand = Azithral 500
AND store = Lucknow Store 1
```

---

### Step 5 – Response Formatting (LLM)

Structured result:

```json
{
  "brand": "Azithral 500",
  "store": "Lucknow Store 1",
  "current_stock": 64
}
```

Formatted output:

> Lucknow Store 1 currently has 64 units of Azithral 500 in stock.

---

### Example 2: Cross-Store Comparison

**User Query**

> Which store has the lowest stock of Azithral 500 in the last 30 days?

---

### Step 1 – Intent Extraction

```json
{
  "intent": "compare_store_stock",
  "brand_name": "Azithral 500",
  "store_name": null,
  "threshold": null,
  "time_window_days": 30
}
```

---

### Step 2 – Validation

- Role must be ADMIN
- Brand verified
- Time window validated

---

### Step 3 – Routing

Intent → `inventory_service.compare_store_stock()`

---

### Step 4 – Aggregation Logic

```
SUM(IN − OUT)
WHERE brand = Azithral 500
AND timestamp >= NOW() − 30 days
GROUP BY store
```

Backend identifies:

- Lowest stock store
- Highest stock store

---

### Step 5 – Formatting

> In the last 30 days, Kanpur Store 2 has the lowest stock of Azithral 500 with 17 units remaining.

---

### Example 3: Low Stock Detection

**User Query**

> Show low stock medicines in Lucknow Store 1.

---

### Step 1 – Intent Extraction

```json
{
  "intent": "get_low_stock",
  "brand_name": null,
  "store_name": "Lucknow Store 1",
  "threshold": null,
  "time_window_days": null
}
```

Default threshold injected (e.g., 50 units).

---

### Step 2 – Routing

Intent → `inventory_service.get_low_stock()`

---

### Step 3 – Aggregation

```
Compute stock per brand
Filter stock < threshold
```

---

### Step 4 – Response

> The following medicines are below 50 units in Lucknow Store 1: ...

---

### Example 4: Conversational Follow-Up

**Query 1**

> How much stock of Azithral 500 in Lucknow?

Memory updated:

```json
{
  "last_intent": "get_brand_stock_in_store",
  "brand_name": "Azithral 500",
  "store_name": "Lucknow"
}
```

---

**Query 2**

> What about Kanpur?

Intent extractor returns missing brand_name.

Memory fills brand_name automatically.

Backend executes:

```
get_brand_stock_in_store("Azithral 500", "Kanpur")
```

System maintains structured continuity.

---

## 6. Memory Model

Memory is session-based.

Stores:

- last_intent
- brand_name
- store_name
- time_window_days
- role

Memory does not:

- Store raw DB results
- Override role constraints
- Persist indefinitely

---

## 7. Security Model

The LLM:

- Cannot access DB
- Cannot modify DB
- Cannot bypass validation
- Cannot change role permissions

Backend enforces:

- Role restrictions
- Parameter validation
- Intent allow-list
- Schema validation
- Safe defaults

---

## 8. Performance Characteristics

Each query involves:

1. Intent extraction (LLM)
2. ORM aggregation query
3. Response formatting (LLM)

Primary latency source: LLM calls.

Database aggregation remains efficient with proper indexing.

---

## 9. PostgreSQL Migration Readiness

The system uses SQLAlchemy ORM exclusively.

Migration requires:

- Changing DATABASE_URL
- Adding production indexes
- Enabling connection pooling

No architectural changes required.

---

## 10. Architectural Classification

This system is not a prompt-based chatbot.

It is:

> A controlled AI orchestration layer over a transactional inventory engine.

---

## 11. Summary

The system cleanly separates:

- Language interpretation (LLM)
- Validation and control (Backend)
- Analytical computation (Database)
- Presentation (Formatter)
- Context retention (Memory)

AI assists the system.

It does not control it.
