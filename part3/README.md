Holberton HBNB API
Project Overview

This project is a RESTful API for a simplified Airbnb clone (HBNB) that allows users to manage users, places, reviews, and amenities. It is built using Flask, SQLAlchemy, and JWT authentication. The API implements role-based access control (RBAC) with administrators and authenticated users, providing secure and flexible management of resources.

The project is designed in modular layers:

Models: SQLAlchemy ORM models for all entities (User, Place, Review, Amenity)

Repositories: Generic and entity-specific repositories for database operations

Facade: Service layer that interacts with repositories and encapsulates business logic

API Endpoints: Flask RESTful routes with JWT authentication and admin/user permissions

Features
1. Authentication & Authorization

JWT-based authentication using flask-jwt-extended

Role-based access:

Admin: Full control over users, places, reviews, and amenities

Authenticated User: Manage own places, reviews, and personal info

Public: Can view places and place details

2. Entities

User

Attributes: first_name, last_name, email, password, is_admin

Passwords are hashed using Flask-Bcrypt

Place

Attributes: title, description, price, latitude, longitude, owner_id

Review

Attributes: text, rating, user_id, place_id

Amenity

Attributes: name (unique)

3. Role-Based Endpoints

Public

GET /api/v1/places/ - List all places

GET /api/v1/places/<place_id> - Retrieve a place

Authenticated Users

Create, update, delete places (owned by user)

Create, update, delete reviews (own reviews only)

Update own user profile (excluding email and password)

Admins

Create and modify users (email/password allowed)

Create and modify amenities

Bypass ownership restrictions for places and reviews

Project Structure
holbertonschool-hbnb/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── persistence/
│   │   ├── repository.py
│   │   └── user_repository.py
│   ├── services/
│   │   └── facade.py
│   ├── api/
│   │   └── v1/
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   └── extensions.py
├── requirements.txt
├── run.py
└── README.md

Installation

Clone the repository:

git clone https://github.com/<your-username>/holbertonschool-hbnb.git
cd holbertonschool-hbnb


Create a virtual environment:

python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Set environment variables (optional):

export FLASK_APP=run.py
export FLASK_ENV=development
export SECRET_KEY="your_secret_key"


Initialize the database:

flask shell
>>> from app import db
>>> db.create_all()

Usage
Running the API:
flask run


The API will be available at: http://127.0.0.1:5000/api/v1/

Example Endpoints:
Public
curl -X GET "http://127.0.0.1:5000/api/v1/places/"

Authenticated User (JWT Token Required)
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
-H "Authorization: Bearer <JWT_TOKEN>" \
-H "Content-Type: application/json" \
-d '{"title": "New Place", "description": "Cozy apartment", "price": 100}'

Admin (JWT Token with is_admin=True)
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Authorization: Bearer <ADMIN_JWT>" \
-H "Content-Type: application/json" \
-d '{"first_name": "Admin", "last_name": "User", "email": "admin@example.com", "password": "password123"}'

Testing

Use Postman or cURL to test:

User registration and authentication

Place CRUD operations

Review CRUD operations

Amenity management

Admin-only actions

Technologies Used

Python 3

Flask

Flask-RESTX

Flask-JWT-Extended

Flask-Bcrypt

SQLAlchemy / Flask-SQLAlchemy

SQLite (development)

License

This project is for educational purposes for Holberton School and does not have an open-source license.
