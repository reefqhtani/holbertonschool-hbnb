from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity class representing a facility or feature of a place"""
    
    def __init__(self, name, **kwargs):
        """
        Initialize a new Amenity instance
        
        Args:
            name (str): Name of the amenity
        """
        super().__init__(**kwargs)
        
        # Validate and set attributes
        self.name = name
        
        # Validate the attribute
        self._validate()
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        if len(value) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        self._name = value
    
    def _validate(self):
        """Validate amenity attribute"""
        # Trigger property setter to validate
        self.name = self._name
    

    def to_dict(self):
        """Convert amenity to dictionary"""
        amenity_dict = super().to_dict()
        # Add the name attribute (it has underscore prefix due to property)
        amenity_dict['name'] = self.name
        return amenity_dict

    def __str__(self):
        """String representation of Amenity"""
        return f"[Amenity] ({self.id}) {self.name}"
