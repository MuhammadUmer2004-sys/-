🧾 Bazaar Inventory Tracking System
This repository documents the development of a scalable Inventory Tracking System built in Python, evolving from a single-store CLI prototype to a multi-store, production-ready backend platform. This solution was designed in response to the Bazaar Technologies engineering challenge focusing on real-time stock visibility, scalability, auditability, and reliability.

1)Design Decisions:

Language & Framework
    Used Python for its readability, rapid prototyping capabilities, and extensive ecosystem.
    Chose Flask for REST API development in later stages due to its simplicity and flexibility.

Architecture
    Adopted a modular design separating core logic, API layer, and database access.
    Designed for evolution across three stages: CLI ➝ REST API ➝ Scalable Service.
    Used SQLite in Stage 1 for simplicity, transitioning to PostgreSQL for Stage 2+, ensuring relational integrity and scalability.

Data Modeling
    Modeled Products, StockMovements, and Stores (added in Stage 2).
    Central Product Catalog added in Stage 2 to ensure consistency across stores.
    Introduced AuditLogs in Stage 3 for traceability.

Security & Reliability
    Implemented basic authentication in Stage 2 and rate limiting using Flask-Limiter.
    In Stage 3, designed for horizontal scalability and asynchronous processing using event queues (e.g., RabbitMQ/Kafka).

2)Assumptions
    Each product has a unique global ID.
    A stock movement can be of type: stock-in, sale, or manual-removal.
    Stage 1 uses local SQLite; Stage 2+ uses PostgreSQL.
    Stage 2 introduces multiple stores, and each store maintains its own stock ledger.
    Stage 3 includes concurrent operations, event-driven architecture, and audit logs.

3)API Design (Stage 2 & 3)
Endpoint	                             Method	               Description
/products	                              GET	         Get list of products (global catalog)
/products	                              POST	           Add a new product
/stores	                                      GET	            List all stores
/stores/<store_id>/stock	              GET	         Get stock levels for a store
/stores/<store_id>/stock	              POST	         Create a stock movement (in, sale, removal)
/audit	                                      GET	          View audit logs (Stage 3)
/products/<product_id>	                      GET	         Get details of a specific product
/products/<product_id>	                      PUT	         Update an existing product
/products/<product_id>	                     DELETE	         Delete a product from the catalog
/stores	                                      POST	             Add a new store
/stores/<store_id>	                      PUT	            Update store details
/stores/<store_id>	                     DELETE	            Remove a store from the system
/stores/<store_id>/stock/<product_id>	      GET	            Get stock level for a specific product in a store
/stock-transfers	                      POST	            Transfer stock between two stores
/audit/<store_id>	                      GET	             View audit logs for a specific store (Stage 3)


Add New Product

{
  "product_id": 102,
  "name": "Sugar 1kg",
  "category": "Grocery",
  "unit": "pack"
}

🔸 Update Stock Movement (Manual Removal)

{
  "product_id": 101,
  "store_id": 2,
  "quantity": 3,
  "movement_type": "manual-removal"
}

🔸 Stock Transfer

{
  "product_id": 103,
  "from_store_id": 1,
  "to_store_id": 2,
  "quantity": 10
}

Sample Stock Movement Payload

{
  "product_id": 101,
  "store_id": 1,
  "quantity": 5,
  "movement_type": "stock-in"
}
My POSTMAN api's:
https://coding-4604.postman.co/workspace/My-Workspace~4acd02d2-e4b1-4f49-8048-dbb5dfd6bc28/collection/38889572-02c1d636-cc55-448e-9ef4-5bf5fa40e487?action=share&creator=38889572

1)http://127.0.0.1:5000/stock-movement
2)http://127.0.0.1:5000/products
3)http://127.0.0.1:5000/products
4)http://127.0.0.1:5000/stock-movement
5)http://127.0.0.1:8000/products/
6)http://127.0.0.1:8000/products/



🧬 Evolution Rationale (v1 → v3)
1) Stage 1: Single Store – CLI or Basic API

    CLI-based or basic REST API using Flask + SQLite.
    Tracks product entries, stock-in, sales, and manual removal.
    All data stored locally in a single flat file or SQLite database.
    Focus: core inventory logic and product model.

2) Stage 2: Multi-Store Support
    Transitioned to PostgreSQL to manage relational data efficiently.
    Added store-specific stock, central product catalog.
    Introduced REST API with filtering (by date/store/product).

    Added:
        Authentication (Basic Auth)
        Rate limiting for APIs
        Reporting APIs per store or product
       Ensures system can scale to 500+ stores with centralized control.

3) Stage 3: Scalable & Auditable Platform
    Designed for thousands of stores and high concurrency.

    Introduced:
        Asynchronous stock updates via event queues (Kafka/RabbitMQ)
        Read/write DB separation, caching, rate limiting
        Audit logging for all inventory changes
        Horizontal scalability considerations using container orchestration
        Deployed in a microservices-ready structure.
