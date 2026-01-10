import re
from datetime import datetime
from app.models.base_model import BaseModel

class User(BaseModel):
    """User class representing a user in the system"""
    
    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        """
        Initialize a new User instance
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            email (str): User's email address
            password (str, optional): User's password
            is_admin (bool, optional): Whether user is admin. Defaults to False
        """
        super().__init__(**kwargs)
        
        # Validate and set attributes
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        
        # Validate the attributes
        self._validate()
    
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("First name must be a non-empty string")
        if len(value) > 50:
            raise ValueError("First name cannot exceed 50 characters")
        self._first_name = value
    
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Last name must be a non-empty string")
        if len(value) > 50:
            raise ValueError("Last name cannot exceed 50 characters")
        self._last_name = value
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Email must be a non-empty string")
        
        # Basic email validation regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise ValueError("Invalid email format")
        
        self._email = value
    
    @property
    def is_admin(self):
        return self._is_admin
    
    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        self._is_admin = value
    
    def _validate(self):
        """Validate all user attributes"""
        # Trigger property setters to validate
        self.first_name = self._first_name
        self.last_name = self._last_name
        self.email = self._email
        self.is_admin = self._is_admin
    
    def to_dict(self):
        """Convert user to dictionary, excluding password"""
        user_dict = super().to_dict()
        # Remove password from dictionary for security
        if 'password' in user_dict:
            del user_dict['password']
        if '_password' in user_dict:
            del user_dict['_password']
        return user_dict
    
    def verify_password(self, password):
        """Verify if the provided password matches the user's password"""
        if not self.password:
            return False
        return self.password == password
    
    def __str__(self):
        """String representation of User"""
        return f"[User] ({self.id}) {self.first_name} {self.last_name} - {self.email}"
