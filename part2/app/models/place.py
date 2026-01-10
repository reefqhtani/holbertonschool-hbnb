from app.models.base_model import BaseModel

class Place(BaseModel):
    """Place class representing a rental property"""
    
    def __init__(self, title, description, price, latitude, longitude, owner, **kwargs):
        """
        Initialize a new Place instance
        
        Args:
            title (str): Title of the place
            description (str): Description of the place
            price (float): Price per night
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            owner (User): User who owns the place
        """
        super().__init__(**kwargs)
        
        # Validate and set attributes
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
        
        # Validate the attributes
        self._validate()
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string")
        if len(value) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        self._title = value
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("Description must be a string or None")
        self._description = value
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value <= 0:
            raise ValueError("Price must be positive")
        self._price = float(value)
    
    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number")
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self._latitude = float(value)
    
    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number")
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        self._longitude = float(value)
    
    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, value):
        # Import here to avoid circular imports
        from app.models.user import User
        if not isinstance(value, User):
            raise ValueError("Owner must be a User instance")
        self._owner = value
    
    def _validate(self):
        """Validate all place attributes"""
        # Trigger property setters to validate
        self.title = self._title
        self.description = self._description
        self.price = self._price
        self.latitude = self._latitude
        self.longitude = self._longitude
        self.owner = self._owner
    
    def add_review(self, review):
        """Add a review to the place"""
        from app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("Can only add Review instances")
        if review not in self.reviews:
            self.reviews.append(review)
    
    def remove_review(self, review):
        """Remove a review from the place"""
        if review in self.reviews:
            self.reviews.remove(review)
    
    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        from app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise ValueError("Can only add Amenity instances")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
    
    def remove_amenity(self, amenity):
        """Remove an amenity from the place"""
        if amenity in self.amenities:
            self.amenities.remove(amenity)
    
    def get_reviews(self):
        """Get all reviews for this place"""
        return self.reviews.copy()
    
    def get_amenities(self):
        """Get all amenities for this place"""
        return self.amenities.copy()
    
    def to_dict(self):
        """Convert place to dictionary"""
        place_dict = super().to_dict()
        # Convert owner to ID for serialization
        if hasattr(self, '_owner') and self._owner:
            place_dict['owner_id'] = self._owner.id
        # Convert reviews and amenities to IDs
        place_dict['review_ids'] = [review.id for review in self.reviews]
        place_dict['amenity_ids'] = [amenity.id for amenity in self.amenities]
        return place_dict
    
    def __str__(self):
        """String representation of Place"""
        return f"[Place] ({self.id}) {self.title} - ${self.price}/night"
