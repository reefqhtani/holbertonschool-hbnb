#!/usr/bin/env python3
"""Unit tests for model validation"""
import unittest
import sys
sys.path.insert(0, '.')

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestUserModel(unittest.TestCase):
    """Test User model validation"""
    
    def setUp(self):
        """Create test data"""
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
    
    def test_create_valid_user(self):
        """Test creating a valid user"""
        user = User(**self.valid_data)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'john.doe@example.com')
    
    def test_invalid_first_name(self):
        """Test invalid first name"""
        with self.assertRaises(ValueError):
            User(first_name='', last_name='Doe', email='test@test.com', password='pass')
    
    def test_invalid_last_name(self):
        """Test invalid last name"""
        with self.assertRaises(ValueError):
            User(first_name='John', last_name='', email='test@test.com', password='pass')
    
    def test_invalid_email_empty(self):
        """Test empty email"""
        with self.assertRaises(ValueError):
            User(first_name='John', last_name='Doe', email='', password='pass')
    
    def test_invalid_email_format(self):
        """Test invalid email format"""
        with self.assertRaises(ValueError):
            User(first_name='John', last_name='Doe', email='invalid-email', password='pass')
    
    def test_email_too_long(self):
        """Test email exceeding max length"""
        long_email = 'a' * 40 + '@' + 'b' * 10 + '.com'
        with self.assertRaises(ValueError):
            User(first_name='John', last_name='Doe', email=long_email, password='pass')


class TestPlaceModel(unittest.TestCase):
    """Test Place model validation"""
    
    def setUp(self):
        """Create test owner"""
        self.owner = User(
            first_name='Owner',
            last_name='Test',
            email='owner@test.com',
            password='password'
        )
    
    def test_create_valid_place(self):
        """Test creating a valid place"""
        place = Place(
            title='Cozy Apartment',
            description='Nice place',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.owner
        )
        self.assertEqual(place.title, 'Cozy Apartment')
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.latitude, 40.7128)
    
    def test_invalid_title(self):
        """Test invalid title"""
        with self.assertRaises(ValueError):
            Place(title='', description='Test', price=100, latitude=0, longitude=0, owner=self.owner)
    
    def test_title_too_long(self):
        """Test title exceeding max length"""
        long_title = 'A' * 101
        with self.assertRaises(ValueError):
            Place(title=long_title, description='Test', price=100, latitude=0, longitude=0, owner=self.owner)
    
    def test_invalid_price_zero(self):
        """Test price zero"""
        with self.assertRaises(ValueError):
            Place(title='Test', description='Test', price=0, latitude=0, longitude=0, owner=self.owner)
    
    def test_invalid_price_negative(self):
        """Test negative price"""
        with self.assertRaises(ValueError):
            Place(title='Test', description='Test', price=-100, latitude=0, longitude=0, owner=self.owner)
    
    def test_invalid_latitude(self):
        """Test invalid latitude"""
        with self.assertRaises(ValueError):
            Place(title='Test', description='Test', price=100, latitude=91, longitude=0, owner=self.owner)
    
    def test_invalid_longitude(self):
        """Test invalid longitude"""
        with self.assertRaises(ValueError):
            Place(title='Test', description='Test', price=100, latitude=0, longitude=181, owner=self.owner)


class TestReviewModel(unittest.TestCase):
    """Test Review model validation"""
    
    def setUp(self):
        """Create test data"""
        self.owner = User(
            first_name='Owner',
            last_name='Test',
            email='owner@test.com',
            password='password'
        )
        self.place = Place(
            title='Test Place',
            description='Test',
            price=100,
            latitude=0,
            longitude=0,
            owner=self.owner
        )
        self.user = User(
            first_name='Reviewer',
            last_name='Test',
            email='reviewer@test.com',
            password='password'
        )
    
    def test_create_valid_review(self):
        """Test creating a valid review"""
        review = Review(
            text='Great place!',
            rating=5,
            place=self.place,
            user=self.user
        )
        self.assertEqual(review.text, 'Great place!')
        self.assertEqual(review.rating, 5)
    
    def test_invalid_text(self):
        """Test invalid text"""
        with self.assertRaises(ValueError):
            Review(text='', rating=5, place=self.place, user=self.user)
    
    def test_invalid_rating_low(self):
        """Test rating below 1"""
        with self.assertRaises(ValueError):
            Review(text='Test', rating=0, place=self.place, user=self.user)
    
    def test_invalid_rating_high(self):
        """Test rating above 5"""
        with self.assertRaises(ValueError):
            Review(text='Test', rating=6, place=self.place, user=self.user)
    
    def test_invalid_place_type(self):
        """Test invalid place type"""
        with self.assertRaises(ValueError):
            Review(text='Test', rating=5, place='not a place', user=self.user)
    
    def test_invalid_user_type(self):
        """Test invalid user type"""
        with self.assertRaises(ValueError):
            Review(text='Test', rating=5, place=self.place, user='not a user')


class TestAmenityModel(unittest.TestCase):
    """Test Amenity model validation"""
    
    def test_create_valid_amenity(self):
        """Test creating a valid amenity"""
        amenity = Amenity(name='Wi-Fi')
        self.assertEqual(amenity.name, 'Wi-Fi')
    
    def test_invalid_name(self):
        """Test invalid name"""
        with self.assertRaises(ValueError):
            Amenity(name='')
    
    def test_name_too_long(self):
        """Test name exceeding max length"""
        long_name = 'A' * 51
        with self.assertRaises(ValueError):
            Amenity(name=long_name)


if __name__ == '__main__':
    unittest.main()
