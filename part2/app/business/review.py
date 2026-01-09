from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, user, place, text):
        super().__init__()
        self.user = user      # User object
        self.place = place    # Place object
        self.text = text
