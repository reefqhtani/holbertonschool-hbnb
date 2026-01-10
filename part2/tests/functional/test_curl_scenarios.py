#!/usr/bin/env python3
"""Functional tests simulating cURL scenarios"""
import subprocess
import json
import time
import os
import signal
import sys
sys.path.insert(0, '.')

class TestCurlScenarios:
    """Test scenarios using cURL commands (simulated)"""
    
    def setup_server(self):
        """Start the Flask server in background"""
        self.server_process = subprocess.Popen(
            ['python3', 'run.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        time.sleep(3)  # Wait for server to start
    
    def teardown_server(self):
        """Stop the Flask server"""
        os.killpg(os.getpgid(self.server_process.pid), signal.SIGTERM)
        self.server_process.wait()
    
    def run_curl(self, method, endpoint, data=None):
        """Simulate cURL command"""
        import requests
        url = f'http://localhost:5000{endpoint}'
        
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url)
        
        return response
    
    def test_user_creation_scenarios(self):
        """Test user creation scenarios"""
        print("\n=== User Creation Scenarios ===")
        
        # Valid user creation
        print("\n1. Valid user creation:")
        user_data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice.smith@example.com',
            'password': 'securepass123'
        }
        response = self.run_curl('POST', '/api/v1/users/', user_data)
        print(f"   Status: {response.status_code} (expected: 201)")
        if response.status_code == 201:
            data = response.json()
            print(f"   Created user ID: {data.get('id')}")
            print(f"   Email: {data.get('email')}")
        
        # Invalid email format
        print("\n2. Invalid email format:")
        user_data = {
            'first_name': 'Bob',
            'last_name': 'Jones',
            'email': 'invalid-email',
            'password': 'pass'
        }
        response = self.run_curl('POST', '/api/v1/users/', user_data)
        print(f"   Status: {response.status_code} (expected: 400)")
        
        # Empty fields
        print("\n3. Empty fields:")
        user_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': ''
        }
        response = self.run_curl('POST', '/api/v1/users/', user_data)
        print(f"   Status: {response.status_code} (expected: 400)")
    
    def test_place_creation_scenarios(self):
        """Test place creation scenarios"""
        print("\n=== Place Creation Scenarios ===")
        
        # First get a user ID
        response = self.run_curl('GET', '/api/v1/users/')
        if response.status_code == 200:
            users = response.json()
            if users:
                user_id = users[0]['id']
                
                # Valid place creation
                print("\n1. Valid place creation:")
                place_data = {
                    'title': 'Beautiful Beach House',
                    'description': 'Luxury beach house with ocean view',
                    'price': 300.0,
                    'latitude': 34.0522,
                    'longitude': -118.2437,
                    'owner_id': user_id
                }
                response = self.run_curl('POST', '/api/v1/places/', place_data)
                print(f"   Status: {response.status_code} (expected: 201)")
                if response.status_code == 201:
                    data = response.json()
                    print(f"   Created place ID: {data.get('id')}")
                    print(f"   Title: {data.get('title')}")
                    print(f"   Price: ${data.get('price')}")
                
                # Invalid price (negative)
                print("\n2. Invalid price (negative):")
                place_data = {
                    'title': 'Invalid Price Place',
                    'description': 'Test',
                    'price': -50.0,
                    'latitude': 40.7128,
                    'longitude': -74.0060,
                    'owner_id': user_id
                }
                response = self.run_curl('POST', '/api/v1/places/', place_data)
                print(f"   Status: {response.status_code} (expected: 400)")
                
                # Invalid latitude
                print("\n3. Invalid latitude:")
                place_data = {
                    'title': 'Invalid Lat Place',
                    'description': 'Test',
                    'price': 100.0,
                    'latitude': 95.0,
                    'longitude': -74.0060,
                    'owner_id': user_id
                }
                response = self.run_curl('POST', '/api/v1/places/', place_data)
                print(f"   Status: {response.status_code} (expected: 400)")
    
    def test_review_creation_scenarios(self):
        """Test review creation scenarios"""
        print("\n=== Review Creation Scenarios ===")
        
        # Get user and place IDs
        users_response = self.run_curl('GET', '/api/v1/users/')
        places_response = self.run_curl('GET', '/api/v1/places/')
        
        if users_response.status_code == 200 and places_response.status_code == 200:
            users = users_response.json()
            places = places_response.json()
            
            if users and places:
                user_id = users[0]['id']
                place_id = places[0]['id']
                
                # Valid review creation
                print("\n1. Valid review creation:")
                review_data = {
                    'text': 'Amazing place! Highly recommend.',
                    'rating': 5,
                    'user_id': user_id,
                    'place_id': place_id
                }
                response = self.run_curl('POST', '/api/v1/reviews/', review_data)
                print(f"   Status: {response.status_code} (expected: 201)")
                if response.status_code == 201:
                    data = response.json()
                    print(f"   Created review ID: {data.get('id')}")
                    print(f"   Rating: {data.get('rating')}/5")
                
                # Invalid rating (out of range)
                print("\n2. Invalid rating (0):")
                review_data = {
                    'text': 'Test review',
                    'rating': 0,
                    'user_id': user_id,
                    'place_id': place_id
                }
                response = self.run_curl('POST', '/api/v1/reviews/', review_data)
                print(f"   Status: {response.status_code} (expected: 400)")
                
                # Empty text
                print("\n3. Empty text:")
                review_data = {
                    'text': '',
                    'rating': 4,
                    'user_id': user_id,
                    'place_id': place_id
                }
                response = self.run_curl('POST', '/api/v1/reviews/', review_data)
                print(f"   Status: {response.status_code} (expected: 400)")
    
    def test_error_handling_scenarios(self):
        """Test error handling scenarios"""
        print("\n=== Error Handling Scenarios ===")
        
        # Get non-existent resource
        print("\n1. Get non-existent user:")
        response = self.run_curl('GET', '/api/v1/users/non-existent-id')
        print(f"   Status: {response.status_code} (expected: 404)")
        
        print("\n2. Get non-existent place:")
        response = self.run_curl('GET', '/api/v1/places/non-existent-id')
        print(f"   Status: {response.status_code} (expected: 404)")
        
        print("\n3. Get non-existent review:")
        response = self.run_curl('GET', '/api/v1/reviews/non-existent-id')
        print(f"   Status: {response.status_code} (expected: 404)")
        
        print("\n4. Get reviews for non-existent place:")
        response = self.run_curl('GET', '/api/v1/places/non-existent-id/reviews')
        print(f"   Status: {response.status_code} (expected: 404)")
    
    def test_swagger_documentation(self):
        """Test Swagger documentation endpoints"""
        print("\n=== Swagger Documentation ===")
        
        print("\n1. Swagger UI:")
        response = self.run_curl('GET', '/api/v1/')
        print(f"   Status: {response.status_code} (expected: 200)")
        
        print("\n2. Swagger JSON:")
        response = self.run_curl('GET', '/api/v1/swagger.json')
        print(f"   Status: {response.status_code} (expected: 200)")
        if response.status_code == 200:
            data = response.json()
            print(f"   API Title: {data.get('info', {}).get('title')}")
            print(f"   API Version: {data.get('info', {}).get('version')}")
            print(f"   Number of paths: {len(data.get('paths', {}))}")
    
    def run_all_tests(self):
        """Run all functional tests"""
        try:
            print("Starting functional tests (cURL scenarios)...")
            print("=" * 60)
            
            self.setup_server()
            
            self.test_user_creation_scenarios()
            self.test_place_creation_scenarios()
            self.test_review_creation_scenarios()
            self.test_error_handling_scenarios()
            self.test_swagger_documentation()
            
            print("\n" + "=" * 60)
            print("Functional tests completed successfully!")
            
        except Exception as e:
            print(f"Error during testing: {e}")
        finally:
            self.teardown_server()

if __name__ == '__main__':
    tester = TestCurlScenarios()
    tester.run_all_tests()
