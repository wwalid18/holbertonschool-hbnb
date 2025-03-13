class HBnBFacade:
    """Facade to manage users, places, reviews, and amenities."""

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # -------- USER MANAGEMENT -------- #
    
    def create_user(self, user_data):
        """Creates and stores a new user."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieves a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieves a user by email."""
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, updates):
        """Updates an existing user."""
        return self.user_repo.update(user_id, updates)

    def delete_user(self, user_id):
        """Deletes a user."""
        return self.user_repo.delete(user_id)

    # -------- PLACE MANAGEMENT -------- #

    def create_place(self, place_data, owner_id):
        """Creates a place and assigns an owner."""
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Invalid owner ID.")
        
        place = Place(**place_data, owner=owner)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieves a place by ID."""
        return self.place_repo.get(place_id)

    def update_place(self, place_id, updates):
        """Updates a place's details."""
        return self.place_repo.update(place_id, updates)

    def delete_place(self, place_id):
        """Deletes a place."""
        return self.place_repo.delete(place_id)

    # -------- REVIEW MANAGEMENT -------- #

    def create_review(self, review_data, place_id, user_id):
        """Creates a review for a place."""
        place = self.get_place(place_id)
        user = self.get_user(user_id)

        if not place or not user:
            raise ValueError("Invalid place or user ID.")

        review = Review(**review_data, place=place, user=user)
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        """Retrieves a review by ID."""
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        """Deletes a review."""
        return self.review_repo.delete(review_id)

    # -------- AMENITY MANAGEMENT -------- #

    def create_amenity(self, amenity_data):
        """Creates an amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def link_amenity_to_place(self, place_id, amenity_id):
        """Associates an amenity with a place."""
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)

        if not place or not amenity:
            raise ValueError("Invalid place or amenity ID.")

        place.add_amenity(amenity)
        return place

    def delete_amenity(self, amenity_id):
        """Deletes an amenity."""
        return self.amenity_repo.delete(amenity_id)
