from app.persistence.user_repository import UserRepository
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        # Use the dedicated UserRepository for user-specific operations.
        self.user_repository = UserRepository()
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)
    
    # --- User Methods ---
    def create_user(self, user_data):
        """
        Create a new user.
        The User model automatically hashes the password in its constructor.
        """
        user = User(**user_data)
        self.user_repository.add(user)
        return user

    def get_user_by_email(self, email):
        """
        Retrieve a user by email using the UserRepository's get_by_email method.
        """
        return self.user_repository.get_by_email(email)

    def get_user_by_id(self, user_id):
        return self.user_repository.get(user_id)

    def get_all_users(self):
        return self.user_repository.get_all()

    def update_user(self, user_id, data):
        user = self.user_repository.get(user_id)
        if not user:
            raise ValueError("User not found.")
        updated_user = self.user_repository.update(user_id, data)
        return updated_user

    def reset_user_password(self, email, new_password):
        """
        Reset a user's password by delegating to the UserRepository.
        """
        return self.user_repository.reset_password(email, new_password)

    # --- Place Methods ---
    def create_place(self, place_data):
        owner = self.user_repository.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found.")
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ""),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repository.get(amenity_id)
                if amenity:
                    place.amenities.append(amenity)
        self.place_repository.add(place)
        return place.to_dict()

    def get_place(self, place_id):
        place = self.place_repository.get(place_id)
        if not place:
            return None
        return place.to_dict()

    def get_all_places(self):
        places = self.place_repository.get_all()
        return [self.get_place(place.id) for place in places]

    def update_place(self, place_id, data):
        place = self.place_repository.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        updated_place = self.place_repository.update(place_id, data)
        return self.get_place(place_id)

    def delete_place(self, place_id):
        if not self.place_repository.delete(place_id):
            raise ValueError("Failed to delete place.")
        return True

    # --- Review Methods ---
    def create_review(self, review_data):
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if field not in review_data or not review_data[field]:
                raise ValueError(f"Missing required field: {field}")
        user = self.user_repository.get(review_data['user_id'])
        place = self.place_repository.get(review_data['place_id'])
        if not user or not place:
            raise ValueError("User or Place not found.")
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def update_review(self, review_id, data):
        review = self.review_repository.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        updated_review = self.review_repository.update(review_id, data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        if not self.review_repository.delete(review_id):
            raise ValueError("Failed to delete review.")
        return True

    # --- Amenity Methods ---
    def create_amenity(self, amenity_data):
        amenity = Amenity(amenity_data['name'])
        self.amenity_repository.add(amenity)
        return amenity

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repository.get(amenity_id)
        if not amenity:
            return None
        self.amenity_repository.update(amenity_id, data)
        return self.amenity_repository.get(amenity_id)

    def delete_amenity(self, amenity_id):
        if not self.amenity_repository.delete(amenity_id):
            raise ValueError("Failed to delete amenity.")
        return True
