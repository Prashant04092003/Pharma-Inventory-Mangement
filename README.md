# Pharma-Inventory-Mangement

A ledger-based pharmaceutical inventory backend with a deterministic AI chatbot interface for natural language inventory queries.

This project simulates a production-style pharmaceutical inventory system and demonstrates how an AI assistant can safely interact with structured business data without directly accessing the database.

---

# Project Overview

The system models a multi-store pharmaceutical inventory environment and exposes both:

- A structured REST API
- A controlled AI chatbot interface

The chatbot interprets user queries in natural language, converts them into structured intent, and retrieves inventory insights through validated backend logic.

The AI model **never accesses the database directly**, ensuring deterministic and secure system behavior.

---

# Key Features

### Inventory System
- Ledger-based stock computation (`SUM(IN) - SUM(OUT)`)
- Batch-level pharmaceutical tracking
- Multi-store inventory distribution
- Expiry and cost tracking
- Realistic transaction simulation

### AI Chatbot Layer
- Natural language inventory queries
- Structured intent extraction using LLM
- Deterministic backend routing
- Role-aware access validation
- Conversational session memory

### Backend Infrastructure
- FastAPI REST API
- SQLAlchemy ORM
- Layered architecture
- PostgreSQL-ready design
- OpenAPI documentation

---

# System Architecture

```
User (Streamlit / UI)
        ↓
FastAPI Chat Endpoint
        ↓
ChatService (Orchestration Layer)
        ↓
Intent Extraction (LLM)
        ↓
Validator + Intent Router
        ↓
Inventory Service
        ↓
SQLAlchemy ORM
        ↓
Ledger-Based Inventory Database
        ↓
Response Formatter (LLM)
        ↓
Final Response
```

### Design Principle

AI interprets language.

Backend controls logic.

Database performs computation.

---

# Inventory Data Model

The system follows a **ledger-based transaction model**.

Stock is not stored directly.

Current Stock = SUM(IN transactions) − SUM(OUT transactions)


### Advantages

- Prevents stock corruption
- Enables historical reconstruction
- Supports turnover analytics
- Enables time-window queries
- Provides auditability

---

# Database Entities

Core tables:

- `manufacturers`
- `generic_medicines`
- `brand_medicines`
- `warehouses`
- `stores`
- `users`
- `batches`
- `transactions`

### Dataset Statistics

- 871 manufacturers
- 571 generics
- 8000 brand medicines
- 15 stores
- 1 central warehouse
- 24 months simulated
- ~541,000 transactions

---

# Example Queries

### Store Stock Lookup
How much stock of Azithral 500 is available in Lucknow Store 1?

### Cross Store Comparison

Which store has the lowest stock of Azithral 500 in the last 30 days?

### Low Stock Detection

Show low stock medicines in Lucknow Store 1

### Conversational Follow-up

How much Azithral 500 in Lucknow?
What about Kanpur?


The system maintains session memory to resolve follow-up queries.

---

# Security Model

The AI model **does not interact with the database directly**.

All queries follow this pipeline:

1. Intent extraction (LLM)
2. Validation layer
3. Intent routing
4. Deterministic backend logic
5. Database aggregation
6. Response formatting

This prevents:

- SQL injection
- AI hallucination errors
- Unauthorized data access
- Prompt injection attacks

---

# Tech Stack

Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite (Prototype)
- PostgreSQL-ready

AI Layer

- LLM-based intent extraction
- Structured response formatting

Data

- CSV ingestion
- Transaction simulation

Frontend (optional)

- Streamlit chatbot interface

---

# Project Structure
```
project/
│
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes_chat.py
│   │
│   ├── services/
│   │   ├── chat_service.py
│   │   ├── inventory_service.py
│   │   └── memory_service.py
│   │
│   ├── router/
│   │   ├── intent_router.py
│   │   └── validator.py
│   │
│   ├── llm/
│   │   ├── intent_extractor.py
│   │   ├── response_formatter.py
│   │   └── llm_client.py
│   │
│   ├── schemas/
│   │   ├── chat_schema.py
│   │   ├── intent_schema.py
│   │   └── response_schema.py
│   │
│   └── core/
│       └── settings.py
│
├── data/
├── scripts/
├── pharma.db
├── requirements.txt
└── README.md
```


---

x
---

# Performance Characteristics

Each chatbot query involves:

1. Intent extraction (LLM)
2. ORM aggregation query
3. Response formatting (LLM)

Database aggregation remains efficient due to ledger indexing.

Primary latency source is LLM inference.

---

# PostgreSQL Migration

The system is designed to be database-agnostic.

To migrate:

1. Update `DATABASE_URL`
2. Apply migrations
3. Add production indexes
4. Enable connection pooling

No architectural changes are required.

---

# Project Classification

This is **not a prompt-based chatbot**.

It is a **controlled AI orchestration layer over a transactional inventory engine**.

The system demonstrates how AI can safely interact with enterprise data systems while maintaining deterministic behavior.

---

# Future Improvements

- Redis-based conversational memory
- Query caching
- Async DB connection pooling
- Dashboard analytics
- Deployment using Docker
- Authentication layer

---

# Author

Prashant  
MSc Statistics & Data Science  
AI / Data Science
