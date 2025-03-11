from base_model import BaseModel
from place import Place
from user import User

class Review(BaseModel):
    """Represents a review for a place"""

    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("Review text cannot be empty")
        self.text = text

        if 1 <= rating <= 5:
            self.rating = rating
        else:
            raise ValueError("Rating must be between 1 and 5")

        if isinstance(place, Place):
            self.place = place
        else:
            raise ValueError("Review must be linked to a valid Place instance")

        if isinstance(user, User):
            self.user = user
        else:
            raise ValueError("Review must be written by a valid User instance")
