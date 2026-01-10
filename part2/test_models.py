#!/usr/bin/env python3
"""Test the core business logic classes"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_user_creation():
    """Test User class creation and validation"""
    print("Testing User class...")
    
    # Test valid user creation
    user = User(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="password123",
        is_admin=False
    )
    
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin == False
    assert user.verify_password("password123")
    assert len(user.id) == 36  # UUID length
    print("  ✓ User creation successful")
    
    # Test validation
    try:
        user = User(first_name="", last_name="Doe", email="invalid")
        print("  ✗ Should have raised error for empty first name")
        return False
    except ValueError:
        print("  ✓ Properly validates empty first name")
    
    try:
        user = User(first_name="A" * 51, last_name="Doe", email="test@example.com")
        print("  ✗ Should have raised error for long first name")
        return False
    except ValueError:
        print("  ✓ Properly validates first name length")
    
    try:
        user = User(first_name="John", last_name="Doe", email="invalid-email")
        print("  ✗ Should have raised error for invalid email")
        return False
    except ValueError:
        print("  ✓ Properly validates email format")
    
    print("  ✓ All User tests passed!")
    return True

def test_place_creation():
    """Test Place class creation and validation"""
    print("\nTesting Place class...")
    
    # Create owner user first
    owner = User(
        first_name="Alice",
        last_name="Smith",
        email="alice.smith@example.com"
    )
    
    # Test valid place creation
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay in the city center",
        price=100.0,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    assert place.title == "Cozy Apartment"
    assert place.description == "A nice place to stay in the city center"
    assert place.price == 100.0
    assert place.latitude == 37.7749
    assert place.longitude == -122.4194
    assert place.owner == owner
    assert len(place.id) == 36
    print("  ✓ Place creation successful")
    
    # Test validation
    try:
        place = Place(title="", description="Test", price=100, latitude=0, longitude=0, owner=owner)
        print("  ✗ Should have raised error for empty title")
        return False
    except ValueError:
        print("  ✓ Properly validates empty title")
    
    try:
        place = Place(title="A" * 101, description="Test", price=100, latitude=0, longitude=0, owner=owner)
        print("  ✗ Should have raised error for long title")
        return False
    except ValueError:
        print("  ✓ Properly validates title length")
    
    try:
        place = Place(title="Test", description="Test", price=-100, latitude=0, longitude=0, owner=owner)
        print("  ✗ Should have raised error for negative price")
        return False
    except ValueError:
        print("  ✓ Properly validates price")
    
    try:
        place = Place(title="Test", description="Test", price=100, latitude=91.0, longitude=0, owner=owner)
        print("  ✗ Should have raised error for invalid latitude")
        return False
    except ValueError:
        print("  ✓ Properly validates latitude range")
    
    try:
        place = Place(title="Test", description="Test", price=100, latitude=0, longitude=181.0, owner=owner)
        print("  ✗ Should have raised error for invalid longitude")
        return False
    except ValueError:
        print("  ✓ Properly validates longitude range")
    
    print("  ✓ All Place tests passed!")
    return True

def test_review_creation():
    """Test Review class creation and validation"""
    print("\nTesting Review class...")
    
    # Create user and place first
    user = User(
        first_name="Bob",
        last_name="Johnson",
        email="bob.johnson@example.com"
    )
    
    place = Place(
        title="Test Place",
        description="Test description",
        price=50.0,
        latitude=40.7128,
        longitude=-74.0060,
        owner=user
    )
    
    # Test valid review creation
    review = Review(
        text="Great place to stay! Very comfortable and clean.",
        rating=5,
        place=place,
        user=user
    )
    
    assert review.text == "Great place to stay! Very comfortable and clean."
    assert review.rating == 5
    assert review.place == place
    assert review.user == user
    assert len(review.id) == 36
    print("  ✓ Review creation successful")
    
    # Test validation
    try:
        review = Review(text="", rating=5, place=place, user=user)
        print("  ✗ Should have raised error for empty text")
        return False
    except ValueError:
        print("  ✓ Properly validates empty text")
    
    try:
        review = Review(text="Test", rating=0, place=place, user=user)
        print("  ✗ Should have raised error for rating < 1")
        return False
    except ValueError:
        print("  ✓ Properly validates rating minimum")
    
    try:
        review = Review(text="Test", rating=6, place=place, user=user)
        print("  ✗ Should have raised error for rating > 5")
        return False
    except ValueError:
        print("  ✓ Properly validates rating maximum")
    
    print("  ✓ All Review tests passed!")
    return True

def test_amenity_creation():
    """Test Amenity class creation and validation"""
    print("\nTesting Amenity class...")
    
    # Test valid amenity creation
    amenity = Amenity(name="Wi-Fi")
    
    assert amenity.name == "Wi-Fi"
    assert len(amenity.id) == 36
    print("  ✓ Amenity creation successful")
    
    # Test validation
    try:
        amenity = Amenity(name="")
        print("  ✗ Should have raised error for empty name")
        return False
    except ValueError:
        print("  ✓ Properly validates empty name")
    
    try:
        amenity = Amenity(name="A" * 51)
        print("  ✗ Should have raised error for long name")
        return False
    except ValueError:
        print("  ✓ Properly validates name length")
    
    print("  ✓ All Amenity tests passed!")
    return True

def test_relationships():
    """Test relationships between entities"""
    print("\nTesting relationships...")
    
    # Create users
    owner = User(
        first_name="Sarah",
        last_name="Wilson",
        email="sarah.wilson@example.com"
    )
    
    reviewer = User(
        first_name="Mike",
        last_name="Brown",
        email="mike.brown@example.com"
    )
    
    # Create place
    place = Place(
        title="Beach House",
        description="Beautiful house by the beach",
        price=200.0,
        latitude=34.0522,
        longitude=-118.2437,
        owner=owner
    )
    
    # Create amenities
    wifi = Amenity(name="Wi-Fi")
    pool = Amenity(name="Pool")
    parking = Amenity(name="Parking")
    
    # Add amenities to place
    place.add_amenity(wifi)
    place.add_amenity(pool)
    place.add_amenity(parking)
    
    assert len(place.amenities) == 3
    assert wifi in place.amenities
    assert pool in place.amenities
    assert parking in place.amenities
    print("  ✓ Amenities added to place successfully")
    
    # Create reviews
    review1 = Review(
        text="Amazing view and great location!",
        rating=5,
        place=place,
        user=reviewer
    )
    
    review2 = Review(
        text="Could be cleaner, but good value for money.",
        rating=3,
        place=place,
        user=owner
    )
    
    # Add reviews to place
    place.add_review(review1)
    place.add_review(review2)
    
    assert len(place.reviews) == 2
    assert review1 in place.reviews
    assert review2 in place.reviews
    print("  ✓ Reviews added to place successfully")
    
    # Test to_dict() serialization
    place_dict = place.to_dict()
    assert 'owner_id' in place_dict
    assert 'review_ids' in place_dict
    assert 'amenity_ids' in place_dict
    assert len(place_dict['review_ids']) == 2
    assert len(place_dict['amenity_ids']) == 3
    print("  ✓ to_dict() serialization works correctly")
    
    print("  ✓ All relationship tests passed!")
    return True

def test_base_model():
    """Test BaseModel functionality"""
    print("\nTesting BaseModel...")
    
    from app.models.base_model import BaseModel
    
    # Create a simple test class
    class TestModel(BaseModel):
        def __init__(self, name, **kwargs):
            super().__init__(**kwargs)
            self.name = name
    
    # Test creation
    test = TestModel(name="Test")
    assert test.name == "Test"
    assert len(test.id) == 36
    assert test.created_at is not None
    assert test.updated_at is not None
    print("  ✓ BaseModel creation successful")
    
    # Test save method updates updated_at
    old_updated = test.updated_at
    import time
    time.sleep(0.001)  # Ensure time difference
    test.save()
    assert test.updated_at > old_updated
    print("  ✓ save() method updates updated_at")
    
    # Test update method
    test.update({"name": "Updated Name"})
    assert test.name == "Updated Name"
    assert test.updated_at > old_updated
    print("  ✓ update() method works correctly")
    
    # Test to_dict method
    test_dict = test.to_dict()
    assert test_dict['name'] == "Updated Name"
    assert test_dict['__class__'] == 'TestModel'
    assert 'id' in test_dict
    assert 'created_at' in test_dict
    assert 'updated_at' in test_dict
    print("  ✓ to_dict() method works correctly")
    
    print("  ✓ All BaseModel tests passed!")
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing Core Business Logic Classes")
    print("=" * 60)
    
    tests = [
        ("BaseModel", test_base_model),
        ("User", test_user_creation),
        ("Place", test_place_creation),
        ("Review", test_review_creation),
        ("Amenity", test_amenity_creation),
        ("Relationships", test_relationships),
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"✓ {test_name} tests PASSED\n")
            else:
                print(f"✗ {test_name} tests FAILED\n")
                all_passed = False
        except Exception as e:
            print(f"✗ {test_name} tests FAILED with error: {e}\n")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("SUCCESS: All core business logic classes are implemented correctly!")
        print("\nSummary:")
        print("  • BaseModel with UUID, created_at, updated_at ✓")
        print("  • User class with validation ✓")
        print("  • Place class with validation ✓")
        print("  • Review class with validation ✓")
        print("  • Amenity class with validation ✓")
        print("  • Relationships (User-Place, Place-Review, Place-Amenity) ✓")
        print("  • to_dict() serialization ✓")
        print("  • save() and update() methods ✓")
    else:
        print("FAILURE: Some tests failed. Review the output above.")
        sys.exit(1)
    
    print("=" * 60)

if __name__ == "__main__":
    main()
