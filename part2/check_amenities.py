#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services import facade

amenities = facade.get_all_amenities()
print(f"Total amenities in facade: {len(amenities)}")
for i, amenity in enumerate(amenities):
    print(f"  {i+1}. {amenity.name} (ID: {amenity.id})")
