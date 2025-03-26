from app.models.base_model import BaseModel
from app.models.place import Place

class Amenity(BaseModel):
    """Represents an amenity that can be associated with a place."""

    def __init__(self, name, place_id):
        super().__init__()  # Call BaseModel to generate ID and timestamps

        # Validate name (must be required and max 50 characters)
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string.")
        if len(name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters.")

        # Validate place_id (must be provided)
        if not place_id:
            raise ValueError("Place ID is required.")

        # Assign values
        self.name = name.strip()
        self.place_id = place_id # Link the amenity to a specific place
        self.user_id = None    

    def link_place(self, place):
        """Link this amenity to a place."""

        if isinstance(place, Place):
            if place.id != self.place_id:
                raise ValueError("Amenity cannot be linked to a different place.")
            place.add_amenity(self)  # Establish relationship
        else:
            raise ValueError("Invalid Place instance.")

    def to_dict(self):
        """Convert the Amenity object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "place_id": self.place_id,
            "user_id": self.user_id
        }

    def __repr__(self):
        """Returns a readable string representation of the amenity."""
        return f"Amenity(Name: {self.name}, Place ID: {self.place_id}, User ID: {self.user_id})"
