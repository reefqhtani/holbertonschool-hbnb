from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, name, description, owner):
        super().__init__()
        self.name = name
        self.description = description
        self.owner = owner  # should be a User object
        self.amenities = []  # list of Amenity objects
        self.reviews = []    # list of Review objects

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        self.reviews.append(review)
