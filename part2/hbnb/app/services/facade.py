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

    # ✅ Place Methods
    def create_place(self, place_data):
        """Create a new place"""
        print(f"🔹 Checking if user exists for owner_id {place_data['owner_id']}...")
        owner = self.get_user(place_data['owner_id'])  # ✅ Ensure user exists

        if not owner:
            print(f"❌ Error: User with ID {place_data['owner_id']} does not exist!")
            raise ValueError("❌ Error: Owner does not exist!")

        amenities = []
        for amenity_id in place_data['amenities']:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                print(f"❌ Error: Amenity with ID {amenity_id} does not exist!")
                raise ValueError(f"❌ Error: Amenity with ID {amenity_id} does not exist!")
            amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner,
        )
        place.amenities = amenities  # ✅ Assign amenities after validating

        self.place_repo.add(place)
        print(f"✅ Place '{place.title}' created successfully!")
        return place
