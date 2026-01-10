#!/usr/bin/env python3
"""Test the full application"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing full application...")

# Test 1: Check all model files
print("\n1. Checking model files:")
model_files = ['base_model.py', 'user.py', 'place.py', 'review.py', 'amenity.py']
for file in model_files:
    path = f"app/models/{file}"
    if os.path.exists(path):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file}")

# Test 2: Check imports
print("\n2. Testing imports:")
try:
    from app.models import BaseModel, User, Place, Review, Amenity
    from app.services import facade
    from app import create_app
    print("  ✓ All imports successful")
except ImportError as e:
    print(f"  ✗ Import error: {e}")

# Test 3: Test model creation
print("\n3. Testing model creation:")
try:
    user = User(first_name="Test", last_name="User", email="test@example.com")
    print(f"  ✓ User created: {user.id}")
    
    place = Place(
        title="Test Place",
        description="Test description",
        price=100.0,
        latitude=40.0,
        longitude=-70.0,
        owner=user
    )
    print(f"  ✓ Place created: {place.id}")
    
    review = Review(
        text="Great place!",
        rating=5,
        place=place,
        user=user
    )
    print(f"  ✓ Review created: {review.id}")
    
    amenity = Amenity(name="Wi-Fi")
    print(f"  ✓ Amenity created: {amenity.id}")
    
    print("  ✓ All models can be created successfully")
except Exception as e:
    print(f"  ✗ Model creation error: {e}")

# Test 4: Test facade
print("\n4. Testing facade:")
try:
    users = facade.get_all_users()
    places = facade.get_all_places()
    reviews = facade.get_all_reviews()
    amenities = facade.get_all_amenities()
    
    print(f"  ✓ Facade has {len(users)} users")
    print(f"  ✓ Facade has {len(places)} places")
    print(f"  ✓ Facade has {len(reviews)} reviews")
    print(f"  ✓ Facade has {len(amenities)} amenities")
except Exception as e:
    print(f"  ✗ Facade error: {e}")

# Test 5: Test Flask app
print("\n5. Testing Flask app:")
try:
    app = create_app()
    print("  ✓ Flask app created successfully")
    
    # Count endpoints
    endpoint_count = len([r for r in app.url_map.iter_rules() if r.endpoint != 'static'])
    print(f"  ✓ App has {endpoint_count} registered endpoints")
except Exception as e:
    print(f"  ✗ Flask app error: {e}")

print("\n" + "="*60)
print("Application test complete!")
print("="*60)
