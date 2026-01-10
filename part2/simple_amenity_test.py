#!/usr/bin/env python3
"""Simple test to verify amenity functionality without starting server"""

import sys
sys.path.insert(0, '.')

from app.services import facade
from app.models.amenity import Amenity

print("Testing Amenity Functionality Directly")
print("=" * 50)

# Test 1: Get all amenities
print("\n1. Testing get_all_amenities():")
amenities = facade.get_all_amenities()
print(f"   Found {len(amenities)} amenities")
for i, amenity in enumerate(amenities[:5]):
    print(f"   {i+1}. {amenity.name} (ID: {amenity.id})")

# Test 2: Create new amenity
print("\n2. Testing create_amenity():")
try:
    new_amenity_data = {"name": "Swimming Pool"}
    new_amenity = facade.create_amenity(new_amenity_data)
    print(f"   Created: {new_amenity.name} (ID: {new_amenity.id})")
    new_id = new_amenity.id
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Get specific amenity
print(f"\n3. Testing get_amenity('{new_id}'):")
amenity = facade.get_amenity(new_id)
if amenity:
    print(f"   Retrieved: {amenity.name}")
else:
    print("   Not found")

# Test 4: Update amenity
print(f"\n4. Testing update_amenity('{new_id}'):")
update_data = {"name": "Olympic Swimming Pool"}
updated = facade.update_amenity(new_id, update_data)
if updated:
    print(f"   Updated to: {updated.name}")
else:
    print("   Update failed")

# Test 5: Test validation
print("\n5. Testing validation:")
print("   a) Empty name:")
try:
    Amenity(name="")
    print("      Should have failed but didn't!")
except ValueError as e:
    print(f"      Correctly failed: {e}")

print("   b) Name too long:")
try:
    Amenity(name="A" * 51)
    print("      Should have failed but didn't!")
except ValueError as e:
    print(f"      Correctly failed: {e}")

print("   c) Valid name:")
try:
    Amenity(name="Valid Amenity")
    print("      Successfully created")
except ValueError as e:
    print(f"      Failed: {e}")

print("\n" + "=" * 50)
print("✓ Direct functionality tests completed!")
