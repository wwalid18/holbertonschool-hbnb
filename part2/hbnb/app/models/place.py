from base_model import BaseModel
from user import User

class Place(BaseModel):
    """Represents a rental place"""

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        self.title = title[:100] if len(title) <= 100 else title[:100]
