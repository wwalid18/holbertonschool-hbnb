from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ✅ User Methods
    def create_user(self, user_data):
        """Creates and stores a user in the repository."""
        user = User(**user_data)
        self.user_repo.add(user)  # ✅ Ensure user is stored
        print(f"✅ User created: {user.id}")
        return user

    def get_user(self, user_id):
        """Retrieves a user from the repository."""
        user = self.user_repo.get(user_id)
        if not user:
            print(f"❌ Error: User with ID {user_id} does not exist in repository!")
        return user

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, update_data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(update_data)
        return user
