from base_model import BaseModel
from user import User

class Place(BaseModel):
    """Represents a rental place"""

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        self.title = title[:100] if len(title) <= 100 else title[:100]

        self.description = description

        self.price = price if price > 0 else None

        self.latitude = latitude if -90.0 <= latitude <= 90.0 else None
        self.longitude = longitude if -180.0 <= longitude <= 180.0 else None

        if isinstance(owner, User):
            self.owner = owner
        else:
            raise ValueError("Owner must be a valid User instance")

        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
