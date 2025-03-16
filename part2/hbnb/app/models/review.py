from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    """Represents a review for a place written by a user."""

    def __init__(self, text, rating, place, user):
        super().__init__()  # Call BaseModel to generate ID and timestamps

        # Validate review text (must not be empty)
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string.")

        # Validate rating (must be an integer between 1 and 5)
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5.")

        # Validate place (must be an existing Place instance)
        if not isinstance(place, Place):
            raise ValueError("Place must be a valid Place instance.")

        # Validate user (must be an existing User instance)
        if not isinstance(user, User):
            raise ValueError("User must be a valid User instance.")

        # Assign values
        self.text = text.strip()
        self.rating = rating
        self.place = place  # One-to-Many relationship with Place
        self.user = user  # One-to-Many relationship with User

        # Link this review to the place
        place.add_review(self)

    def __repr__(self):
        """Returns a readable string representation of the review."""
        return f"Review(Rating: {self.rating}, Place: {self.place.title}, User: {self.user.first_name})"
