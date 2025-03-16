from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Represents an amenity that can be associated with a place."""

    def __init__(self, name):
        super().__init__()  # Call BaseModel to generate ID and timestamps

        # Validate name (must be required and max 50 characters)
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string.")
        if len(name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters.")

        # Assign values
        self.name = name.strip()
        self.places = set()  # Many-to-Many relationship with Place

    def link_place(self, place):
        """Link this amenity to a place."""
        from app.models.place import Place  # Avoid circular import
        if isinstance(place, Place):
            self.places.add(place)
            place.add_amenity(self)  # Establish relationship
        else:
            raise ValueError("Invalid Place instance.")

    def __repr__(self):
        """Returns a readable string representation of the amenity."""
        return f"Amenity(Name: {self.name}, Linked Places: {len(self.places)})"
