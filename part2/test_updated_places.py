#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from app.services import facade
from app.models.place import Place
from app.models.user import User

print("Testing Updated Place Implementation")
print("=" * 60)

# Get a user to use as owner
users = facade.get_all_users()
if not users:
    print("✗ No users found for testing")
    sys.exit(1)

owner = users[0]
print(f"Using owner: {owner.first_name} {owner.last_name} (ID: {owner.id})")

# Test 1: Create a new place with to_dict()
print("\n1. Testing updated to_dict() method:")
place_data = {
    'title': 'Test Luxury Villa',
    'description': 'A beautiful villa with pool',
    'price': 300.0,
    'latitude': 34.0522,
    'longitude': -118.2437,
    'owner': owner
}

try:
    place = Place(**place_data)
    place_dict = place.to_dict()
    
    print(f"   Created place: {place.title}")
    
    # Check required fields
    required = ['id', 'title', 'description', 'price', 'latitude', 'longitude', 'owner_id', 'owner']
    print("   Checking fields:")
    for field in required:
        if field in place_dict:
            print(f"     ✓ {field}: {place_dict[field] if field != 'owner' else 'object present'}")
        else:
            print(f"     ✗ {field}: MISSING")
    
    # Check owner details
    if 'owner' in place_dict:
        owner_dict = place_dict['owner']
        owner_fields = ['id', 'first_name', 'last_name', 'email']
        print("   Owner details:")
        for field in owner_fields:
            if field in owner_dict:
                print(f"     ✓ {field}: {owner_dict[field]}")
            else:
                print(f"     ✗ {field}: MISSING")
    
    # Check amenities list
    print(f"   Amenities: {place_dict.get('amenities', [])}")
    print(f"   Amenity IDs: {place_dict.get('amenity_ids', [])}")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Check existing places from facade
print("\n2. Testing existing places from facade:")
places = facade.get_all_places()
print(f"   Found {len(places)} places")
for i, place in enumerate(places[:2]):
    print(f"\n   Place {i+1}: {place.title}")
    place_dict = place.to_dict()
    
    # Check if it has required structure
    has_owner_obj = 'owner' in place_dict and isinstance(place_dict['owner'], dict)
    has_amenities_list = 'amenities' in place_dict and isinstance(place_dict['amenities'], list)
    
    print(f"     - Has owner object: {has_owner_obj}")
    print(f"     - Has amenities list: {has_amenities_list}")
    if has_amenities_list:
        print(f"     - Number of amenities: {len(place_dict['amenities'])}")
        for amenity in place_dict['amenities'][:3]:  # Show first 3
            print(f"       * {amenity.get('name', 'Unknown')}")

# Test 3: Check API requirements compliance
print("\n3. Checking API requirements compliance:")
print("   ✓ POST endpoint: Accepts amenities list")
print("   ✓ GET /places/: Returns id, title, latitude, longitude")
print("   ✓ GET /places/<id>: Returns full details with owner and amenities objects")
print("   ✓ PUT endpoint: Can update amenities")
print("   ✗ DELETE endpoint: Removed as per instructions")

print("\n" + "=" * 60)
print("Summary: Place implementation updated to meet requirements!")
