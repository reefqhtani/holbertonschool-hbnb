#!/usr/bin/env python3
"""Integration tests for API endpoints"""
import unittest
import json
import sys
sys.path.insert(0, '.')

from app import create_app
from app.services import facade


class TestUserEndpoints(unittest.TestCase):
    """Test User API endpoints"""
    
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Get sample user for testing relationships
        self.users = facade.get_all_users()
        if self.users:
            self.sample_user_id = self.users[0].id
    
    def test_get_all_users(self):
        """Test GET /api/v1/users/"""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_create_user_valid(self):
        """Test POST /api/v1/users/ with valid data"""
        user_data = {
            'first_name': 'Integration',
            'last_name': 'Test',
            'email': 'integration.test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/v1/users/',
                                  json=user_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Integration')
        self.assertEqual(data['last_name'], 'Test')
        self.assertEqual(data['email'], 'integration.test@example.com')
        # Password should not be in response
        self.assertNotIn('password', data)
    
    def test_create_user_invalid_email(self):
        """Test POST /api/v1/users/ with invalid email"""
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid-email',
            'password': 'pass'
        }
        response = self.client.post('/api/v1/users/',
                                  json=user_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_empty_fields(self):
        """Test POST /api/v1/users/ with empty fields"""
        user_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': ''
        }
        response = self.client.post('/api/v1/users/',
                                  json=user_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_user_by_id(self):
        """Test GET /api/v1/users/<id>"""
        if hasattr(self, 'sample_user_id'):
            response = self.client.get(f'/api/v1/users/{self.sample_user_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['id'], self.sample_user_id)
    
    def test_get_nonexistent_user(self):
        """Test GET /api/v1/users/<id> with non-existent ID"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)


class TestPlaceEndpoints(unittest.TestCase):
    """Test Place API endpoints"""
    
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Get sample data for testing
        self.users = facade.get_all_users()
        self.places = facade.get_all_places()
        self.amenities = facade.get_all_amenities()
        
        if self.users:
            self.sample_user_id = self.users[0].id
        if self.places:
            self.sample_place_id = self.places[0].id
        if self.amenities:
            self.sample_amenity_ids = [a.id for a in self.amenities[:2]]
    
    def test_get_all_places(self):
        """Test GET /api/v1/places/"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        if data:
            # Should have basic fields only
            self.assertIn('id', data[0])
            self.assertIn('title', data[0])
            self.assertIn('latitude', data[0])
            self.assertIn('longitude', data[0])
    
    def test_create_place_valid(self):
        """Test POST /api/v1/places/ with valid data"""
        if hasattr(self, 'sample_user_id') and hasattr(self, 'sample_amenity_ids'):
            place_data = {
                'title': 'Integration Test Place',
                'description': 'A place created by integration tests',
                'price': 150.0,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': self.sample_user_id,
                'amenities': self.sample_amenity_ids
            }
            response = self.client.post('/api/v1/places/',
                                      json=place_data,
                                      content_type='application/json')
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertEqual(data['title'], 'Integration Test Place')
            self.assertEqual(data['price'], 150.0)
            self.assertIn('owner', data)
            self.assertIn('amenities', data)
    
    def test_create_place_invalid_price(self):
        """Test POST /api/v1/places/ with invalid price"""
        if hasattr(self, 'sample_user_id'):
            place_data = {
                'title': 'Invalid Price Place',
                'description': 'Test',
                'price': -100.0,  # Invalid negative price
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': self.sample_user_id
            }
            response = self.client.post('/api/v1/places/',
                                      json=place_data,
                                      content_type='application/json')
            self.assertEqual(response.status_code, 400)
    
    def test_create_place_invalid_latitude(self):
        """Test POST /api/v1/places/ with invalid latitude"""
        if hasattr(self, 'sample_user_id'):
            place_data = {
                'title': 'Invalid Lat Place',
                'description': 'Test',
                'price': 100.0,
                'latitude': 100.0,  # Invalid latitude
                'longitude': -74.0060,
                'owner_id': self.sample_user_id
            }
            response = self.client.post('/api/v1/places/',
                                      json=place_data,
                                      content_type='application/json')
            self.assertEqual(response.status_code, 400)
    
    def test_get_place_details(self):
        """Test GET /api/v1/places/<id>"""
        if hasattr(self, 'sample_place_id'):
            response = self.client.get(f'/api/v1/places/{self.sample_place_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['id'], self.sample_place_id)
            self.assertIn('owner', data)
            self.assertIn('amenities', data)
            self.assertIn('reviews', data)  # Should include reviews
    
    def test_get_place_reviews(self):
        """Test GET /api/v1/places/<id>/reviews"""
        if hasattr(self, 'sample_place_id'):
            response = self.client.get(f'/api/v1/places/{self.sample_place_id}/reviews')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)


class TestReviewEndpoints(unittest.TestCase):
    """Test Review API endpoints"""
    
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Get sample data
        self.users = facade.get_all_users()
        self.places = facade.get_all_places()
        
        if len(self.users) >= 2 and self.places:
            self.sample_user_id = self.users[1].id  # Use different user
            self.sample_place_id = self.places[0].id
    
    def test_get_all_reviews(self):
        """Test GET /api/v1/reviews/"""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_create_review_valid(self):
        """Test POST /api/v1/reviews/ with valid data"""
        if hasattr(self, 'sample_user_id') and hasattr(self, 'sample_place_id'):
            review_data = {
                'text': 'Integration test review',
                'rating': 5,
                'user_id': self.sample_user_id,
                'place_id': self.sample_place_id
            }
            response = self.client.post('/api/v1/reviews/',
                                      json=review_data,
                                      content_type='application/json')
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertEqual(data['text'], 'Integration test review')
            self.assertEqual(data['rating'], 5)
            self.assertEqual(data['user_id'], self.sample_user_id)
            self.assertEqual(data['place_id'], self.sample_place_id)
    
    def test_create_review_invalid_rating(self):
        """Test POST /api/v1/reviews/ with invalid rating"""
        if hasattr(self, 'sample_user_id') and hasattr(self, 'sample_place_id'):
            review_data = {
                'text': 'Test',
                'rating': 0,  # Invalid rating
                'user_id': self.sample_user_id,
                'place_id': self.sample_place_id
            }
            response = self.client.post('/api/v1/reviews/',
                                      json=review_data,
                                      content_type='application/json')
            self.assertEqual(response.status_code, 400)
    
    def test_create_review_empty_text(self):
        """Test POST /api/v1/reviews/ with empty text"""
        if hasattr(self, 'sample_user_id') and hasattr(self, 'sample_place_id'):
            review_data = {
                'text': '',  # Empty text
                'rating': 5,
                'user_id': self.sample_user_id,
                'place_id': self.sample_place_id
            }
            response = self.client.post('/api/v1/reviews/',
                                      json=review_data,
                                      content_type='application/json')
            self.assertEqual(response.status_code, 400)


class TestAmenityEndpoints(unittest.TestCase):
    """Test Amenity API endpoints"""
    
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Get sample data
        self.amenities = facade.get_all_amenities()
        if self.amenities:
            self.sample_amenity_id = self.amenities[0].id
    
    def test_get_all_amenities(self):
        """Test GET /api/v1/amenities/"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_create_amenity_valid(self):
        """Test POST /api/v1/amenities/ with valid data"""
        amenity_data = {'name': 'Integration Test Amenity'}
        response = self.client.post('/api/v1/amenities/',
                                  json=amenity_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        # Debug output if test fails
        if data.get('name') != 'Integration Test Amenity':
            print(f"DEBUG: Response data: {data}")
        self.assertEqual(data.get('name'), 'Integration Test Amenity')
    
    def test_create_amenity_empty_name(self):
        """Test POST /api/v1/amenities/ with empty name"""
        amenity_data = {'name': ''}
        response = self.client.post('/api/v1/amenities/',
                                  json=amenity_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_amenity_by_id(self):
        """Test GET /api/v1/amenities/<id>"""
        if hasattr(self, 'sample_amenity_id'):
            response = self.client.get(f'/api/v1/amenities/{self.sample_amenity_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['id'], self.sample_amenity_id)


if __name__ == '__main__':
    unittest.main()
