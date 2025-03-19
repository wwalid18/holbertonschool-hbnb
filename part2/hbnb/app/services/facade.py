from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    """Facade to manage business logic between API and repository."""

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    ###  User Methods ###
    def get_all_users(self):
        """Retrieve all users"""
        return self.user_repo.get_all()

    def create_user(self, user_data):
        """Create a new user and store it in the repository."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.user_repo.get_by_attribute('email', email)

    ### Amenity Methods ###
    def create_amenity(self, amenity_data):
        """Creates a new amenity and links it to a place."""
        print(f"Amenity data: {amenity_data}")  # Debug log

        # Fetch the place and user
        place_id = amenity_data['place_id']
        user_id = amenity_data['user_id']

        print(f"Fetching place with ID: {place_id}")  # Debug log
        place = self.place_repo.get(place_id)
        print(f"Place found: {place}")  # Debug log

        print(f"Fetching user with ID: {user_id}")  # Debug log
        user = self.user_repo.get(user_id)
        print(f"User found: {user}")  # Debug log

        # Ensure the place and user exist
        if not place:
            raise ValueError("Place not found.")
        if not user:
            raise ValueError("User not found.")

        # Ensure the user is the owner of the place
        if place.owner.id != user.id:
            raise ValueError("Only the owner of the place can add amenities.")

        # Ensure the amenity name is unique for the place
        existing_amenities = [a for a in self.amenity_repo.get_all() if a.place_id == place.id]
        if any(a.name == amenity_data['name'] for a in existing_amenities):
            raise ValueError("An amenity with this name already exists for the place.")

        # Create the amenity
        amenity = Amenity(name=amenity_data['name'], place_id=place.id)
        self.amenity_repo.add(amenity)

        # Link the amenity to the place
        amenity.link_place(place)

        return amenity

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by its ID."""
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        """Retrieves an amenity by its name."""
        return self.amenity_repo.get_by_attribute('name', name)

    def get_all_amenities(self):
        """Retrieves a list of all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Updates an amenity's details with validation."""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None  

        name = amenity_data.get('name', '').strip()
        if not name:
            raise ValueError("Amenity name cannot be empty")

        self.amenity_repo.update(amenity_id, {'name': name})
        return self.get_amenity(amenity_id)

    ### Place Methods ###
    def create_place(self, place_data):
        """Creates a new place with validation for price, location, and owner."""

        # Ensure the user is an admin
        owner = self.user_repo.get(place_data['owner_id'])
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

        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found.")

        amenities = []
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
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
            place.amenities.add(amenity)

        self.place_repo.add(place)
        return place.to_dict()  # Return the Place object as a dictionary

    def get_place(self, place_id):
        """Retrieves a place by ID, including its owner and amenities."""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        return place.to_dict()

    def get_all_places(self):
        """Retrieves a list of all places."""
        places = self.place_repo.get_all()
        return [self.get_place(place.id) for place in places]

    def update_place(self, place_id, place_data):
        """Updates an existing place with new data, ensuring valid input."""
        place = self.place_repo.get(place_id)
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
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    amenities.append(amenity)
            place.amenities = amenities

        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)

    ### Review Methods ###
    def create_review(self, review_data):
        """Creates a review with validation for user_id, place_id, and rating."""
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if field not in review_data or not review_data[field]:
                raise ValueError(f"Missing required field: {field}")

        if not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5.")

        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])
        if not user or not place:
            raise ValueError("User or Place not found.")

        review = Review(text=review_data['text'], rating=review_data['rating'], user=user, place=place)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieves all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieves all reviews for a specific place."""
        return [review for review in self.review_repo.get_all() if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        """Updates a review with validation."""
        review = self.review_repo.get(review_id)
        if not review:
            return None  

        if 'rating' in review_data and not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5.")

        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        """Deletes a review by its ID."""
        return self.review_repo.delete(review_id)
