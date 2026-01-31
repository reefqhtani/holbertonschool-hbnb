from app import db
from sqlalchemy.exc import IntegrityError

class SQLAlchemyRepository:
    """Generic repository for any SQLAlchemy model"""
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Data integrity error (e.g., duplicate entry)")
        except Exception as e:
            db.session.rollback()
            raise e

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj, data):
        # In SQLAlchemy, modifying the object attributes directly tracks changes.
        # We just need to commit.
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()
