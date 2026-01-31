from app import db
from app.models.base_model import BaseModel

class Amenity(BaseModel, db.Model):
    """Amenity model for database"""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
