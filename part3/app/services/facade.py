from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.services.repositories.user_repository import UserRepository
from app.services.repositories.generic_repository import SQLAlchemyRepository
from app import db


class HBnBFacade:
    def __init__(self):
        # Repositories
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # --------------------
    # User Operations
    # --------------------
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, data, current_user):
        user = self.get_user(user_id)
        if not user:
            return None

        # Admin can modify everything
        if current_user.get('is_admin'):
            if 'password' in data:
                user.hash_password(data['password'])
            for key, value in data.items():
                setattr(user, key, value)
        else:
            # Regular user: can only modify own data except email/password
            if user.id != current_user.get('id'):
                raise PermissionError("Unauthorized action")
            if 'email' in data or 'password' in data:
                raise ValueError("You cannot modify email or password")
            for key, value in data.items():
                setattr(user, key, value)

        db.session.commit()
        return user

    # --------------------
    # Place Operations
    # --------------------
    def create_place(self, data, current_user):
        place = Place(**data)
        place.owner_id = current_user.get('id')
        self.place_repo.add(place)
        return place

    def update_place(self, place_id, data, current_user):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        is_admin = current_user.get('is_admin', False)
        if not is_admin and place.owner_id != current_user.get('id'):
            raise PermissionError("Unauthorized action")
        for key, value in data.items():
            setattr(place, key, value)
        db.session.commit()
        return place

    # --------------------
    # Review Operations
    # --------------------
    def create_review(self, data, current_user):
        place = self.place_repo.get(data.get('place_id'))
        if not place:
            raise ValueError("Place not found")

        if place.owner_id == current_user.get('id'):
            raise ValueError("You cannot review your own place")

        # Check if user already reviewed this place
        existing_review = self.review_repo.model.query.filter_by(
            user_id=current_user.get('id'), place_id=place.id
        ).first()
        if existing_review:
            raise ValueError("You have already reviewed this place")

        review = Review(**data)
        review.user_id = current_user.get('id')
        self.review_repo.add(review)
        return review

    def update_review(self, review_id, data, current_user):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        is_admin = current_user.get('is_admin', False)
        if not is_admin and review.user_id != current_user.get('id'):
            raise PermissionError("Unauthorized action")
        for key, value in data.items():
            setattr(review, key, value)
        db.session.commit()
        return review

    def delete_review(self, review_id, current_user):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        is_admin = current_user.get('is_admin', False)
        if not is_admin and review.user_id != current_user.get('id'):
            raise PermissionError("Unauthorized action")
        self.review_repo.delete(review_id)
        return review

    # --------------------
    # Amenity Operations (Admin Only)
    # --------------------
    def create_amenity(self, data, current_user):
        if not current_user.get('is_admin'):
            raise PermissionError("Admin privileges required")
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def update_amenity(self, amenity_id, data, current_user):
        if not current_user.get('is_admin'):
            raise PermissionError("Admin privileges required")
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        for key, value in data.items():
            setattr(amenity, key, value)
        db.session.commit()
        return amenity

    # --------------------
    # Public Place Operations
    # --------------------
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()
