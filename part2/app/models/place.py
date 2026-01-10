from .base_model import BaseModel


class Place(BaseModel):
    def __init__(self, name, description, owner_id):
        super().__init__()
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.amenities = []
