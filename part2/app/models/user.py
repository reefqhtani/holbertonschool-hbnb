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
    
    def _validate(self):
        """Validate all user attributes"""
        # Validate first_name
        if not self.first_name or not isinstance(self.first_name, str):
            raise ValueError("First name must be a non-empty string")
        if len(self.first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters")
        
        # Validate last_name
        if not self.last_name or not isinstance(self.last_name, str):
            raise ValueError("Last name must be a non-empty string")
        if len(self.last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters")
        
        # Validate email
        if not self.email or not isinstance(self.email, str):
            raise ValueError("Email must be a non-empty string")
        
        # Check email length
        if len(self.email) > 50:
            raise ValueError("Email cannot exceed 50 characters")
        
        # Basic email validation regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, self.email):
            raise ValueError("Invalid email format")
        
        # Validate is_admin
        if not isinstance(self.is_admin, bool):
            raise ValueError("is_admin must be a boolean")
    
    def to_dict(self):
        """Convert user to dictionary, excluding password"""
        user_dict = super().to_dict()
        # Remove password from dictionary for security
        if 'password' in user_dict:
            del user_dict['password']
        return user_dict
    
    def verify_password(self, password):
        """Verify if the provided password matches the user's password"""
        if not self.password:
            return False
        return self.password == password
    
    def __str__(self):
        """String representation of User"""
        return f"[User] ({self.id}) {self.first_name} {self.last_name} - {self.email}"
