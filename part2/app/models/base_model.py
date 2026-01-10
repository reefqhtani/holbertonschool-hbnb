import uuid
from datetime import datetime

class BaseModel:
    """Base class with common attributes and methods for all models"""
    
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # If kwargs is provided, set attributes from it
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    # Convert string to datetime if needed
                    if isinstance(value, str):
                        try:
                            value = datetime.fromisoformat(value)
                        except ValueError:
                            pass
                setattr(self, key, value)
    
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()
    
    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
    
    def to_dict(self):
        """Convert the object to a dictionary"""
        obj_dict = {}
        obj_dict['id'] = self.id
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        
        # Add other attributes that don't start with underscore
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if key not in ['id', 'created_at', 'updated_at']:  # Already added
                    if hasattr(value, 'isoformat'):  # Handle datetime objects
                        obj_dict[key] = value.isoformat()
                    else:
                        obj_dict[key] = value
        
        return obj_dict
    
    def __str__(self):
        """String representation of the object"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
