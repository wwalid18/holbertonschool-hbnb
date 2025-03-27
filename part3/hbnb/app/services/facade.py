from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.models.amenity import Amenity
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repository = SQLAlchemyRepository(User)
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

    # ---------- User Methods ----------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repository.add(user)
        return user

    def get_user_by_id(self, user_id):
        return self.user_repository.get(user_id)

    def get_all_users(self):
        return self.user_repository.get_all()

    def get_user_by_email(self, email):
        return self.user_repository.get_by_attribute('email', email)

    def update_user(self, user_id, data):
        """
        Update user details.
        Only allowed fields (e.g. first_name and last_name) should be in data.
        """
        user = self.user_repository.get(user_id)
        if not user:
            raise ValueError("User not found.")
        
        updated_user = self.user_repository.update(user_id, data)
        return updated_user

    # ---------- Place Methods ----------
    def create_place(self, place_data):
        owner = self.user_repository.get(place_data['owner_id'])
        if not owner or not owner.is_admin:
            raise ValueError("Only admin users can create places.")
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data or not place_data[field]:
                raise ValueError(f"Missing required field: {field}")
        if place_data['price'] <= 0:
            raise ValueError("Price must be a positive number.")
        if not (-90.0 <= place_data['latitude'] <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        if not (-180.0 <= place_data['longitude'] <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")

        # Optionally fetch amenities if provided
        amenities = []
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repository.get(amenity_id)
                if amenity:
                    amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ""),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
        for amenity in amenities:
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

    def update_place(self, place_id, place_data):
        place = self.place_repository.get(place_id)
        if not place:
            return None
        if 'price' in place_data and place_data['price'] <= 0:
            raise ValueError("Price must be a positive number.")
        if 'latitude' in place_data and not (-90.0 <= place_data['latitude'] <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        if 'longitude' in place_data and not (-180.0 <= place_data['longitude'] <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        if 'amenities' in place_data:
            amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repository.get(amenity_id)
                if amenity:
                    amenities.append(amenity)
            place.amenities = amenities
        self.place_repository.update(place_id, place_data)
        return self.get_place(place_id)

    # ---------- Amenity Methods ----------
    def create_amenity(self, amenity_data):
        place_id = amenity_data['place_id']
        user_id = amenity_data['user_id']
        place = self.place_repository.get(place_id)
        user = self.user_repository.get(user_id)
        if not place:
            raise ValueError("Place not found.")
        if not user:
            raise ValueError("User not found.")
        if place.owner.id != user.id:
            raise ValueError("Only the owner of the place can add amenities.")
        # Check for duplicate amenity name for the given place
        existing_amenities = [a for a in self.amenity_repository.get_all() if a.place_id == place.id]
        if any(a.name == amenity_data['name'] for a in existing_amenities):
            raise ValueError("An amenity with this name already exists for the place.")
        amenity = Amenity(name=amenity_data['name'], place_id=place.id)
        self.amenity_repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        name = amenity_data.get('name', '').strip()
        if not name:
            raise ValueError("Amenity name cannot be empty")
        self.amenity_repository.update(amenity_id, {'name': name})
        return self.get_amenity(amenity_id)

    # ---------- Review Methods ----------
    def create_review(self, review_data):
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if field not in review_data or not review_data[field]:
                raise ValueError(f"Missing required field: {field}")
        if not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        user = self.user_repository.get(review_data['user_id'])
        place = self.place_repository.get(review_data['place_id'])
        if not user or not place:
            raise ValueError("User or Place not found.")
        review = Review(text=review_data['text'], rating=review_data['rating'], user=user, place=place)
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        return [review for review in self.review_repository.get_all() if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repository.get(review_id)
        if not review:
            return None
        if 'rating' in review_data and not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        self.review_repository.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        return self.review_repository.delete(review_id)
