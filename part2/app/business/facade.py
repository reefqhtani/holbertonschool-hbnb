from app.persistence.repository import InMemoryRepository
from app.business.models.user import User


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, data):
        user = User(**data)
        return self.user_repo.add(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()
