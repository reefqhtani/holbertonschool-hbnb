#!/bin/bash

# HBnB API Manual cURL Tests
# Start the server first: python3 run.py

BASE_URL="http://localhost:5000"

echo "HBnB API Manual cURL Tests"
echo "=========================="

# Test 1: Health endpoint
echo -e "\n1. Testing health endpoint:"
curl -s -X GET "$BASE_URL/api/v1/health/" | jq '.'

# Test 2: Get all users
echo -e "\n2. Testing GET /api/v1/users/:"
curl -s -X GET "$BASE_URL/api/v1/users/" | jq '.'

# Test 3: Create a user (valid)
echo -e "\n3. Testing POST /api/v1/users/ (valid):"
curl -s -X POST "$BASE_URL/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test.user@example.com",
    "password": "password123"
  }' | jq '.'

# Test 4: Create a user (invalid email)
echo -e "\n4. Testing POST /api/v1/users/ (invalid email):"
curl -s -X POST "$BASE_URL/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Invalid",
    "last_name": "Email",
    "email": "invalid-email",
    "password": "pass"
  }' | jq '.'

# Test 5: Get all places
echo -e "\n5. Testing GET /api/v1/places/:"
curl -s -X GET "$BASE_URL/api/v1/places/" | jq '.'

# Test 6: Get Swagger documentation
echo -e "\n6. Testing Swagger documentation:"
echo "   Swagger UI: $BASE_URL/api/v1/"
echo "   Swagger JSON: $BASE_URL/api/v1/swagger.json"

echo -e "\nTests completed. Check output above for results."
