from base_model import BaseModel

class Amenity(BaseModel):
    """Represents an amenity (e.g., Wi-Fi, Parking)"""

    def __init__(self, name):
        super().__init__()

        self.name = name[:50] if len(name) <= 50 else name[:50]
