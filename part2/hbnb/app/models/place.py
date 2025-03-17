from app.models.base_model import BaseModel
from app.models.user import User  # Ensure User is imported

class Place(BaseModel):
    """Represents a rental place owned by a User."""

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()  # Call BaseModel to generate ID and timestamps

        # Validate title
        if not title or len(title) > 100:
            raise ValueError("Title is required (max 100 characters).")

        # Validate price (must be positive)
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number.")

        # Validate latitude and longitude
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")

        # Validate owner (must be a valid User instance)
        if not isinstance(owner, User):
            raise ValueError("Owner must be a valid User instance.")

        # Assign values
        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.price = float(price)
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # One-to-Many relationship with User
        self.reviews = []  # One-to-Many relationship with Review
        self.amenities = set()  # Many-to-Many relationship with Amenity

        # Link this place to the owner
        owner.add_place(self)

    def __repr__(self):
        """Returns a readable string representation of the place."""
        return f"Place(Title: {self.title}, Owner: {self.owner.first_name}, Price: {self.price}, Amenities: {len(self.amenities)})"
