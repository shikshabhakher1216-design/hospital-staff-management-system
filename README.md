# hospital-staff-management-system
"A secure RESTful API built with FastAPI, PostgreSQL, SQLAlchemy ORM, JWT Authentication, Bcrypt Password Hashing, and Role-Based Access Control (RBAC) for hospital staff administration."

# 🏥 Hospital Staff Management System API

A secure RESTful API built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy ORM**. Features password hashing with Bcrypt, JWT Token Authentication, pagination, filtering, and Role-Based Access Control (RBAC).

---

## 📌 Project Features

* **🔐 Security & Authentication:** Passwords hashed using `passlib` with `bcrypt`. User logins generate signed **JWT tokens** using `python-jose`.
* **🛡️ Role-Based Access Control (RBAC):** Restrict sensitive admin actions (assigning, updating, and deleting roles) strictly to authorized accounts (e.g., `Director`).
* **⚡ Search & Filtering:** Filter hospital staff records by `department` or search by `username`.
* **📄 Pagination:** Default paginated endpoints to fetch records efficiently using limit and offset parameters.
* **✅ Input Validation:** Built-in data validation using **Pydantic** models.

---

## 🧰 Tech Stack

* **Language:** Python
* **Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Authentication:** JWT (JSON Web Tokens), Passlib (Bcrypt)
* **Server:** Uvicorn

---

## 📁 Key File Descriptions

* **`database.py`**: Handles connection strings, engine creation, session generators (`SessionLocal`), and the `get_db` FastAPI dependency.
* **`models.py`**: Defines the `HospitalStaff` SQLAlchemy table structure (`id`, `username`, `password`, `role`, `department`).
* **`schemas.py`**: Contains Pydantic models (`HospitalStaff`, `LoginSchema`) for payload validation.
* **`main.py`**: Implements authentication flows, JWT token generation, CRUD endpoints, and RBAC authorization functions.

---
