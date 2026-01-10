from app.models.base_model import BaseModel

class Review(BaseModel):
    """Review class representing a review for a place"""
    
    def __init__(self, text, rating, place, user, **kwargs):
        """
        Initialize a new Review instance
        
        Args:
            text (str): Review text content
            rating (int): Rating from 1 to 5
            place (Place): Place being reviewed
            user (User): User who wrote the review
        """
        super().__init__(**kwargs)
        
        # Validate and set attributes
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        
        # Validate the attributes
        self._validate()
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Text must be a non-empty string")
        self._text = value
    
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value
    
    @property
    def place(self):
        return self._place
    
    @place.setter
    def place(self, value):
        from app.models.place import Place
        if not isinstance(value, Place):
            raise ValueError("Place must be a Place instance")
        self._place = value
    
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        from app.models.user import User
        if not isinstance(value, User):
            raise ValueError("User must be a User instance")
        self._user = value
    
    def _validate(self):
        """Validate all review attributes"""
        # Trigger property setters to validate
        self.text = self._text
        self.rating = self._rating
        self.place = self._place
        self.user = self._user
    
    def to_dict(self):
        """Convert review to dictionary"""
        review_dict = super().to_dict()
        
        # Remove empty lists that base class might have added
        if 'reviews' in review_dict:
            del review_dict['reviews']
        
        # Add review attributes (they have underscore prefixes due to properties)
        review_dict['text'] = self.text
        review_dict['rating'] = self.rating
        
        # Convert place and user to IDs for serialization
        if hasattr(self, '_place') and self._place:
            review_dict['place_id'] = self._place.id
        if hasattr(self, '_user') and self._user:
            review_dict['user_id'] = self._user.id
        
        return review_dict
    def __str__(self):
        """String representation of Review"""
        return f"[Review] ({self.id}) {self.rating}/5 - {self.text[:50]}..."
