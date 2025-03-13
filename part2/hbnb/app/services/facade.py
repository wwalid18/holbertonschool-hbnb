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

    """place methods"""
    def create_place(self, place_data):
        """
        Creates a new Place with validated attributes and stores it.
        """
        try:
            place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner_id=place_data['owner_id'],
                amenities=place_data.get('amenities', [])
            )
            return self.place_repository.save(place)
        except (ValueError, KeyError) as e:
            raise ValueError(f"Invalid place data: {str(e)}")

    def get_place(self, place_id):
        """
        Retrieves a Place by ID, including owner and amenities.
        """
        place = self.place_repository.get_by_id(place_id)
        if not place:
            return None
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": place.owner.to_dict(),
            "amenities": [amenity.to_dict() for amenity in place.amenities]
        }

    def get_all_places(self):
        """
        Retrieves all places with basic details.
        """
        places = self.place_repository.get_all()
        return [
            {
                "id": place.id,
                "title": place.title,
                "latitude": place.latitude,
                "longitude": place.longitude,
            }
            for place in places
        ]

    def update_place(self, place_id, place_data):
        """
        Updates an existing Place with new attributes.
        """
        place = self.place_repository.get_by_id(place_id)
        if not place:
            return None

        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        return self.place_repository.save(place)

    """review methods"""
    def create_review(self, review_data):
        """Creates a new review after validating user_id, place_id, and rating."""
        user = User.query.get(review_data['user_id'])
        place = Place.query.get(review_data['place_id'])
        
        if not user or not place:
            return None, "Invalid user or place ID"
        
        if not (1 <= review_data['rating'] <= 5):
            return None, "Rating must be between 1 and 5"
        
        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        )
        
        db.session.add(new_review)
        db.session.commit()
        return new_review, None

    def get_review(self, review_id):
        """Retrieves a review by ID."""
        return Review.query.get(review_id)

    def get_all_reviews(self):
        """Retrieves all reviews."""
        return Review.query.all()

    def get_reviews_by_place(self, place_id):
        """Retrieves all reviews for a specific place."""
        return Review.query.filter_by(place_id=place_id).all()

    def update_review(self, review_id, review_data):
        """Updates an existing review."""
        review = Review.query.get(review_id)
        if not review:
            return None, "Review not found"
        
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            if not (1 <= review_data['rating'] <= 5):
                return None, "Rating must be between 1 and 5"
            review.rating = review_data['rating']
        
        db.session.commit()
        return review, None

    def delete_review(self, review_id):
        """Deletes a review by ID."""
        review = Review.query.get(review_id)
        if not review:
            return None, "Review not found"
        
        db.session.delete(review)
        db.session.commit()
        return True, None
