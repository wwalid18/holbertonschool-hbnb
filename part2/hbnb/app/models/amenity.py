class Place(BaseModel):
    """Represents a place owned by a User, with amenities."""

    def __init__(self, name, location, owner):
        super().__init__()
        self.name = self.validate_name(name)
        self.location = self.validate_location(location)
        self.owner = owner
        self.amenities = set()

        if not isinstance(owner, User):
            raise ValueError("Owner must be an instance of User.")
        owner.add_place(self)

    def add_amenity(self, amenity):
        """Link an amenity to this place."""
        if not isinstance(amenity, Amenity):
            raise ValueError("Invalid amenity instance.")
        self.amenities.add(amenity)
        amenity.places.add(self)

    @staticmethod
    def validate_name(name):
        """Ensure name is a valid non-empty string."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Place name is required and must be a non-empty string.")
        return name.strip()

    @staticmethod
    def validate_location(location):
        """Ensure location is a valid non-empty string."""
        if not isinstance(location, str) or not location.strip():
            raise ValueError("Location is required and must be a non-empty string.")
        return location.strip()

    def __repr__(self):
        return f"Place(Name: {self.name}, Location: {self.location}, Owner: {self.owner.first_name} {self.owner.last_name}, Amenities: {len(self.amenities)})"
