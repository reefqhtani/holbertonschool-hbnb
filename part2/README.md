# HBnB - Part 2 (Business Logic + API) - Task 0

This directory contains the initial scaffold for **HBnB Part 2**, implementing the project structure and a minimal Flask + Flask-RESTx API foundation, along with an **in-memory repository** and a **Facade** entry point to decouple the Presentation and Business Logic layers from Persistence.

At this stage, persistence is implemented using in-memory storage. In Part 3, it will be replaced by a database-backed implementation (SQLAlchemy) without changing the API layer’s usage pattern.

---

## Project Structure

part2/
├─ README.md
├─ requirements.txt
├─ run.py
├─ smoke_test.py
└─ app/
├─ init.py
├─ config.py
├─ extensions.py
├─ api/
│ ├─ init.py
│ └─ v1/
│ ├─ init.py
│ ├─ routes.py
│ └─ namespaces/
│ ├─ init.py
│ └─ health.py
├─ business/
│ ├─ init.py
│ ├─ facade.py
│ └─ models/
│ ├─ init.py
│ └─ base.py
└─ persistence/
├─ init.py
└─ repository/
├─ init.py
├─ base_repository.py
└─ in_memory.py


### Layers

- **Presentation Layer**: `app/api/...` (Flask-RESTx namespaces/endpoints)
- **Business Logic Layer**: `app/business/...` (Facade + domain models)
- **Persistence Layer**: `app/persistence/...` (Repository interface + in-memory implementation)

---

## Requirements

- Python 3.10+
- Flask
- flask-restx

Dependencies are listed in `requirements.txt`.

---

## Setup

### 1) Create and activate a virtual environment

> Note: In some sandboxes, `python3-venv` must be installed first. If `venv` creation fails, install:
> `apt update && apt install -y python3.10-venv`

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
Running the Application
Development server

. .venv/bin/activate
python3 run.py
The API is configured with Swagger documentation at:

/docs

Important (Sandbox environments):
Some sandbox environments do not allow keeping a long-running server process alive or do not expose localhost ports for curl. If curl fails with "Connection refused", use the smoke test below.

Smoke Test (Recommended in Sandboxes)
A local “no-network” test using Flask’s test_client is provided in smoke_test.py.

Run:

. .venv/bin/activate
python3 smoke_test.py
Expected output:

STATUS: 200

JSON: {'status': 'ok'}

Implemented Endpoint (Task 0)
Health Check
GET /api/v1/health/

Response (200):

{ "status": "ok" }
Notes
Authentication (JWT) and role-based access control are intentionally not implemented in Part 2 Task 0.

The HBnBFacade is the intended interface the API will use to interact with the business logic and repositories.

The in-memory repository is designed to be replaced with SQLAlchemy repositories in Part 3 with minimal impact to the API layer.

