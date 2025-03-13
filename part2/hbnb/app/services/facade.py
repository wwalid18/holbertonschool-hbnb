from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    """Facade to manage users, places, reviews, and amenities."""

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # -------- USER MANAGEMENT -------- #
    
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, updates):
        return self.user_repo.update(user_id, updates)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    # -------- PLACE MANAGEMENT -------- #

    def create_place(self, place_data, owner_id):
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Invalid owner ID.")
        
        place = Place(**place_data, owner=owner)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def update_place(self, place_id, updates):
        return self.place_repo.update(place_id, updates)

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # -------- REVIEW MANAGEMENT -------- #

    def create_review(self, review_data, place_id, user_id):
        place = self.get_place(place_id)
        user = self.get_user(user_id)

        if not place or not user:
            raise ValueError("Invalid place or user ID.")

        review = Review(**review_data, place=place, user=user)
        self.review_repo.add(review)
        if hasattr(place, "add_review"):
            place.add_review(review)  # Ensure place supports this
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)

    # -------- AMENITY MANAGEMENT -------- #

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def link_amenity_to_place(self, place_id, amenity_id):
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)

        if not place or not amenity:
            raise ValueError("Invalid place or amenity ID.")

        if hasattr(place, "add_amenity"):
            place.add_amenity(amenity)  # Ensure place supports this
        return place

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)
