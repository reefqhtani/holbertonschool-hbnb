#!/usr/bin/env python3
"""Test API integration with new models"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services import facade

def test_api_with_new_models():
    print("Testing API integration with new models...")
    
    # Create Flask app
    app = create_app()
    
    with app.test_client() as client:
        # Test health endpoint
        response = client.get('/api/v1/health/')
        assert response.status_code == 200
        health_data = json.loads(response.data)
        print(f"  ✓ Health endpoint works: {health_data['status']}")
        print(f"     Counts: Users={health_data['counts']['users']}, "
              f"Places={health_data['counts']['places']}, "
              f"Reviews={health_data['counts']['reviews']}, "
              f"Amenities={health_data['counts']['amenities']}")
        
        # Test getting users
        response = client.get('/api/v1/users/')
        assert response.status_code == 200
        users = json.loads(response.data)
        print(f"  ✓ Users endpoint returns {len(users)} users")
        
        # Test getting places
        response = client.get('/api/v1/places/')
        assert response.status_code == 200
        places = json.loads(response.data)
        print(f"  ✓ Places endpoint returns {len(places)} places")
        
        # Test getting amenities
        response = client.get('/api/v1/amenities/')
        assert response.status_code == 200
        amenities = json.loads(response.data)
        print(f"  ✓ Amenities endpoint returns {len(amenities)} amenities")
        
        # Test getting reviews
        response = client.get('/api/v1/reviews/')
        assert response.status_code == 200
        reviews = json.loads(response.data)
        print(f"  ✓ Reviews endpoint returns {len(reviews)} reviews")
        
        # Test facade methods
        users = facade.get_all_users()
        print(f"  ✓ Facade returns {len(users)} users")
        
        places = facade.get_all_places()
        print(f"  ✓ Facade returns {len(places)} places")
        
        # Test relationships through facade
        if places:
            place = places[0]
            amenities = facade.get_place_amenities(place.id)
            print(f"  ✓ Place '{place.title}' has {len(amenities)} amenities")
            
            reviews = facade.get_reviews_by_place(place.id)
            print(f"  ✓ Place '{place.title}' has {len(reviews)} reviews")
        
        print("\n✓ All API integration tests passed!")
        return True

if __name__ == "__main__":
    test_api_with_new_models()
