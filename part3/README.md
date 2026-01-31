# HBnB Project - Part 3: Database Integration & Authentication

## Project Overview
Welcome to Part 3 of the HBnB project. In this phase, we have transitioned the backend from in-memory storage to a persistent **SQLite database** using **SQLAlchemy ORM**. We have also implemented robust **JWT Authentication** and **Role-Based Access Control (RBAC)** to secure the API.

This project is a RESTful API for a simplified Airbnb clone, allowing users to manage Users, Places, Reviews, and Amenities with proper data relationships.

## Key Features

### 1. Database Persistence (SQLAlchemy)
* Replaced in-memory storage with **SQLite** for development.
* Mapped entities (**User, Place, Review, Amenity**) to database tables.
* Established relationships:
    * **One-to-Many:** User ↔ Places, User ↔ Reviews, Place ↔ Reviews.
    * **Many-to-Many:** Place ↔ Amenities (via association table).

### 2. Authentication & Security
* **JWT Authentication:** Secure login using `Flask-JWT-Extended`.
* **Password Hashing:** Passwords are securely hashed using `bcrypt` before storage.
* **RBAC (Role-Based Access Control):**
    * **Admin:** Can manage all resources (Users, Amenities).
    * **Regular User:** Can only manage their own resources.
    * **Public:** Can view places and details.

## Project Structure
```text
holbertonschool-hbnb/
├── app/
│   ├── __init__.py          # App factory and DB configuration
│   ├── config.py            # Environment configurations
│   ├── models/              # SQLAlchemy Models
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── persistence/         # Database Repositories
│   │   └── repository.py    # Generic SQLAlchemy Repository
│   ├── services/            # Business Logic Layer
│   │   └── facade.py
│   └── api/                 # API Endpoints (Blueprints)
│       └── v1/
│           ├── users.py
│           ├── places.py
│           ├── reviews.py
│           └── amenities.py
├── instance/                # Contains the SQLite DB file
├── requirements.txt         # Python dependencies
├── run.py                   # Entry point
├── schema.sql               # SQL script for schema creation
└── seed.sql                 # SQL script for initial data
Installation & Setup
Clone the repository:

git clone [https://github.com/](https://github.com/)<your-username>/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3
Create a virtual environment:

python3 -m venv venv
source venv/bin/activate
Install dependencies:

pip install -r requirements.txt
Initialize the Database: Run the application to auto-generate the instance/development.db file:

python3 run.py
(Alternatively, you can use schema.sql and seed.sql to populate data manually).

Usage
Start the Flask server:

python3 run.py
The API will be available at: http://127.0.0.1:5000/

API Examples
1. Register a User:

curl -X POST "[http://127.0.0.1:5000/api/v1/users/](http://127.0.0.1:5000/api/v1/users/)" \
     -H "Content-Type: application/json" \
     -d '{"first_name": "John", "last_name": "Doe", "email": "john@example.com", "password": "securepass"}'
2. Login (Get Token):

curl -X POST "[http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)" \
     -H "Content-Type: application/json" \
     -d '{"email": "john@example.com", "password": "securepass"}'
3. Create a Place (Protected):

curl -X POST "[http://127.0.0.1:5000/api/v1/places/](http://127.0.0.1:5000/api/v1/places/)" \
     -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"title": "Cozy Cabin", "description": "Mountain view", "price": 150.0, "latitude": 34.0, "longitude": -118.0}'
Database Schema Design (ER Diagram)
The following diagram visualizes the relationships between the entities in the database.

erDiagram
    User {
        string id PK
        string email
        string password
        string first_name
        string last_name
        boolean is_admin
    }

    Place {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string user_id FK
    }

    Review {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
    }

    Amenity {
        string id PK
        string name
    }

    Place_Amenity {
        string place_id FK
        string amenity_id FK
    }

    %% Relationships
    User ||--o{ Place : "owns"
    User ||--o{ Review : "writes"
    Place ||--o{ Review : "has"
    Place }|..|{ Amenity : "features"
Technologies Used
Python 3.8+

Flask (Web Framework)

SQLAlchemy (ORM)

SQLite (Database)

Flask-JWT-Extended (Authentication)

Bcrypt (Password Hashing)

Mermaid.js (Documentation)

License
This project is part of the Holberton School curriculum.
