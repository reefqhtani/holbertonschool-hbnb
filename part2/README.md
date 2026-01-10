# HBnB API - Part 2

A RESTful API for the HBnB (Holberton BnB) application built with Flask and Flask-RESTx. This implementation follows a clean architecture with separation of concerns between Presentation, Business Logic, and Persistence layers.

## 🏗️ Architecture

The application follows a layered architecture:
┌─────────────────────────────────────────┐
│ Presentation Layer (API) │
│ app/api/v1/.py │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│ Business Logic Layer │
│ app/services/facade.py │
│ app/models/.py │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│ Persistence Layer │
│ app/persistence/repository.py │
└─────────────────────────────────────────┘

text

### Key Design Patterns:
- **Facade Pattern**: `HBnBFacade` provides a unified interface to the business logic
- **Repository Pattern**: Abstract data access layer for persistence
- **Dependency Injection**: Services are injected where needed

## 📋 Features

### Implemented Entities:
1. **Users** - System users with authentication
2. **Places** - Rental properties with location and pricing
3. **Reviews** - User reviews for places
4. **Amenities** - Features available at places

### CRUD Operations:
- ✅ **Users**: Create, Read, Update
- ✅ **Places**: Create, Read, Update (Delete not implemented as per requirements)
- ✅ **Reviews**: Create, Read, Update, Delete (only entity with delete)
- ✅ **Amenities**: Create, Read, Update (Delete bonus implementation)

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd holbertonschool-hbnb/part2
Install dependencies

bash
pip3 install -r requirements.txt
Run the application

bash
python3 run.py
The API will be available at http://localhost:5000

📚 API Documentation
Interactive Documentation
Swagger UI is automatically available at: http://localhost:5000/api/v1/

API Endpoints
Health Check
text
GET /api/v1/health/
Returns API health status and entity counts.

Users
text
GET    /api/v1/users/           # List all users
POST   /api/v1/users/           # Create a new user
GET    /api/v1/users/<id>       # Get user by ID
PUT    /api/v1/users/<id>       # Update user
Places
text
GET    /api/v1/places/           # List all places (basic info)
POST   /api/v1/places/           # Create a new place
GET    /api/v1/places/<id>       # Get place details with relationships
PUT    /api/v1/places/<id>       # Update place
GET    /api/v1/places/<id>/reviews  # Get reviews for a place
Reviews
text
GET    /api/v1/reviews/          # List all reviews
POST   /api/v1/reviews/          # Create a new review
GET    /api/v1/reviews/<id>      # Get review by ID
PUT    /api/v1/reviews/<id>      # Update review
DELETE /api/v1/reviews/<id>      # Delete review (only entity with delete)
Amenities
text
GET    /api/v1/amenities/        # List all amenities
POST   /api/v1/amenities/        # Create a new amenity
GET    /api/v1/amenities/<id>    # Get amenity by ID
PUT    /api/v1/amenities/<id>    # Update amenity
DELETE /api/v1/amenities/<id>    # Delete amenity (bonus implementation)
🔧 Validation Rules
User Validation
first_name: Required, non-empty string, max 50 characters

last_name: Required, non-empty string, max 50 characters

email: Required, valid email format, max 50 characters

password: Optional (excluded from API responses)

Place Validation
title: Required, non-empty string, max 100 characters

price: Must be positive number (> 0)

latitude: Must be between -90 and 90

longitude: Must be between -180 and 180

description: Optional string

Review Validation
text: Required, non-empty string

rating: Must be integer between 1 and 5 (inclusive)

user_id: Must reference existing user

place_id: Must reference existing place

Amenity Validation
name: Required, non-empty string, max 50 characters

🧪 Testing
Test Structure
text
tests/
├── unit/              # Unit tests for models
├── integration/       # Integration tests for API endpoints
└── functional/        # Functional tests (cURL scenarios)
Running Tests
Run All Tests
bash
python3 run_all_tests.py
Run Specific Test Categories
bash
# Unit tests only
python3 -m pytest tests/unit/ -v

# Integration tests only
python3 -m pytest tests/integration/ -v

# Run with coverage report
python3 -m pytest --cov=app tests/ --cov-report=html
Manual Testing with cURL
bash
# Make the script executable
chmod +x manual_curl_tests.sh

# Run manual tests (requires server running)
./manual_curl_tests.sh
Test Coverage
42 Total Tests (22 unit + 20 integration)

Model Validation: Comprehensive coverage

API Endpoints: All endpoints tested

Error Handling: 400 and 404 scenarios tested

Boundary Conditions: Edge cases validated

📁 Project Structure
text
part2/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── amenities.py     # Amenity endpoints
│   │       ├── health.py        # Health check endpoint
│   │       ├── places.py        # Place endpoints
│   │       ├── reviews.py       # Review endpoints
│   │       └── users.py         # User endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── amenity.py          # Amenity model
│   │   ├── base_model.py       # Base model with UUID/timestamps
│   │   ├── place.py            # Place model
│   │   ├── review.py           # Review model
│   │   └── user.py             # User model
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py       # Repository pattern implementation
│   └── services/
│       ├── __init__.py
│       └── facade.py           # Facade pattern implementation
├── tests/
│   ├── unit/
│   │   └── test_models.py      # Unit tests for models
│   ├── integration/
│   │   └── test_api_endpoints.py # Integration tests
│   └── functional/
│       └── test_curl_scenarios.py # Functional tests
├── run.py                       # Application entry point
├── config.py                    # Configuration
├── requirements.txt             # Dependencies
├── run_all_tests.py            # Test runner
├── manual_curl_tests.sh        # Manual test script
└── README.md                   # This file
🎯 Key Implementation Details
1. BaseModel Class
Automatic UUID generation for all entities

Created/updated timestamps

Common to_dict() serialization method

Update method for partial updates

2. Relationship Handling
Places have owners (User references)

Places have amenities (many-to-many)

Places have reviews (one-to-many)

Reviews reference both User and Place

3. Error Handling
400 Bad Request for validation errors

404 Not Found for non-existent resources

201 Created for successful resource creation

200 OK for successful operations

4. Sample Data
The application initializes with sample data for testing:

2 sample users

2 sample places (with amenities)

2 sample reviews

5 sample amenities

📊 Example Requests
Create a User
bash
curl -X POST "http://localhost:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "password123"
  }'
Create a Place with Amenities
bash
curl -X POST "http://localhost:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "user-uuid-here",
    "amenities": ["amenity-uuid-1", "amenity-uuid-2"]
  }'
Create a Review
bash
curl -X POST "http://localhost:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place! Very comfortable.",
    "rating": 5,
    "user_id": "user-uuid-here",
    "place_id": "place-uuid-here"
  }'
🔍 Troubleshooting
Common Issues
Port already in use

bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9
Import errors

bash
# Ensure you're in the correct directory
cd /path/to/holbertonschool-hbnb/part2

# Install dependencies
pip3 install -r requirements.txt
Test failures

bash
# Run tests with verbose output
python3 -m pytest tests/ -v

# Check for Python path issues
export PYTHONPATH=/path/to/holbertonschool-hbnb/part2:$PYTHONPATH
📝 Development Notes
Design Decisions
No DELETE for Places/Amenities: Following project requirements

Password exclusion: Passwords are never returned in API responses

In-memory storage: Uses repository pattern for easy switching to database

Property decorators: Used for validation in models

Future Improvements
Add database persistence (SQLAlchemy)

Implement authentication/authorization

Add search/filtering endpoints

Implement pagination

Add image upload support

Implement caching

👥 Contributors
This project was developed as part of the Holberton School curriculum.

📄 License
This project is for educational purposes as part of the Holberton School curriculum.
