#!/usr/bin/env python3
import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_amenity_endpoints():
    """Test all amenity endpoints"""
    print("Testing Amenity Endpoints...")
    print("=" * 50)
    
    # Start server in background
    import subprocess
    import time
    import os
    
    # Kill any existing server
    os.system("pkill -f 'python3 run.py' 2>/dev/null")
    time.sleep(1)
    
    # Start server
    server = subprocess.Popen(["python3", "run.py"], 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
    time.sleep(3)  # Wait for server to start
    
    try:
        # 1. GET all amenities
        print("\n1. GET /api/v1/amenities/")
        response = requests.get(f"{BASE_URL}/api/v1/amenities/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            amenities = response.json()
            print(f"   Found {len(amenities)} amenities")
            for i, amenity in enumerate(amenities[:3]):  # Show first 3
                print(f"   {i+1}. {amenity['name']} (ID: {amenity['id']})")
        
        # 2. POST new amenity
        print("\n2. POST /api/v1/amenities/")
        new_amenity = {"name": "Test Gym Facility"}
        response = requests.post(f"{BASE_URL}/api/v1/amenities/", 
                                json=new_amenity)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            created = response.json()
            print(f"   Created: {created['name']} (ID: {created['id']})")
            new_id = created['id']
            
            # 3. GET specific amenity
            print(f"\n3. GET /api/v1/amenities/{new_id}")
            response = requests.get(f"{BASE_URL}/api/v1/amenities/{new_id}")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                amenity = response.json()
                print(f"   Retrieved: {amenity['name']}")
            
            # 4. PUT (update) amenity
            print(f"\n4. PUT /api/v1/amenities/{new_id}")
            update_data = {"name": "Updated Gym Name"}
            response = requests.put(f"{BASE_URL}/api/v1/amenities/{new_id}", 
                                   json=update_data)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                updated = response.json()
                print(f"   Updated to: {updated['name']}")
        
        # 5. Test error cases
        print("\n5. Testing error cases...")
        
        # Invalid POST (empty name)
        print("   a) POST with empty name:")
        response = requests.post(f"{BASE_URL}/api/v1/amenities/", 
                                json={"name": ""})
        print(f"      Status: {response.status_code} (expected: 400)")
        
        # GET non-existent amenity
        print("   b) GET non-existent amenity:")
        response = requests.get(f"{BASE_URL}/api/v1/amenities/nonexistent-id")
        print(f"      Status: {response.status_code} (expected: 404)")
        
        print("\n" + "=" * 50)
        print("✓ All amenity endpoint tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server. Make sure it's running on port 5000")
    finally:
        # Kill server
        server.terminate()
        server.wait()

if __name__ == "__main__":
    test_amenity_endpoints()
