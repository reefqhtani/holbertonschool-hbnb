from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        
        # Initialize with some sample data for testing
        self._init_sample_data()
    
    def _init_sample_data(self):
        """Initialize with some sample data for testing"""
        # Sample users
        try:
            sample_users = [
                User(
                    first_name="John",
                    last_name="Doe",
                    email="john.doe@example.com",
                    password="password123"
                ),
                User(
                    first_name="Jane",
                    last_name="Smith",
                    email="jane.smith@example.com",
                    password="password456"
                ),
            ]
            for user in sample_users:
                self.user_repo.add(user)
        except Exception as e:
            print(f"Warning: Could not create sample users: {e}")
        
        # Sample amenities
        try:
            sample_amenities = [
                Amenity(name="Wi-Fi"),
                Amenity(name="Pool"),
                Amenity(name="Kitchen"),
                Amenity(name="Parking"),
                Amenity(name="Air Conditioning"),
            ]
            for amenity in sample_amenities:
                self.amenity_repo.add(amenity)
        except Exception as e:
            print(f"Warning: Could not create sample amenities: {e}")
        
        # Sample places (need at least one user first)
        try:
            users = self.user_repo.get_all()
            if users:
                owner = users[0]
                sample_places = [
                    Place(
                        title="Cozy Apartment",
                        description="A cozy apartment in the city center",
                        price=100.0,
                        latitude=40.7128,
                        longitude=-74.0060,
                        owner=owner
                    ),
                    Place(
                        title="Beach House",
                        description="Beautiful house by the beach",
                        price=200.0,
                        latitude=34.0522,
                        longitude=-118.2437,
                        owner=owner
                    ),
                ]
                for place in sample_places:
                    # Add some amenities to places
                    amenities = self.amenity_repo.get_all()
                    if len(amenities) >= 2:
                        place.add_amenity(amenities[0])
                        place.add_amenity(amenities[1])
                    self.place_repo.add(place)
        except Exception as e:
            print(f"Warning: Could not create sample places: {e}")
        
        # Sample reviews (need users and places first)
        try:
            users = self.user_repo.get_all()
            places = self.place_repo.get_all()
            if len(users) >= 2 and len(places) >= 2:
                reviewer = users[1]
                sample_reviews = [
                    Review(
                        text="Great place! Very comfortable.",
                        rating=5,
                        place=places[0],
                        user=reviewer
                    ),
                    Review(
                        text="Nice view but a bit noisy.",
                        rating=4,
                        place=places[1],
                        user=reviewer
                    ),
                ]
                for review in sample_reviews:
                    self.review_repo.add(review)
                    # Also add review to place
                    review.place.add_review(review)
        except Exception as e:
            print(f"Warning: Could not create sample reviews: {e}")
    
    # User methods
    def create_user(self, user_data):
        """Create a new user"""
        try:
            user = User(**user_data)
            self.user_repo.add(user)
            return user
        except Exception as e:
            raise ValueError(f"Failed to create user: {e}")
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)
    
    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()
    
    def update_user(self, user_id, data):
        """Update user"""
        user = self.get_user(user_id)
        if user:
            user.update(data)
            return user
        return None
    
    def delete_user(self, user_id):
        """Delete user"""
        self.user_repo.delete(user_id)
        return True
    
    def get_user_by_email(self, email):
        """Get user by email"""
        return self.user_repo.get_by_attribute('email', email)
    
    # Place methods
    def create_place(self, place_data):
        """Create a new place"""
        try:
            # Get owner from repository
            if 'owner_id' in place_data:
                owner = self.get_user(place_data['owner_id'])
                if not owner:
                    raise ValueError("Owner not found")
                place_data['owner'] = owner
                del place_data['owner_id']
            
            place = Place(**place_data)
            self.place_repo.add(place)
            return place
        except Exception as e:
            raise ValueError(f"Failed to create place: {e}")
    
    def get_place(self, place_id):
        """Get place by ID"""
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()
    
    def update_place(self, place_id, data):
        """Update place"""
        place = self.get_place(place_id)
        if place:
            place.update(data)
            return place
        return None
    
    def delete_place(self, place_id):
        """Delete place"""
        self.place_repo.delete(place_id)
        return True
    
    # Review methods
    def create_review(self, review_data):
        """Create a new review"""
        try:
            # Get place and user from repository
            if 'place_id' in review_data:
                place = self.get_place(review_data['place_id'])
                if not place:
                    raise ValueError("Place not found")
                review_data['place'] = place
                del review_data['place_id']
            
            if 'user_id' in review_data:
                user = self.get_user(review_data['user_id'])
                if not user:
                    raise ValueError("User not found")
                review_data['user'] = user
                del review_data['user_id']
            
            review = Review(**review_data)
            self.review_repo.add(review)
            # Also add review to place
            review.place.add_review(review)
            return review
        except Exception as e:
            raise ValueError(f"Failed to create review: {e}")
    
    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        place = self.get_place(place_id)
        if place:
            return place.get_reviews()
        return []
    
    def update_review(self, review_id, data):
        """Update review"""
        review = self.get_review(review_id)
        if review:
            review.update(data)
            return review
        return None
    
    def delete_review(self, review_id):
        """Delete review"""
        review = self.get_review(review_id)
        if review:
            # Remove from place first
            review.place.remove_review(review)
            self.review_repo.delete(review_id)
        return True
    
    # Amenity methods
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        try:
            amenity = Amenity(**amenity_data)
            self.amenity_repo.add(amenity)
            return amenity
        except Exception as e:
            raise ValueError(f"Failed to create amenity: {e}")
    
    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)
    
    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id, data):
        """Update amenity"""
        amenity = self.get_amenity(amenity_id)
        if amenity:
            amenity.update(data)
            return amenity
        return None
    
    def delete_amenity(self, amenity_id):
        """Delete amenity"""
        self.amenity_repo.delete(amenity_id)
        return True
    
    # Relationship methods
    def add_amenity_to_place(self, place_id, amenity_id):
        """Add an amenity to a place"""
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        if place and amenity:
            place.add_amenity(amenity)
            return True
        return False
    
    def remove_amenity_from_place(self, place_id, amenity_id):
        """Remove an amenity from a place"""
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        if place and amenity:
            place.remove_amenity(amenity)
            return True
        return False
    
    def get_place_amenities(self, place_id):
        """Get all amenities for a place"""
        place = self.get_place(place_id)
        if place:
            return place.get_amenities()
        return []
